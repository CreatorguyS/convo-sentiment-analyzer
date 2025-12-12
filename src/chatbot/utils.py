"""
Utility functions used ONLY inside the chatbot layer.
This file is intentionally lightweight so it does not conflict
with global utils in src/utils/.
"""

import random


# ---------------------------
# Sentiment Emoji Mapping
# ---------------------------
SENTIMENT_EMOJI = {
    "positive": "😊",
    "negative": "😞",
    "neutral": "😐",
}


def sentiment_to_emoji(label: str) -> str:
    """
    Convert a sentiment label to emoji.
    Safe even if label is unexpected.
    """
    if not isinstance(label, str):
        return "❓"
    return SENTIMENT_EMOJI.get(label.lower(), "❓")


# ---------------------------
# Intent Detection Helpers
# ---------------------------
def detect_basic_intent(message: str) -> str:
    """
    Very lightweight fallback intent detection.
    ResponseGenerator may already do heavy intent logic.
    This helper exists so chatbot layer never breaks.
    """
    msg = message.lower()

    if any(x in msg for x in ["hello", "hi", "hey"]):
        return "greeting"

    if any(x in msg for x in ["bye", "goodbye"]):
        return "farewell"

    if any(x in msg for x in ["help", "support", "assist"]):
        return "help"

    if any(x in msg for x in ["issue", "problem", "not working", "broken"]):
        return "complaint"

    return "general"


# ---------------------------
# Response Helpers
# ---------------------------
def choose_response(templates: list, fallback: str = "How can I assist you?") -> str:
    """
    Pick a safe random response. Ensures no crash on empty list.
    """
    if not templates:
        return fallback
    return random.choice(templates)


def ensure_period(text: str) -> str:
    """
    Makes sure bot responses end with punctuation.
    This keeps output clean but does NOT affect pipeline.
    """
    if not text:
        return ""
    if text.endswith((".", "!", "?")):
        return text
    return text + "."


__all__ = [
    "sentiment_to_emoji",
    "detect_basic_intent",
    "choose_response",
    "ensure_period",
]
