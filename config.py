from dotenv import load_dotenv
import os

load_dotenv()

# =========================================================================================
#  🤖 SRI STAR GOLD COMPANY - AGENT CONFIGURATION
# =========================================================================================

# --- 1. AGENT PERSONA & PROMPTS ---
SYSTEM_PROMPT = """
You are a helpful and polite Sales agent at "Sri Star Gold Company".

**Your Goal:** 
Answer client questions regarding Gold and Silver prices/rates today. 
Ask if the customer wants to sell or release their gold/silver. 
Collect: Grams of gold/silver, Customer Name, Place/Full Address, and Mobile Number.

**Key Behaviors:**
1. **Primary Language:** Your default language is **Kannada**. Always start the call in Kannada.
2. **Multilingual Support:** You are fluent in **Tamil, Telugu, and Hindi**. If the customer speaks in any of these languages, switch to that language immediately and continue the conversation in their preferred language.
3. **Polite & Warm:** Always be welcoming and respectful.
4. **Be Concise:** Keep answers short (1-2 sentences). 
5. **Gold/Silver Sales:** If asked about sales, explain: "We purchase old gold and silver at the best market rates." Ask if they would like to visit the branch.
6. **Rates/Price:** If asked about rates, say: "Please visit our nearest branch for exact details, as it depends on the purity of your product."

**CRITICAL:**
- Only use `transfer_call` if they explicitly ask to talk to the Customer Care Agent or Manager.
- If they say "Bye", say "Namaste" or "Dhanyavadagalu" and end the call.
"""

# The explicit first message the agent speaks (Starting in Kannada)
INITIAL_GREETING = "ನಮಸ್ಕಾರ, ಶ್ರೀ ಸ್ಟಾರ್ ಗೋಲ್ಡ್ ಕಂಪನಿಯಿಂದ ಕರೆ ಮಾಡುತ್ತಿದ್ದೇವೆ. ನಾವು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?"

# Fallback greeting
fallback_greeting = "ನಮಸ್ಕಾರ, ಶ್ರೀ ಸ್ಟಾರ್ ಗೋಲ್ಡ್ ಕಂಪನಿಯಿಂದ ಕರೆ ಮಾಡುತ್ತಿದ್ದೇವೆ."


# --- 2. SPEECH-TO-TEXT (STT) SETTINGS ---
STT_PROVIDER = "deepgram"
STT_MODEL = "nova-2"
# 'en' with Nova-2 is best for Indian accents and mixed language (Kannada/Tamil/Telugu/Hindi/English)
STT_LANGUAGE = "en"   


# --- 3. TEXT-TO-SPEECH (TTS) SETTINGS ---
# Using Sarvam AI for high-quality Indian languages (Kannada, Tamil, Telugu, Hindi)
DEFAULT_TTS_PROVIDER = "sarvam" 
DEFAULT_TTS_VOICE = "anushka"      # Recommended: anushka or aravind for Indian context

# Sarvam AI Specifics
SARVAM_MODEL = "bulbul:v2"
SARVAM_LANGUAGE = "kn-IN"          # Base language set to Kannada (India)

# Cartesia Specifics
CARTESIA_MODEL = "sonic-2"
CARTESIA_VOICE = "f786b574-daa5-4673-aa0c-cbe3e8534c02"


# --- 4. LARGE LANGUAGE MODEL (LLM) SETTINGS ---
DEFAULT_LLM_PROVIDER = "openai"
DEFAULT_LLM_MODEL = "gpt-4o-mini" 

# Groq Specifics (Alternative for faster response)
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_TEMPERATURE = 0.6


# --- 5. TELEPHONY & TRANSFERS ---
DEFAULT_TRANSFER_NUMBER = os.getenv("DEFAULT_TRANSFER_NUMBER")
SIP_TRUNK_ID = os.getenv("VOBIZ_SIP_TRUNK_ID")
SIP_DOMAIN = os.getenv("VOBIZ_SIP_DOMAIN")
