# src/services/conversation_service.py
from src.chatbot.conversation_manager import ConversationManager
from src.repository.conversation_repository import ConversationRepository

class ConversationService:
    def __init__(self, repository: ConversationRepository = None):
        self.manager = ConversationManager()
        self.repo = repository or ConversationRepository()

    def start(self):
        return self.manager.start_new_conversation()

    def add_user(self, content, cleaned=None, sentiment=None):
        msg = self.manager.add_user_message(content, cleaned=cleaned, sentiment=sentiment)
        self.repo.save_conversation(self.manager.current_conversation)
        return msg

    def add_bot(self, content):
        msg = self.manager.add_bot_message(content)
        self.repo.save_conversation(self.manager.current_conversation)
        return msg

    def get_history(self):
        return self.manager.get_conversation_history()
