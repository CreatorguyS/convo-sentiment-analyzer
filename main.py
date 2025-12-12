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

def emoji(label):
    return {"positive":"😊","negative":"😞","neutral":"😐"}.get(label,"❓")

def print_overall(overall):
    print("\n================ Conversation Summary ================\n")
    print(f"Overall Sentiment: {overall['label'].title()} {emoji(overall['label'])}")
    print(f"Confidence: {overall['confidence']:.2f}")
    print(f"Meaning: {overall['description']}\n")

def print_mood(mood):
    print("Mood Analysis:")
    print("──────────────────────")
    print(f"Trend: {mood['trend'].title()}")
    print(f"Significant Shift: {'Yes' if mood['significant_shift'] else 'No'}")
    print()

def main():
    setup_logging()
    bot = Chatbot()
    print_banner()
    print("Bot: Hello! I'm Leoplus Assistant. How can I help?\n")

    while True:
        try:
            user = input("You: ").strip()
            if not user:
                continue

            if user.lower() in ("quit", "exit", "bye"):
                result = bot.end_conversation()
                if result.get("success"):
                    print_overall(result["overall_sentiment"])
                    print_mood(result["mood_analysis"])
                break

            res = bot.process_message(user)

            if res.get("success"):
                s = res["statement_sentiment"]
                print(f"→ Sentiment: {s['label'].title()} {emoji(s['label'])} (confidence: {s['confidence']:.2f})")
                print(f"Bot: {res['bot_response']}\n")
            else:
                print("Bot Error:", res.get("error"))

        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

if __name__ == "__main__":
    main()
