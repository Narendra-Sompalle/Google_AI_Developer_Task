# 🤖 AI-Powered Assistant

A complete, production-ready conversational AI application with text and voice capabilities. Built with Python, Streamlit, Google Gemini API, and advanced voice processing.

## Features

✨ **Core Features:**
- 💬 **Text Interaction**: Chat with an AI assistant powered by Google Gemini
- 🎤 **Voice Input**: Speak your questions (speech-to-text)
- 🔊 **Voice Output**: Listen to AI responses (text-to-speech)
- 🧠 **Conversation Memory**: AI remembers last 3 interactions for context-aware responses
- 💾 **Session Management**: Clear conversation history anytime
- 🌐 **Web UI**: Clean, user-friendly Streamlit interface
- ⚙️ **Real-time Settings**: Monitor AI temperature, memory usage, and microphone status

## Architecture

```
GenAI_task/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variable template
├── .env                      # (Create this) Your API keys
├── README.md                 # This file
│
├── src/                      # Core application modules
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration and settings management
│   ├── llm_service.py       # Google Gemini API integration
│   ├── voice_service.py     # Speech recognition and TTS
│   └── memory.py            # Conversation memory management
│
└── utils/                    # Utility modules
    ├── __init__.py
    └── logger.py            # Logging functionality
```

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Streamlit | Web UI and user interaction |
| **LLM** | Google Generative AI | Intelligent text responses |
| **Speech-to-Text** | speech_recognition | Convert voice to text |
| **Text-to-Speech** | pyttsx3 | Convert text to voice |
| **API Key Management** | python-dotenv | Secure environment variables |
| **Language** | Python 3.8+ | Core application |

## Prerequisites

- Python 3.8 or higher
- Microphone (for voice input)
- Speaker or headphones (for voice output)
- Internet connection (for Google Gemini API)
- Google Gemini API key

## Installation

### Step 1: Clone or Download the Project

```bash
cd /home/naren/GenAI_task
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# On Linux/Mac
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: If PyAudio installation fails on Linux:
```bash
# Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-dev

