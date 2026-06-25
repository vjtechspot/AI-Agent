import os
import certifi
import asyncio
import logging
import json
from typing import Annotated, Optional
from dotenv import load_dotenv

# Fix for SSL Certificate errors - MUST be before other imports
os.environ['SSL_CERT_FILE'] = certifi.where()

from livekit import agents, api
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
    sarvam,
)
from livekit.agents import llm

# Load environment variables
load_dotenv(".env")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("outbound-agent")

import config

def _build_tts(config_provider: str = None, config_voice: str = None):
    """Configure the Text-to-Speech provider based on config or env vars."""
    provider = (config_provider or os.getenv("TTS_PROVIDER", config.DEFAULT_TTS_PROVIDER)).lower()

    # Force Sarvam for Indian regional voices
    if provider == "sarvam" or config_voice in ["anushka", "aravind", "amartya", "dhruv"]:
        logger.info(f"Using Sarvam TTS (Voice: {config_voice or config.DEFAULT_TTS_VOICE})")
        model = os.getenv("SARVAM_TTS_MODEL", config.SARVAM_MODEL)
        voice = config_voice or config.DEFAULT_TTS_VOICE
        return sarvam.TTS(model=model, speaker=voice, target_language_code=config.SARVAM_LANGUAGE)

    if provider == "cartesia":
        logger.info("Using Cartesia TTS")
        return cartesia.TTS(model=config.CARTESIA_MODEL, voice=config.CARTESIA_VOICE)

    if provider == "deepgram":
        logger.info("Using Deepgram TTS")
        return deepgram.TTS(model="aura-asteria-en")

    # Default to OpenAI
    logger.info(f"Using OpenAI TTS (Voice: {config_voice or config.DEFAULT_TTS_VOICE})")
    voice = config_voice or config.DEFAULT_TTS_VOICE
    return openai.TTS(model="tts-1", voice=voice)


def _build_llm(config_provider: str = None):
    """Configure the LLM provider based on config or env vars."""
    provider = (config_provider or os.getenv("LLM_PROVIDER", config.DEFAULT_LLM_PROVIDER)).lower()

    if provider == "groq":
        logger.info("Using Groq LLM (High Speed)")
        return openai.LLM(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY"),
            model=config.GROQ_MODEL,
            temperature=config.GROQ_TEMPERATURE,
        )

    logger.info("Using OpenAI LLM")
    return openai.LLM(model=config.DEFAULT_LLM_MODEL)


class TransferFunctions(llm.ToolContext):
    def __init__(self, ctx: agents.JobContext, phone_number: str = None):
        super().__init__(tools=[])
        self.ctx = ctx
        self.phone_number = phone_number

    @llm.function_tool(description="Look up user details by phone number.")
    def lookup_user(self, phone: str):
        logger.info(f"Looking up user: {phone}")
        return f"User details for {phone}: Preferred language Kannada. Status: Active."

    @llm.function_tool(description="Transfer the call to a human support agent.")
    async def transfer_call(self, destination: Optional[str] = None):
        destination = destination or config.DEFAULT_TRANSFER_NUMBER
        if not destination:
            return "Error: No transfer number available."

        if "@" not in destination and config.SIP_DOMAIN:
            clean_dest = destination.replace("tel:", "").replace("sip:", "")
            destination = f"sip:{clean_dest}@{config.SIP_DOMAIN}"

        # Find the participant to transfer
        participant_identity = None
        if self.phone_number:
            participant_identity = f"sip_{self.phone_number}"
        else:
            # Fallback: Find any remote participant that looks like a SIP caller
            for p in self.ctx.room.remote_participants.values():
                if "sip_" in p.identity:
                    participant_identity = p.identity
                    break

        if not participant_identity:
            return "Error: Could not find participant to transfer."

        try:
            logger.info(f"Transferring {participant_identity} to {destination}")
            await self.ctx.api.sip.transfer_sip_participant(
                api.TransferSIPParticipantRequest(
                    room_name=self.ctx.room.name,
                    participant_identity=participant_identity,
                    transfer_to=destination
                )
            )
            return "Transfer initiated successfully. Please wait while I connect you."
        except Exception as e:
            logger.error(f"Transfer failed: {e}")
            return f"Transfer failed: {e}"


class OutboundAssistant(Agent):
    def __init__(self, tools: list) -> None:
        super().__init__(
            instructions=config.SYSTEM_PROMPT,
            tools=tools,
        )

async def entrypoint(ctx: agents.JobContext):
    logger.info(f"Agent starting for room: {ctx.room.name}")

    # Parse metadata from job or room
    phone_number = None
    config_dict = {}
    try:
        metadata = ctx.job.metadata or ctx.room.metadata
        if metadata:
            data = json.loads(metadata)
            phone_number = data.get("phone_number")
            config_dict = data
    except Exception:
        logger.warning("Failed to parse metadata")

    fnc_ctx = TransferFunctions(ctx, phone_number)

    # Initialize session with metadata overrides if present
    llm_instance = _build_llm(config_dict.get("llm_provider"))
    tts_instance = _build_tts(config_dict.get("tts_provider"), config_dict.get("voice_id"))

    session = AgentSession(
        vad=silero.VAD.load(),
        stt=deepgram.STT(model=config.STT_MODEL, language=config.STT_LANGUAGE),
        llm=llm_instance,
        tts=tts_instance,
    )

    await session.start(
        room=ctx.room,
        agent=OutboundAssistant(tools=list(fnc_ctx.function_tools.values())),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVCTelephony(),
            close_on_disconnect=True,
        ),
    )

    # Check if we need to dial out
    should_dial = False
    if phone_number:
        user_already_here = False
        for p in ctx.room.remote_participants.values():
            if f"sip_{phone_number}" in p.identity or "sip_" in p.identity:
                user_already_here = True
                break

        if not user_already_here:
            should_dial = True

    if should_dial:
        logger.info(f"Dialing {phone_number} via SIP Trunk...")
        try:
            await ctx.api.sip.create_sip_participant(
                api.CreateSIPParticipantRequest(
                    room_name=ctx.room.name,
                    sip_trunk_id=config.SIP_TRUNK_ID,
                    sip_call_to=phone_number,
                    participant_identity=f"sip_{phone_number}",
                    wait_until_answered=True,
                )
            )
            logger.info("Call answered. Waiting 1s for audio stabilization...")
            await asyncio.sleep(1)
            await session.generate_reply(instructions=config.INITIAL_GREETING)
        except Exception as e:
            logger.error(f"Call failed: {e}")
            ctx.shutdown()
    else:
        logger.info("User already present. Greeting immediately...")
        await session.generate_reply(instructions=config.fallback_greeting)

if __name__ == "__main__":
    agents.cli.run_app(
        agents.WorkerOptions(
            entrypoint_fnc=entrypoint,
            agent_name="outbound-caller",
        )
    )
