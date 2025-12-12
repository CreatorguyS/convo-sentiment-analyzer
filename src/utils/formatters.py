"""
Formatting utilities for Leoplus Sentiment Chatbot.
These helpers format output for CLI, API response bodies,
conversation logs, and debugging.

NOTE:
This file is intentionally simple and independent.
It does not depend on any heavy libraries.
"""

from datetime import datetime


# ------------------------------
# TIMESTAMP FORMATTING
# ------------------------------
def format_timestamp(ts: datetime) -> str:
    """
    Convert datetime object to readable string.
    """
    if not isinstance(ts, datetime):
        return str(ts)
    return ts.strftime("%Y-%m-%d %H:%M:%S")


# ------------------------------
# SENTIMENT FORMATTERS
# ------------------------------
def format_sentiment(label: str, confidence: float) -> str:
    """
    Produce a clean formatted sentiment string.
    Example:
        Positive (85.2%)
    """
    try:
        pct = f"{confidence * 100:.1f}%"
    except:
        pct = "N/A"

    label_clean = label.title() if isinstance(label, str) else "Unknown"
    return f"{label_clean} ({pct})"


def format_sentiment_details(sentiment_dict: dict) -> str:
    """
    Takes a sentiment dictionary and prints a human-readable description.
    Example input:
        {
            "label": "positive",
            "confidence": 0.87,
            "scores": { "pos": 0.87, "neg": 0.03, "neu": 0.10 }
        }
    """
    if not sentiment_dict:
        return "No sentiment data"

    label = sentiment_dict.get("label", "unknown")
    conf = sentiment_dict.get("confidence", 0.0)

    score_str = ""
    scores = sentiment_dict.get("scores", {})
    if isinstance(scores, dict):
        parts = [f"{k}: {round(v, 3)}" for k, v in scores.items()]
        score_str = ", ".join(parts)

    return f"{format_sentiment(label, conf)} | Scores: {score_str}"


# ------------------------------
# CONVERSATION FORMATTERS
# ------------------------------
def format_message(role: str, content: str, timestamp=None, sentiment=None) -> str:
    """
    One-line message formatter for logs or CLI output.
    """
    ts = ""
    if timestamp:
        ts = f"[{format_timestamp(timestamp)}] "

    if role == "user":
        prefix = "User:"
    elif role == "bot":
        prefix = "Bot:"
    else:
        prefix = role.capitalize() + ":"

    base = f"{ts}{prefix} {content}"

    if sentiment:
        sent_str = format_sentiment_details(sentiment)
        return f"{base}\n    → {sent_str}"
    return base


def format_full_conversation(messages: list) -> str:
    """
    Join all messages into a formatted multiline string.
    Safe even if messages list is empty.
    """
    lines = []
    for msg in messages:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        ts = msg.get("timestamp")
        sentiment = msg.get("sentiment")

        lines.append(format_message(role, content, ts, sentiment))

    return "\n".join(lines)


__all__ = [
    "format_timestamp",
    "format_sentiment",
    "format_sentiment_details",
    "format_message",
    "format_full_conversation",
]
