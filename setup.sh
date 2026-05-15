#!/bin/bash

# AI Assistant Quick Setup Script
# This script automates the initial setup process

set -e

echo "================================"
echo "AI Assistant Setup Script"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your GEMINI_API_KEY"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Verify imports
echo "Verifying installation..."
python -c "from src.llm_service import LLMService; print('✅ LLM Service OK')"
python -c "from src.voice_service import VoiceService; print('✅ Voice Service OK')"
python -c "from src.memory import ConversationMemory; print('✅ Memory Service OK')"
python -c "import streamlit; print('✅ Streamlit OK')"
echo ""

echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Google Gemini API key"
echo "2. Run: streamlit run app.py"
echo "3. Open http://localhost:8501 in your browser"
echo ""
