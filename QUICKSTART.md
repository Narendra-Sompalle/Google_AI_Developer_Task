# Quickstart Guide

Follow these steps to quickly set up and run the AI Assistant application.

## Prerequisites
- Python 3.8 or higher
- Virtual environment tool (e.g., `venv`)
- Internet connection for API access

## Setup
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd GenAI_task
   ```

2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Create a `.env` file in the project root.
   - Add the following variables:
     ```env
     GEMINI_API_KEY=<your-api-key>
     APP_NAME=AI Assistant
     MAX_CONVERSATION_MEMORY=3
     TEMPERATURE=0.7
     MAX_TOKENS=1024
     ```

## Running the Application
1. Start the Streamlit server:
   ```bash
   streamlit run app.py
   ```
2. Open the application in your browser (default: `http://localhost:8501`).

## Troubleshooting
- Ensure all dependencies are installed.
- Verify environment variables are correctly set.
- Check logs for errors using the logging utility.
