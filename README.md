# Sri Star Gold - AI Telecalling Agent 📞

A multilingual (Kannada, Hindi, Tamil, Telugu) production-ready voice agent for **Sri Star Gold Company**. Built using **LiveKit**, **Sarvam AI**, and **Groq**.

## 🚀 Features
- **Multilingual Support**: Starts in Kannada; switches to Hindi, Tamil, or Telugu automatically.
- **Ultra-Fast LLM**: Powered by **Groq (Llama 3.3 70B)** for human-like response speeds.
- **Indian Native Voices**: Uses **Sarvam AI (Anushka voice)** for natural-sounding regional languages.
- **Lead Capture**: Automatically extracts and logs customer details (Name, Grams, Address).
- **SIP Integration**: Seamlessly integrated with **Vobiz** for outbound calling.

---

## 🛠️ Setup & Installation (Windows)

### 1. Prerequisites
- Python 3.10+
- LiveKit Cloud Account
- Sarvam AI API Key (for high-quality Indian voices)
- Groq API Key (for fast intelligence)
- Vobiz SIP Account

### 2. Installation
```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
.\venv\Scripts\pip.exe install -r requirements.txt
```

### 3. Environment Configuration
Ensure your `.env` file contains the correct LiveKit and Vobiz credentials. Specifically, ensure `VOBIZ_SIP_TRUNK_ID` starts with `ST_` (LiveKit internal ID).

---

## 🏃‍♂️ Usage (Windows)

### Step 1: Start the Agent
This worker must be running to handle the calls.
```powershell
.\venv\Scripts\python.exe agent.py dev
```
*Wait for: `[INFO] outbound-agent: worker registered`.*

### Step 2: Initiate a Call
In a **new terminal window**, run:
```powershell
.\venv\Scripts\python.exe make_call.py --to +91XXXXXXXXXX
```

---

## 🔧 Windows Troubleshooting

### ❌ Error: `SSL: CERTIFICATE_VERIFY_FAILED`
**Fix:** The agent already includes `certifi` logic. Ensure `pip install certifi` was successful.

### ❌ Error: `404 Not Found` (SIP Trunk)
**Fix:** The ID in `.env` is likely your Vobiz ID, not the LiveKit ID.
1. Run `.\venv\Scripts\python.exe create_trunk.py`.
2. Copy the `ST_...` ID from the output.
3. Update `VOBIZ_SIP_TRUNK_ID` in `.env`.

### ❌ Agent is running but phone doesn't ring
**Fix:**
1. Check the Agent terminal for `--- STEP 3 ---`.
2. If it stops there, check your Vobiz **Username** and **Password** in `.env`.
3. Ensure your Vobiz account has an active balance.

---

## 📂 Key Files
- `agent.py`: Core AI logic & Multilingual switching.
- `config.py`: Prompt engineering & Model settings.
- `make_call.py`: Outbound trigger script.
- `.env`: API Keys & SIP Credentials.
