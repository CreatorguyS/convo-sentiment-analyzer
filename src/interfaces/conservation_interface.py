# src/interfaces/conversation_interface.py
from typing import Protocol

class ConversationInterface(Protocol):
    def add_user_message(self, content: str):
        ...
    def add_bot_message(self, content: str):
        ...
