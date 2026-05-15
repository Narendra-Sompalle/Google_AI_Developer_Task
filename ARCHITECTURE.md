# 🏗️ Architecture Documentation

## System Overview

The AI Assistant follows a **modular, layered architecture** designed for:
- ✅ Easy maintenance
- ✅ Scalability
- ✅ Clear separation of concerns
- ✅ Simple testing
- ✅ Extensibility

```
┌─────────────────────────────────────────────────┐
│         Web UI Layer (Streamlit)                │
│    - User Input/Output                          │
│    - Chat History Display                       │
│    - Session Management                         │
└─────────────┬───────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────┐
│      Service Layer                              │
│  ┌──────────────┐  ┌──────────────────────┐   │
│  │ LLM Service  │  │  Voice Service       │   │
│  │ (Gemini API) │  │  (Speech I/O)        │   │
│  └──────────────┘  └──────────────────────┘   │
└─────────────┬───────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────┐
│      Core Layer                                 │
│  ┌──────────────┐  ┌──────────────────────┐   │
│  │    Memory    │  │    Config            │   │
│  │  Management  │  │  Management          │   │
│  └──────────────┘  └──────────────────────┘   │
└─────────────┬───────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────┐
│      External APIs & Services                   │
│  - Google Generative AI (Gemini)                │
│  - Google Speech Recognition                    │
│  - System Audio (pyttsx3)                       │
└─────────────────────────────────────────────────┘
```

## Component Architecture

### 1. **Presentation Layer** (`app.py`)

**Responsibility**: User interface and interaction handling

```python
Main Streamlit App
├── Session State Management
│   ├── LLM Service instance
│   ├── Voice Service instance
│   └── Chat History
├── UI Components
│   ├── Chat History Display
│   ├── Text Input Box
│   ├── Voice Input Button
│   ├── Sidebar Settings
│   └── Help Section
└── Event Handlers
    ├── Text Input Handler
    ├── Voice Input Handler
    └── Response Playback Handler
```

**Design Principles**:
- Single responsibility: Only handles UI
- No business logic in UI
- Delegates to services
- Manages session state using Streamlit's session_state

### 2. **Service Layer**

#### A. LLM Service (`src/llm_service.py`)

**Responsibility**: AI model interaction and response generation

```python
LLMService
├── Initialization
│   ├── API Key Configuration
│   ├── Model Loading
│   └── Temperature Settings
├── Core Functions
│   ├── generate_response()
│   ├── _build_prompt()
│   ├── add_to_memory()
│   └── clear_memory()
└── Dependencies
    └── ConversationMemory
```

**Key Features**:
- Single API key per instance
- Encapsulates Gemini API complexity
- Manages prompt construction with context
- Memory integration for context-aware responses

**Workflow**:
```
User Input
    ↓
get_memory_context() ← Retrieve past interactions
    ↓
_build_prompt() ← Construct full prompt
    ↓
model.generate_content() ← Call Gemini API
    ↓
add_to_memory() ← Store interaction
    ↓
Return Response
```

#### B. Voice Service (`src/voice_service.py`)

**Responsibility**: Speech input/output operations

```python
VoiceService
├── Speech-to-Text
│   ├── speech_to_text()
│   ├── Microphone Setup
│   └── Google Speech Recognition
├── Text-to-Speech
│   ├── text_to_speech()
│   ├── pyttsx3 Engine
│   └── Audio Output
└── Utilities
    ├── test_microphone()
    └── get_audio_devices()
```

**Error Handling**:
- Microphone access failures
- Speech recognition timeouts
- Audio device unavailability
- Network issues (speech recognition)

### 3. **Core Layer**

#### A. Memory Management (`src/memory.py`)

**Responsibility**: Conversation history and context management

```python
ConversationMemory
├── Storage
│   └── interactions[] ← List of interaction pairs
├── Size Management
│   ├── max_memory (configurable)
│   └── Auto-trim oldest when full
├── Operations
│   ├── add_interaction()
│   ├── get_memory_context()
│   ├── get_memory_text()
│   ├── clear_memory()
│   └── get_interaction_count()
└── Format
    └── {"user": "...", "assistant": "...", "timestamp": "..."}
```

**Memory Window Strategy**:
```
Interaction Limit = 3 (configurable)

Scenario 1: First message
- No previous context
- Prompt = User message

Scenario 2: After 3 messages
Memory:
[Msg1_User, Msg1_Asst]
[Msg2_User, Msg2_Asst]
[Msg3_User, Msg3_Asst]
Prompt = All 3 + new message

Scenario 3: 4th message (exceeds limit)
Memory:
[Msg2_User, Msg2_Asst]  ← Msg1 removed
[Msg3_User, Msg3_Asst]
[Msg4_User, Msg4_Asst]
Prompt = Last 3 + new message
```

#### B. Configuration (`src/config.py`)

**Responsibility**: Centralized settings and environment management

```python
Config Class
├── API Configuration
│   └── GEMINI_API_KEY
├── Model Configuration
│   ├── TEMPERATURE
│   ├── MAX_TOKENS
│   └── MAX_CONVERSATION_MEMORY
├── Voice Configuration
│   ├── VOICE_RATE
│   └── VOICE_LANGUAGE
├── UI Configuration
│   ├── PAGE_TITLE
│   └── PAGE_LAYOUT
└── Validation
    └── validate_config()
```

**Environment Loading**:
```
1. .env file loaded via python-dotenv
2. Values read from Config class
3. Defaults applied if not in .env
4. Validation ensures required keys present
```

## Data Flow Diagrams

### Text Conversation Flow

