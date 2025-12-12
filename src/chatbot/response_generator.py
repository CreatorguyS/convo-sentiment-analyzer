# src/chatbot/response_generator.py

import random
from typing import List, Dict

from src.components.intent_classifier import IntentClassifier


class ResponseGenerator:
    """
    Generates context-aware responses based on:
    - Rule-Based NLU (intent classification)
    - Sentiment label (positive, neutral, negative)
    """

    def __init__(self):

        # Load rule-based NLU module
        self.intent_classifier = IntentClassifier()

        # Response templates for all supported intents
        self.response_templates = {

            "greeting": {
                "positive": [
                    "Hi! I'm happy to assist you today 😊",
                    "Hello! Great to see you — how can I help?"
                ],
                "neutral": [
                    "Hello! How can I help you today?",
                    "Hi. What can I do for you?"
                ],
                "negative": [
                    "Hello. I understand something is bothering you — I'm here to help.",
                    "Hey… I'm here to make things better. Tell me what's wrong."
                ]
            },

            "farewell": {
                "positive": [
                    "Thanks for chatting! Have a wonderful day! 🌟",
                    "Happy to help! Goodbye!"
                ],
                "neutral": [
                    "Goodbye.",
                    "Thank you."
                ],
                "negative": [
                    "I'm sorry things weren’t perfect today. We appreciate your feedback.",
                    "Thank you for telling us — we’ll work to improve."
                ]
            },

            "refund": {
                "positive": [
                    "Sure! I'd be happy to help with your refund. Could you share your order ID?",
                ],
                "neutral": [
                    "I can help you with the refund. Please provide your order ID.",
                ],
                "negative": [
                    "I understand you want a refund. I'm here to help — please share your order ID.",
                ]
            },

            "delivery_issue": {
                "positive": [
                    "Happy to help with your delivery concern — may I have your tracking ID?"
                ],
                "neutral": [
                    "I see there's a delivery issue. Could you share your tracking number?",
                ],
                "negative": [
                    "I'm sorry your package is delayed. Let me check it — can you share the order ID?",
                ]
            },

            "technical_issue": {
                "positive": [
                    "Great! Let's quickly sort out the technical issue. What's the exact problem?"
                ],
                "neutral": [
                    "I can help with this technical issue. What exactly is not working?",
                ],
                "negative": [
                    "I know technical issues can be frustrating — tell me what error you're seeing.",
                ]
            },

            "billing_issue": {
                "positive": [
                    "Sure! What billing detail would you like to verify?"
                ],
                "neutral": [
                    "I can help with billing queries. What seems incorrect?",
                ],
                "negative": [
                    "I'm sorry you're facing a billing issue — let me help. What's wrong exactly?",
                ]
            },

            "account_issue": {
                "positive": [
                    "Let's get your account issue solved! What error are you facing?"
                ],
                "neutral": [
                    "I can help with your account access. What seems to be the problem?",
                ],
                "negative": [
                    "I understand the frustration — let's fix your login issue. What error do you see?",
                ]
            },

            "general": {
                "positive": [
                    "That sounds great! How else can I help?",
                    "Happy to hear that — what would you like next?"
                ],
                "neutral": [
                    "I can help you with that. Could you please explain a bit more?",
                ],
                "negative": [
                    "I understand your concern — could you tell me more so I can assist?",
                ]
            },
        }

    # ----------------------------- MAIN LOGIC ------------------------------

    def generate_response(
        self,
        user_message: str,
        conversation_history: List[Dict],
        current_sentiment: str
    ) -> str:
        """
        Generates a response based on:
        1. Detected intent (via rule-based NLU)
        2. Sentiment of the latest user message
        """

        # 1. Classify intent using rule-based NLU
        intent = self.intent_classifier.classify(user_message)

        # 2. Resolve templates based on intent + sentiment
        templates = self.response_templates.get(intent, {}).get(current_sentiment)

        # Fallback to neutral tone
        if not templates:
            templates = self.response_templates.get(intent, {}).get("neutral", [])

        # Ultimate fallback (should never happen)
        if not templates:
            return "I'm here to help — could you tell me more?"

        # Randomly pick one template for natural variation
        return random.choice(templates)
