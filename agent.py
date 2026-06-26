import os
import certifi
import asyncio
import logging
import json
from typing import Annotated, Optional
from dotenv import load_dotenv

# MUST BE FIRST: Fix for Windows SSL
os.environ['SSL_CERT_FILE'] = certifi.where()

from livekit import agents, api
from livekit.agents import JobContext, WorkerOptions, VoicePipelineAgent, chat_ctx
from livekit.plugins import openai, deepgram, silero, sarvam
from livekit.agents.llm import ToolContext, function_tool

# Load configuration
load_dotenv(".env")
import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("outbound-agent")

class SalesTools(ToolContext):
    def __init__(self, ctx: JobContext, phone_number: str = None):
        super().__init__()
        self.ctx = ctx
        self.phone_number = phone_number

    @function_tool(description="Save customer details (Name, Grams, Address) into the company system.")
    def save_lead(self, name: str, grams: str, address: str, item_type: str = "gold"):
        logger.info(f"LEAD CAPTURED: {name} | {grams}g {item_type} | Address: {address} | Phone: {self.phone_number}")
        return f"Thank you {name}. I have recorded your interest in {grams} grams of {item_type}."

    @function_tool(description="End the call after the conversation is finished.")
    async def end_call(self):
        logger.info("Agent requested to end the call.")
        asyncio.create_task(self._delayed_disconnect())
        return "Thank you for contacting Sri Star Gold Company. Namaskara."

    async def _delayed_disconnect(self):
        await asyncio.sleep(2) # Allow speech to finish
        await self.ctx.room.disconnect()

async def entrypoint(ctx: JobContext):
    logger.info(f"--- STEP 1: Agent Joined Room {ctx.room.name} ---")

    # Get phone number from metadata
    phone_number = None
    if ctx.job.metadata:
        try:
            parsed = json.loads(ctx.job.metadata)
            phone_number = parsed.get("phone_number") if isinstance(parsed, dict) else str(parsed)
        except:
            phone_number = ctx.job.metadata

    logger.info(f"--- STEP 2: Target Number identified: {phone_number} ---")
    
    # Initialize the Voice Pipeline
    initial_ctx = chat_ctx.ChatContext().append(role="system", text=config.SYSTEM_PROMPT)
    
    agent = VoicePipelineAgent(
        vad=silero.VAD.load(),
        stt=deepgram.STT(model=config.STT_MODEL, language=config.STT_LANGUAGE),
        llm=openai.LLM(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY"),
            model=config.GROQ_MODEL
        ),
        tts=sarvam.TTS(
            model=config.SARVAM_MODEL, 
            speaker=config.DEFAULT_TTS_VOICE, 
            target_language_code=config.SARVAM_LANGUAGE
        ),
        chat_ctx=initial_ctx,
        fnc_ctx=SalesTools(ctx, phone_number),
    )

    agent.start(ctx.room)
    logger.info("--- STEP 3: AI Pipeline Active ---")

    # Initiate Dial-out
    if phone_number:
        trunk_id = os.getenv("VOBIZ_SIP_TRUNK_ID")
        clean_number = phone_number.replace('+', '') # Some providers like Vobiz prefer digits only
        
        logger.info(f"--- STEP 4: Calling {clean_number} via {trunk_id} ---")
        try:
            await ctx.api.sip.create_sip_participant(
                api.CreateSIPParticipantRequest(
                    room_name=ctx.room.name,
                    sip_trunk_id=trunk_id,
                    sip_call_to=clean_number,
                    participant_identity=f"sip_{clean_number}",
                    wait_until_answered=False # Critical for bypassing SIP delay
                )
            )
            logger.info("--- STEP 5: Dial Command Sent ---")
            await asyncio.sleep(1)
            await agent.say(config.INITIAL_GREETING, allow_interruptions=True)
        except Exception as e:
            logger.error(f"--- FAILED: {e} ---")
            ctx.shutdown()

if __name__ == "__main__":
    print("SRI STAR GOLD AGENT STARTING...")
    agents.cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, agent_name="outbound-caller"))
