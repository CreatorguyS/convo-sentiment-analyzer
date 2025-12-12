#!/usr/bin/env python3
from src.utils.logger import setup_logging
from src.chatbot.chatbot import Chatbot


def print_banner():
    print("""
    ─────────────────────────────────────────────────────
           Leoplus AI - Sentiment Chatbot (CLI)
          Type 'quit' to end the conversation
    ─────────────────────────────────────────────────────
    """)


def print_sentiment_emoji(label: str) -> str:
    return {
        "positive": "😊",
        "negative": "😞",
        "neutral":  "😐"
    }.get(label, "❓")


def format_sentiment_line(label: str, confidence: float) -> str:
    """Formats per-message sentiment output."""
    emoji = print_sentiment_emoji(label)
    return f"{label.title()} {emoji} (confidence: {confidence:.2f})"


def format_overall_sentiment(overall: dict) -> str:
    """Formats final summary sentiment block."""
    label = overall.get("label", "unknown")
    confidence = overall.get("confidence", 0.0)

    # If description was not provided, fall back safely
    description = overall.get(
        "description",
        "No overall interpretation available"
    )

    emoji = print_sentiment_emoji(label)

    return (
        f"Overall Conversation Sentiment: {label.title()} {emoji}\n"
        f"Confidence: {confidence:.2f}\n"
        f"Meaning: {description}\n"
    )


def main():
    setup_logging()

    bot = Chatbot()

    print_banner()
    print("Bot: Hello! I'm Leoplus Assistant. How can I help?\n")

    while True:
        try:
            user_text = input("You: ").strip()
            if not user_text:
                continue

            # Exit / summary trigger
            if user_text.lower() in ("quit", "exit", "bye"):
                result = bot.end_conversation()

                if result.get("success"):
                    print("\n================ Conversation Summary ================\n")

                    # Format and print overall sentiment
                    summary = format_overall_sentiment(result["overall_sentiment"])
                    print(summary)

                    print("Full Conversation:")
                    print("──────────────────────────────────────")
                    print(result["full_conversation"])

                break

            # Normal message flow
            response = bot.process_message(user_text)

            if response.get("success"):
                bot_reply = response["bot_response"]
                sentiment = response["statement_sentiment"]

                sentiment_line = format_sentiment_line(
                    sentiment["label"],
                    sentiment["confidence"]
                )

                print(f"→ Sentiment: {sentiment_line}")
                print(f"Bot: {bot_reply}\n")

            else:
                print("Bot Error:", response.get("error"), "\n")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break


if __name__ == "__main__":
    main()
