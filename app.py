import streamlit as st
from pathlib import Path
import sys
from datetime import datetime

# =========================================================
# PROJECT IMPORTS
# =========================================================
sys.path.insert(0, str(Path(__file__).parent))

from streamlit_mic_recorder import mic_recorder
from src.config import Config
from src.llm_service import LLMService
from src.voice_service import VoiceService
from src.memory import ConversationMemory

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="AI Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# PRODUCTION CSS
# =========================================================
st.markdown("""
<style>

/* =========================================================
FONTS
========================================================= */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* =========================================================
GLOBAL
========================================================= */
html, body, .stApp {
    background: #0b1020;
    color: white;
}

/* Remove Streamlit Header */
header,
[data-testid="stHeader"],
[data-testid="collapsedControl"] {
    display: none !important;
}

/* Main Layout */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 9rem !important;
    max-width: 950px !important;
}

/* =========================================================
SIDEBAR
========================================================= */
section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid rgba(255,255,255,0.06);
    width: 270px !important;
}

.sidebar-title {
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 24px;
    color: white;
}

.stButton > button {
    border-radius: 12px !important;
    border: none !important;
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 10px 16px !important;
    transition: 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    opacity: 0.95;
}

/* =========================================================
HERO SECTION
========================================================= */
.hero-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 70vh;
    text-align: center;
    flex-direction: column;
}

.hero-title {
    font-size: 56px;
    font-weight: 700;
    margin-bottom: 12px;
    background: linear-gradient(to right, #ffffff, #a5b4fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #9ca3af;
    font-size: 18px;
}

/* =========================================================
CHAT MESSAGES
========================================================= */
[data-testid="stChatMessage"] {
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 18px;
    border: 1px solid rgba(255,255,255,0.06);
    background: #151b2e;
}

/* User Message */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, #312e81, #4c1d95);
    border: none;
}

/* Assistant Message */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: #151b2e;
}

/* Markdown Text */
.stMarkdown p {
    font-size: 15px !important;
    line-height: 1.8 !important;
    color: #f3f4f6;
}

/* =========================================================
CHAT INPUT
========================================================= */
.stChatInput {
    position: fixed !important;
    bottom: 25px;
    left: 50%;
    transform: translateX(-50%);
    width: min(920px, 92%);
    background: #111827 !important;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px !important;
    padding: 10px 14px !important;
    z-index: 9999;
    box-shadow: 0 10px 40px rgba(0,0,0,0.35);
}

/* Input Inner Area */
.stChatInput textarea {
    background: transparent !important;
    color: white !important;
    font-size: 15px !important;
}

/* Placeholder */
.stChatInput textarea::placeholder {
    color: #9ca3af !important;
}

/* Remove Borders */
.stChatInput > div {
    border: none !important;
}

/* =========================================================
MIC BUTTON
========================================================= */
.mic-wrapper {
    position: fixed;
    bottom: 38px;
    right: 7%;
    z-index: 999999;
}

/* =========================================================
ACTION BUTTONS
========================================================= */
.action-row {
    display: flex;
    gap: 8px;
    margin-top: 10px;
}

.action-row button {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 10px !important;
    border: none !important;
}

/* =========================================================
SCROLLBAR
========================================================= */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #374151;
    border-radius: 20px;
}

/* =========================================================
RESPONSIVE
========================================================= */
@media (max-width: 768px) {

    .hero-title {
        font-size: 36px;
    }

    .hero-subtitle {
        font-size: 15px;
    }

    .block-container {
        padding-left: 12px !important;
        padding-right: 12px !important;
    }

    .stChatInput {
        width: 95%;
    }

    .mic-wrapper {
        right: 10%;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# INITIALIZE SESSION
# =========================================================
def initialize():

    if "llm" not in st.session_state:
        st.session_state.llm = LLMService(
            Config.GEMINI_API_KEY,
            ConversationMemory(Config.MAX_CONVERSATION_MEMORY)
        )

    if "voice" not in st.session_state:
        st.session_state.voice = VoiceService()

    if "history" not in st.session_state:
        st.session_state.history = []

# =========================================================
# SEND MESSAGE
# =========================================================
def send_message(prompt):

    st.session_state.history.append({
        "role": "user",
        "content": prompt,
        "time": datetime.now().strftime("%H:%M")
    })

    try:

        with st.spinner("Thinking..."):

            response = st.session_state.llm.generate_response(prompt)

            st.session_state.llm.add_to_memory(prompt, response)

            st.session_state.history.append({
                "role": "assistant",
                "content": response,
                "time": datetime.now().strftime("%H:%M")
            })

    except Exception as e:

        error_text = str(e)

        if "429" in error_text or "quota" in error_text.lower():

            response = """
### ⚠️ Gemini API Quota Exceeded

Your current Gemini API free-tier limit has been reached.

#### Fix Options:
- Wait for quota reset
- Upgrade Gemini API billing
- Use another API key
- Reduce request frequency

This is an API limitation — not a UI issue.
"""

        else:
            response = f"⚠️ Error:\n\n{error_text}"

        st.session_state.history.append({
            "role": "assistant",
            "content": response,
            "time": datetime.now().strftime("%H:%M")
        })

    st.rerun()

# =========================================================
# MAIN APP
# =========================================================
def main():

    initialize()

    # =====================================================
    # SIDEBAR
    # =====================================================
    with st.sidebar:

        st.markdown(
            '<div class="sidebar-title">✨ AI Assistant</div>',
            unsafe_allow_html=True
        )

        if st.button("➕ New Chat", use_container_width=True):

            st.session_state.history = []
            st.session_state.llm.clear_memory()
            st.rerun()

        st.markdown("---")

        st.markdown("""
### Features

- 🎤 Voice Assistant
- ⚡ Fast Responses
- 🧠 Conversation Memory
- 🌙 Modern Dark UI
- 📱 Mobile Responsive
""")

    # =====================================================
    # HERO SECTION
    # =====================================================
    if len(st.session_state.history) == 0:

        st.markdown("""
        <div class="hero-container">
            <div class="hero-title">
                How can I help today?
            </div>

           
        </div>
        """, unsafe_allow_html=True)

    # =====================================================
    # CHAT HISTORY
    # =====================================================
    for idx, message in enumerate(st.session_state.history):

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            # assistant action buttons
            if message["role"] == "assistant":

                col1, col2, col3, col4 = st.columns([1,1,1,8])

                with col1:
                    st.button("📋", key=f"copy_{idx}")

                with col2:
                    st.button("🔄", key=f"retry_{idx}")

                with col3:
                    st.button("👍", key=f"like_{idx}")

    # =====================================================
    # INPUT
    # =====================================================
    prompt = st.chat_input("Ask anything...")

    # =====================================================
    # MIC RECORDER
    # =====================================================
    st.markdown('<div class="mic-wrapper">', unsafe_allow_html=True)

    audio = mic_recorder(
        start_prompt="🎤",
        stop_prompt="⏹️",
        just_once=True,
        key=f"mic_{len(st.session_state.history)}"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # =====================================================
    # HANDLE TEXT
    # =====================================================
    if prompt:

        send_message(prompt)

    # =====================================================
    # HANDLE AUDIO
    # =====================================================
    if audio:

        with open("temp_audio.webm", "wb") as f:
            f.write(audio["bytes"])

        text = st.session_state.voice.speech_to_text_from_audio(
            "temp_audio.webm"
        )

        if text:
            send_message(text)

# =========================================================
# RUN APP
# =========================================================
if __name__ == "__main__":
    main()