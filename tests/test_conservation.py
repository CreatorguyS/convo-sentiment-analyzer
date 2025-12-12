# tests/test_conversation.py
from src.chatbot.conversation_manager import ConversationManager

def test_conversation_basic():
    mgr = ConversationManager()
    mgr.start_new_conversation()
    mgr.add_user_message("hello")
    mgr.add_bot_message("hi")
    history = mgr.get_conversation_history()
    assert isinstance(history, list)
    assert history[-1]['message_count'] >= 2
