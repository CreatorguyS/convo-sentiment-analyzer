# src/chatbot/chatbot.py
from src.utils.formatters import format_sentiment_details
from src.components.text_cleaner import TextCleaner
from src.services.sentiment_service import SentimentService
from src.services.conversation_service import ConversationService
from src.chatbot.response_generator import ResponseGenerator
from src.utils.logger import setup_logging
from typing import Any, Dict
import logging

setup_logging()
logger = logging.getLogger(__name__)

class Chatbot:
    def __init__(self, name: str = "Leoplus Assistant"):
        self.name = name
        self.cleaner = TextCleaner()
        self.sentiment = SentimentService()
        self.conv_service = ConversationService()
        self.response_gen = ResponseGenerator()
        self.conv_service.start()

    def process_message(self, user_input: str) -> Dict[str, Any]:
        if not user_input or not isinstance(user_input, str):
            return {"success": False, "error": "Invalid input"}

        cleaned = self.cleaner.clean(user_input)
        if not cleaned:
            return {"success": False, "error": "Empty after cleaning"}

        # Tier 2: Per-statement sentiment analysis
        stmt_sent = self.sentiment.analyze_statement(cleaned)
        sentiment_meta = {
            "label": stmt_sent["label"],
            "confidence": stmt_sent["confidence"],
            "scores": stmt_sent["scores"]
        }

        # Save user message
        self.conv_service.add_user(user_input, cleaned=cleaned, sentiment=sentiment_meta)

        # Prepare history for NLU
        history = self.conv_service.manager.current_conversation.messages

        # Generate bot response
        bot_resp = self.response_gen.generate_response(
            cleaned,
            [m.to_dict() for m in history],
            stmt_sent["label"]
        )

        self.conv_service.add_bot(bot_resp)

        return {
            "success": True,
            "user_input": user_input,
            "bot_response": bot_resp,
            "statement_sentiment": {
                "label": stmt_sent["label"],
                "confidence": round(stmt_sent["confidence"], 3)
            }
        }

    def end_conversation(self) -> Dict[str, Any]:
        conv = self.conv_service.manager.current_conversation
        if not conv:
            return {"success": False, "error": "No active conversation"}

        # Gather filtered user messages
        cleaned_msgs = conv.get_user_cleaned_messages()

        # Overall sentiment (Tier 1)
        overall = self.sentiment.analyze_conversation(cleaned_msgs)

        # Mood analysis (Bonus)
        mood = self.sentiment.detect_mood_shifts(cleaned_msgs)

        # Persist
        self.conv_service.repo.save_conversation(conv)

        # Reset for next run
        self.conv_service.manager.start_new_conversation()

        # FINAL OUTPUT — No metadata, only main results
        return {
            "success": True,
            "overall_sentiment": {
                "label": overall["label"],
                "confidence": round(overall["confidence"], 3),
                "description": f"Overall emotional direction: {overall['label']}"
            },
            "mood_analysis": mood
        }

    def get_conversation_history(self):
        return self.conv_service.get_history()
