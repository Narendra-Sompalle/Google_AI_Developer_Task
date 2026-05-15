# 🚀 Quick Start Guide

## Installation (5 minutes)

### 1. Prerequisites
- Python 3.8+
- Microphone
- Google Gemini API key (free)

### 2. Get API Key
1. Go to [https://ai.google.dev](https://ai.google.dev)
2. Sign in with Google
3. Create API key
4. Copy the key

### 3. Setup Project

**Option A: Automatic Setup (Linux/Mac)**
```bash
chmod +x setup.sh
./setup.sh
# Edit .env with your API key
streamlit run app.py
```

**Option B: Manual Setup**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your API key
# GEMINI_API_KEY=your_key_here

# Run the app
streamlit run app.py
```

### 4. Access Application
Open your browser to: **http://localhost:8501**

---

## Usage (1 minute)

### Text Mode
1. Type question in input box
2. Click "Send"
3. Wait for response
4. (Optional) Click "Speak Response" to hear it

### Voice Mode
1. Click "Voice Input" button
2. Speak into microphone
3. AI responds automatically

### Clear History
Use "Clear Conversation" button in sidebar anytime

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "GEMINI_API_KEY not set" | Edit `.env`, add API key, restart app |
| Microphone not found | Install: `sudo apt-get install portaudio19-dev` |
| Speech recognition fails | Speak clearly, check internet |
| App won't start | Check Python 3.8+, reinstall dependencies |

---

## Project Files

```
GenAI_task/
├── app.py                 ← Main application (run this)
├── requirements.txt       ← Dependencies
├── .env                   ← Your API keys (create from .env.example)
├── src/
│   ├── config.py         ← Settings
│   ├── llm_service.py    ← Gemini AI
│   ├── voice_service.py  ← Speech/Audio
│   └── memory.py         ← Conversation memory
└── utils/
    └── logger.py         ← Logging
```

---

## First Message Test

After setup, try these questions:
- "What is machine learning?"
- "Tell me about Python"
- "Explain AI in 2 sentences"

---

## Documentation

- Full details: See [README.md](README.md)
- Architecture: See Architecture section in README
- Configuration: Edit `.env` file
- Troubleshooting: See README.md Troubleshooting section

---

**Status**: ✅ Ready to Use
