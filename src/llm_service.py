"""
LLM Service module for Google Gemini API interactions.
"""

import google.generativeai as genai
from typing import Optional

from .config import Config
from .memory import ConversationMemory


class LLMService:
    """
    Service class for interacting with Google Gemini API.
    """

    def __init__(
        self,
        api_key: str,
        memory: Optional[ConversationMemory] = None
    ):

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set."
            )

        self.api_key = api_key
        self.memory = memory or ConversationMemory()

        genai.configure(api_key=self.api_key)

        self.model = genai.GenerativeModel(
            Config.MODEL_NAME
        )

        self.generation_config = {
            "temperature": Config.TEMPERATURE,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": Config.MAX_TOKENS,
        }

    def generate_response(self, user_input: str) -> str:
        """
        Generate LLM response.
        """

        try:
            prompt = self._build_prompt(user_input)

            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )

            if response.text:
                return response.text

            return "I could not generate a response."

        except Exception as e:
            return f"Error generating response: {str(e)}"

    def _build_prompt(self, user_input: str) -> str:
        """
        Build prompt with memory context.
        """

        memory_context = self.memory.get_memory_text()

        if memory_context:
            prompt = f"""
{memory_context}

Current user message:
{user_input}

Provide a helpful response.
"""
        else:
            prompt = user_input

        return prompt

    def add_to_memory(
        self,
        user_message: str,
        assistant_response: str
    ) -> None:
        """
        Store conversation interaction.
        """

        self.memory.add_interaction(
            user_message,
            assistant_response
        )

    def get_memory(self) -> ConversationMemory:
        """
        Return memory object.
        """

        return self.memory

    def clear_memory(self) -> None:
        """
        Clear conversation memory.
        """

        self.memory.clear_memory()