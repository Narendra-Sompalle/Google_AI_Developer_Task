# AI Assistant

AI Assistant is a Streamlit-based application that integrates voice recognition, memory management, and a generative AI model to provide an interactive and intelligent assistant experience.

## Features
- **Voice Recognition**: Convert speech to text using `speech_recognition`.
- **Generative AI**: Interact with Google Gemini API for intelligent responses.
- **Memory Management**: Maintain conversation context for better interactions.
- **Customizable Configuration**: Easily adjust settings via environment variables.
- **User-Friendly Interface**: Built with Streamlit for a clean and interactive experience.

## Technologies Used
- **Streamlit**: For the web interface.
- **Google Gemini API**: For generative AI capabilities.
- **SpeechRecognition & gTTS**: For speech-to-text and text-to-speech functionalities.
- **Python**: Core programming language.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd GenAI_task
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Set up environment variables in a `.env` file (refer to `src/config.py` for required variables).
2. Run the application:
   ```bash
   streamlit run app.py
   ```

## License
This project is licensed under the MIT License.
