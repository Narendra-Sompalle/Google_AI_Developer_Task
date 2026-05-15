"""
Memory management module for maintaining conversation context.
Stores and retrieves conversation history.
"""

from typing import List, Dict, Optional
from datetime import datetime


class ConversationMemory:
    """
    Manages conversation history with configurable memory length.
    Stores recent interactions for context awareness.
    """
    
    def __init__(self, max_memory: int = 3):
        """
        Initialize the conversation memory.
        
        Args:
            max_memory (int): Maximum number of interactions to store.
        """
        self.max_memory = max_memory
        self.interactions: List[Dict] = []
    
    def add_interaction(self, user_message: str, assistant_response: str) -> None:
        """
        Add a user-assistant interaction pair to memory.
        
        Args:
            user_message (str): The user's input message.
            assistant_response (str): The assistant's response.
        """
        interaction = {
            'user': user_message,
            'assistant': assistant_response,
            'timestamp': datetime.now().isoformat()
        }
        
        self.interactions.append(interaction)
        
        # Keep only the last max_memory interactions
        if len(self.interactions) > self.max_memory:
            self.interactions = self.interactions[-self.max_memory:]
    
    def get_memory_context(self) -> List[Dict] :
        """
        Get the current memory context for the LLM.
        
        Returns:
            List[Dict]: List of interaction dictionaries.
        """
        return self.interactions
    
    def get_memory_text(self) -> str:
        """
        Format memory as text for context window.
        
        Returns:
            str: Formatted conversation history.
        """
        if not self.interactions:
            return ""
        
        context_text = "Previous conversation context:\n"
        for i, interaction in enumerate(self.interactions, 1):
            context_text += f"\nInteraction {i}:\n"
            context_text += f"User: {interaction['user']}\n"
            context_text += f"Assistant: {interaction['assistant']}\n"
        
        return context_text
    
    def clear_memory(self) -> None:
        """Clear all stored interactions."""
        self.interactions = []
    
    def get_interaction_count(self) -> int:
        """
        Get the number of stored interactions.
        
        Returns:
            int: Number of interactions in memory.
        """
        return len(self.interactions)
