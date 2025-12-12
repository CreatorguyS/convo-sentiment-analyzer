# src/chatbot/conversation_manager.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any
import uuid

@dataclass
class Message:
    id: str
    role: str
    content: str
    timestamp: str
    sentiment: Dict[str, Any] = None
    cleaned: str = None

    def to_dict(self):
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
            "cleaned": self.cleaned,
            "timestamp": self.timestamp,
            "sentiment": self.sentiment
        }

@dataclass
class Conversation:
    id: str
    start_time: str
    messages: List[Message] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_message(self, role: str, content: str, cleaned: str = None, sentiment: Dict = None):
        msg = Message(
            id=str(uuid.uuid4()),
            role=role,
            content=content,
            cleaned=cleaned,
            timestamp=datetime.now().isoformat(),
            sentiment=sentiment
        )
        self.messages.append(msg)
        return msg

    def get_user_messages(self):
        return [m.content if m.role == 'user' else None for m in self.messages if m.role == 'user']

    def get_user_cleaned_messages(self):
        return [m.cleaned for m in self.messages if m.role == 'user']

    def to_dict(self):
        return {
            "id": self.id,
            "start_time": self.start_time,
            "message_count": len(self.messages),
            "messages": [m.to_dict() for m in self.messages]
        }

class ConversationManager:
    def __init__(self):
        self.conversations: Dict[str, Conversation] = {}
        self.current_conversation: Conversation = None

    def start_new_conversation(self):
        cid = str(uuid.uuid4())
        conv = Conversation(id=cid, start_time=datetime.now().isoformat())
        self.conversations[cid] = conv
        self.current_conversation = conv
        return conv

    def add_user_message(self, content: str, cleaned: str = None, sentiment: Dict = None):
        if not self.current_conversation:
            self.start_new_conversation()
        return self.current_conversation.add_message('user', content, cleaned, sentiment)

    def add_bot_message(self, content: str):
        if not self.current_conversation:
            raise ValueError("No active conversation")
        return self.current_conversation.add_message('bot', content)

    def end_current_conversation(self):
        self.current_conversation = None

    def get_conversation_history(self):
        return [c.to_dict() for c in self.conversations.values()]