```
User Types Message
    ↓
[Click Send Button]
    ↓
app.py: handle_text_input()
    ↓
LLMService.generate_response()
    ├─ memory.get_memory_text() ← Get context
    ├─ _build_prompt() ← Construct prompt with context
    └─ API Call: genai.GenerativeModel.generate_content()
    ↓
LLMService.add_to_memory() ← Store interaction
    ↓
Display Response in Chat
    ↓
Optional: VoiceService.text_to_speech()
    ↓
Play Audio Output
```

### Voice Conversation Flow

```
User Clicks [Voice Input]
    ↓
VoiceService.speech_to_text()
    ├─ Activate Microphone
    ├─ Listen (max 10 seconds)
    └─ Google Speech Recognition API
    ↓
Get Recognized Text
    ↓
handle_text_input(recognized_text)
    ↓
[Same as text flow above]
    ↓
Optional: Auto-play response as voice
```

## Design Decisions

### 1. **Modular Services**

✅ **Decision**: Create separate service classes

**Rationale**:
- LLM logic independent of UI
- Voice can be mocked in tests
- Easy to replace services
- Reusable components

**Alternative Rejected**:
- Monolithic design (harder to test/maintain)

### 2. **Session-Based Memory**

✅ **Decision**: Store memory in-session only

**Rationale**:
- Simple, no database
- Requirement scope: no persistence
- Fast access
- Fresh start each session

**Alternative Rejected**:
- Database persistence (over-engineering for scope)

### 3. **Limited Context Window**

✅ **Decision**: Store only last 3 interactions

**Rationale**:
- Balances context with token usage
- Prevents API costs from growing
- Suitable for short conversations
- Still provides good context awareness

**Trade-off**:
- Longer conversations may lose context
- Configure MAX_CONVERSATION_MEMORY if needed

### 4. **pyttsx3 for TTS**

✅ **Decision**: Use pyttsx3 instead of gTTS

**Rationale**:
- Offline capable (no API needed)
- No latency
- Works everywhere
- Simpler setup

**Trade-off**:
- Less natural voice
- Limited voice options

### 5. **Streamlit for UI**

✅ **Decision**: Use Streamlit

**Rationale**:
- Rapid UI development
- No frontend knowledge needed
- State management built-in
- Deploy easily

**Alternative Rejected**:
- Flask (more verbose)
- FastAPI (overkill for simple UI)

## Extensibility Points

### Adding New Features

#### 1. Add RAG Support
```python
# src/rag_service.py
class RAGService:
    def embed_documents(self, docs: List[str]):
        # Implement embedding
        pass
    
    def retrieve_context(self, query: str):
        # Implement retrieval
        pass

# In LLMService:
def __init__(self, ..., rag_service=None):
    self.rag_service = rag_service

def generate_response(self, user_input):
    context = self.rag_service.retrieve_context(user_input)
    # Use context in prompt
```

#### 2. Add Database Support
```python
# src/persistence.py
class PersistenceService:
    def save_conversation(self, user_id, interactions):
        # Save to DB
        pass
    
    def load_conversation(self, user_id):
        # Load from DB
        pass

# In app.py:
persistence = PersistenceService()
chat_history = persistence.load_conversation(user_id)
```

#### 3. Add Multiple LLM Support
```python
# src/llm_factory.py
class LLMFactory:
    @staticmethod
    def create_service(provider: str):
        if provider == 'gemini':
            return LLMService(...)
        elif provider == 'openai':
            return OpenAIService(...)
        # ...
```

#### 4. Add Advanced Voice Features
```python
# src/advanced_voice_service.py
class AdvancedVoiceService(VoiceService):
    def text_to_speech_streaming(self, text):
        # Stream audio
        pass
    
    def speech_to_text_continuous(self):
        # Continuous listening
        pass
```

## Performance Considerations

### Current Performance

| Metric | Value |
|--------|-------|
| Response Time | 1-3 seconds |
| Memory Usage | ~150MB |
| Storage | None (session) |
| API Latency | 0.5-1 second |

### Optimization Opportunities

1. **Response Streaming**: Use streaming API for faster perceived response
2. **Caching**: Cache common questions
3. **Batch Processing**: Handle multiple requests
4. **Async Operations**: Non-blocking voice processing

## Security Architecture

```
User Input
    ↓
[Validation]
    ↓
[Sanitization]
    ↓
[API Key Injection from .env]
    ↓
[HTTPS to Google API]
    ↓
[Response Processing]
    ↓
[Session Storage (no persistence)]
```

**Security Features**:
- ✅ Environment variables (no hardcoded keys)
- ✅ HTTPS for API calls
- ✅ No sensitive data logging
- ✅ Session-based (no cross-user data)

## Testing Architecture

```
Unit Tests
├── test_memory.py
├── test_config.py
├── test_llm_service.py (mocked API)
└── test_voice_service.py (mocked audio)

Integration Tests
├── test_app_flow.py
└── test_end_to_end.py

Manual Tests
├── Text input flow
├── Voice input flow
└── UI responsiveness
```

## Deployment Considerations

### Local Deployment
```bash
streamlit run app.py
# Single user, development
```

### Cloud Deployment (Streamlit Cloud)
```bash
git push to GitHub
# Streamlit auto-deploys
# Requires .env variables in secrets
```

### Multi-User Server (Flask-based)
```python
# Would require separate architecture
# Session management per user
# Database for persistence
```

---

## Summary

The AI Assistant architecture achieves:
- **Modularity**: Each component has single responsibility
- **Simplicity**: No over-engineering
- **Maintainability**: Clear separation of concerns
- **Testability**: Services can be mocked
- **Extensibility**: Easy to add features
- **Performance**: Optimized for responsive UI
- **Security**: API keys protected

**Total Lines**: ~600 (excluding tests & docs)  
**Complexity**: Low-to-Medium  
**Scalability**: Single-user (easily adaptable for multi-user)
