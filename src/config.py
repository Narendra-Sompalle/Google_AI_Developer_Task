"""
Configuration module for the AI Assistant application.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration settings."""

    # API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    # Model Configuration
    MODEL_NAME = "gemini-2.5-flash"

    # Application Settings
    APP_NAME = os.getenv("APP_NAME", "AI Assistant")

    MAX_CONVERSATION_MEMORY = int(
        os.getenv("MAX_CONVERSATION_MEMORY", "3")
    )

    TEMPERATURE = float(
        os.getenv("TEMPERATURE", "0.7")
    )

    MAX_TOKENS = int(
        os.getenv("MAX_TOKENS", "1024")
    )

    # UI Settings
    PAGE_TITLE = "AI Powered Assistant"
    PAGE_LAYOUT = "wide"
    INITIAL_SIDEBAR_STATE = "expanded"

    @classmethod
    def validate_config(cls) -> bool:
        """
        Validate required configuration.
        """

        return bool(cls.GEMINI_API_KEY)


def get_config() -> Config:
    """
    Return application configuration.
    """

    return Config