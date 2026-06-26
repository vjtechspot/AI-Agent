import os
from dotenv import load_dotenv

load_dotenv()

# --- 1. AGENT PERSONA ---
SYSTEM_PROMPT = """
You are a helpful and polite Sales agent at "Sri Star Gold Company".

**Your Goal:** 
Answer client questions regarding Gold and Silver prices/rates today. 
Ask if the customer wants to sell or release their gold/silver. 
Collect: Grams of gold/silver, Customer Name, Place/Full Address, and Mobile Number.

**Key Behaviors:**
1. **Language:** Start in Kannada. Switch to Hindi, Tamil, or Telugu if the customer uses them.
2. **Concise:** Keep answers under 2 sentences.
3. **Rates:** Tell them to visit the branch for exact rates based on purity.
"""

INITIAL_GREETING = "ನಮಸ್ಕಾರ, ಶ್ರೀ ಸ್ಟಾರ್ ಗೋಲ್ಡ್ ಕಂಪನಿಯಿಂದ ಕರೆ ಮಾಡುತ್ತಿದ್ದೇವೆ. ನಾವು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?"

# --- 2. MODELS & PLUGINS ---
# STT Settings
STT_MODEL = "nova-2"
STT_LANGUAGE = "en" # 'en' is best for multi-language Indian accents

# TTS Settings (Sarvam AI)
DEFAULT_TTS_VOICE = "anushka"
SARVAM_MODEL = "bulbul:v2"
SARVAM_LANGUAGE = "kn-IN"

# LLM Settings (Groq)
GROQ_MODEL = "llama-3.3-70b-versatile"

# --- 3. SIP & TELEPHONY ---
# This pulls the Trunk ID from your .env file
VOBIZ_SIP_TRUNK_ID = os.getenv("VOBIZ_SIP_TRUNK_ID")
DEFAULT_TRANSFER_NUMBER = os.getenv("DEFAULT_TRANSFER_NUMBER")