# Then retry
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Get your Google Gemini API key:
   - Visit [https://ai.google.dev](https://ai.google.dev)
   - Sign in with your Google account
   - Create a new API key
   - Copy the API key

3. Edit `.env` and add your API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

### Step 5: Verify Setup

Test that everything is working:

```bash
# Test imports
python -c "from src.llm_service import LLMService; print('✅ LLM Service OK')"
python -c "from src.voice_service import VoiceService; print('✅ Voice Service OK')"
python -c "from src.memory import ConversationMemory; print('✅ Memory Service OK')"
```

## Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Using the Application

**Text Mode:**
1. Type your question in the text input box
2. Click "Send" or press Enter
3. Wait for the AI response
4. Optional: Click "Speak Response" to hear the answer

**Voice Mode:**
1. Click "Voice Input" button
2. Speak clearly into your microphone
3. Wait for speech recognition to complete
4. Your recognized text will be sent automatically

**Example Interactions:**
- "What is machine learning?"
- "Explain quantum computing in simple terms"
- "Tell me about Python programming"
- "What's the capital of France?"

### Settings Panel (Sidebar)

- **App Information**: Shows model and configuration details
- **Current Memory**: Displays how many interactions are stored
- **Microphone Status**: Shows if audio input is available
- **Clear Conversation**: Button to reset chat history and memory

## Configuration

Edit `.env` file to customize:

```env
# Required
GEMINI_API_KEY=your_api_key_here

# Optional: Customize AI behavior
APP_NAME=AI Assistant
MAX_CONVERSATION_MEMORY=3          # Number of past interactions to remember (1-10)
TEMPERATURE=0.7                    # AI creativity (0.0=factual, 1.0=creative)
MAX_TOKENS=1024                    # Maximum response length
```

**Configuration Parameters Explained:**

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `MAX_CONVERSATION_MEMORY` | 3 | 1-10 | How many previous interactions to include in context |
| `TEMPERATURE` | 0.7 | 0.0-1.0 | Lower = factual, Higher = creative responses |
| `MAX_TOKENS` | 1024 | 100-4000 | Maximum length of AI response |

## Project Structure Explanation

### `src/config.py`
- Centralized configuration management
- Loads environment variables from `.env`
- Validates required API keys
- Provides default values

### `src/memory.py`
- Manages conversation history
- Stores last N interactions
- Formats context for LLM
- Provides memory statistics

### `src/llm_service.py`
- Integrates with Google Gemini API
- Generates AI responses
- Manages LLM configuration
- Builds prompts with context

### `src/voice_service.py`
- Speech recognition (mic to text)
- Text-to-speech (text to audio)
- Microphone device detection
- Audio configuration

### `app.py`
- Main Streamlit application
- User interface implementation
- Session state management
- User interaction handling

### `utils/logger.py`
- Application logging utility
- Console output formatting
- Error tracking

## Error Handling

### Common Issues and Solutions

**"GEMINI_API_KEY is not set"**
- Make sure `.env` file exists in project root
- Verify API key is correctly copied
- Restart Streamlit app after editing `.env`

**Microphone not detected**
- Check microphone is connected
- Linux: Install `portaudio19-dev`
- Test: `python -c "import pyaudio; print('OK')"`

**Speech recognition fails**
- Speak clearly and slowly
- Reduce background noise
- Try again - it might be a network issue
- Check internet connection (uses Google Speech API)

**"Could not generate response"**
- Check internet connection
- Verify API key is valid
- Check API quota hasn't exceeded
- Restart application

### Debug Mode

To see detailed logs:

```bash
streamlit run app.py --logger.level=debug
```

## Code Examples

### Using LLM Service Directly

```python
from src.llm_service import LLMService
from src.memory import ConversationMemory

# Create memory
memory = ConversationMemory(max_memory=3)

# Initialize LLM
llm = LLMService(api_key="your-key", memory=memory)

# Generate response
response = llm.generate_response("What is AI?")
print(response)

# Store interaction
llm.add_to_memory("What is AI?", response)
```

### Using Voice Service Directly

```python
from src.voice_service import VoiceService

voice = VoiceService()

# Speech to text
text = voice.speech_to_text(timeout=10)
print(f"You said: {text}")

# Text to speech
voice.text_to_speech("Hello, this is a test message")
```

## Conversation Memory Explained

The assistant maintains memory of the last 3 interactions by default:

```
Interaction 1: 
- User: "What is Python?"
- Assistant: "Python is a programming language..."

Interaction 2:
- User: "What can I build with it?"
- Assistant: "You can build web apps, data science..."

Interaction 3:
- User: "Tell me more about web development"
- Assistant: "For web development, Python has..."  ← Uses context from previous interactions
```

When the user sends a new message, the LLM receives:
1. All previous interactions (for context)
2. The new user message
3. Instructions to provide relevant response

This allows the AI to:
- Understand follow-up questions
- Reference previous topics
- Maintain conversation flow
- Provide contextual responses

## Performance Notes

- **Response Time**: 1-3 seconds (depends on API latency)
- **Memory Usage**: ~150MB typical
- **Storage**: None (session-based, no persistence)
- **Scalability**: Single user session, suitable for personal use

## Security

✅ **Security Features:**
- API keys stored in `.env` (not in code)
- Environment variables loaded at runtime
- No credentials logged or transmitted unsecurely
- Session-based (no persistent storage)
- Direct HTTPS connection to Google API

⚠️ **Keep Secure:**
- Never commit `.env` file to version control
- Don't share your API key
- Keep `.env.example` as template only
- Use `.gitignore` to exclude `.env`

## Limitations

- ❌ No conversation persistence (resets on restart)
- ❌ No user authentication
- ❌ Limited to text and basic voice
- ❌ Single user per session
- ❌ No RAG or knowledge base
- ❌ Requires internet connection for LLM

## Future Improvements

1. **Conversation Persistence**
   - Save chat history to database
   - Load previous conversations
   - Export chat as PDF

2. **Enhanced Voice**
   - Multiple voice options
   - Voice profiles
   - Language selection

3. **User Management**
   - Multi-user support
   - User preferences
   - History per user

4. **Advanced Features**
   - Image understanding
   - Document Q&A (RAG)
   - Web search integration
   - Code execution
   - Sentiment analysis

5. **UI Improvements**
   - Dark mode
   - Custom themes
   - Message reactions
   - Message editing

6. **Performance**
   - Streaming responses
   - Caching frequently asked questions
   - Optimized memory management
   - Faster speech recognition

7. **Integration**
   - Slack integration
   - Telegram bot
   - Discord bot
   - Email notifications

## Testing

### Manual Testing Checklist

- [ ] Text input works
- [ ] AI response is generated
- [ ] Conversation history displays
- [ ] Voice input recognizes speech
- [ ] Voice output plays audio
- [ ] Clear conversation works
- [ ] Settings display correctly
- [ ] Error messages show on API errors

### Unit Test Example

```python
# test_memory.py
from src.memory import ConversationMemory

def test_memory_storage():
    memory = ConversationMemory(max_memory=2)
    memory.add_interaction("Hi", "Hello!")
    memory.add_interaction("How are you?", "I'm good")
    
    assert memory.get_interaction_count() == 2
    interactions = memory.get_memory_context()
    assert interactions[0]['user'] == "Hi"
    print("✅ Memory test passed")

if __name__ == "__main__":
    test_memory_storage()
```

## Troubleshooting

### App Won't Start
```bash
# Clear Streamlit cache
rm -rf ~/.streamlit
streamlit run app.py
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Microphone Issues
```bash
# Check available audio devices
python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_indexes())"
```

## License

This project is provided as-is for educational and personal use.

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review error messages in console
3. Verify `.env` configuration
4. Check Google Gemini API documentation

## Credits

Built with:
- [Streamlit](https://streamlit.io/) - UI Framework
- [Google Generative AI](https://ai.google.dev) - LLM Provider
- [SpeechRecognition](https://github.com/Uberi/speech_recognition) - Voice Input
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3) - Voice Output
- [python-dotenv](https://github.com/theskumar/python-dotenv) - Configuration

---

**Version**: 1.0.0  
**Last Updated**: May 2026  
**Status**: ✅ Production Ready
