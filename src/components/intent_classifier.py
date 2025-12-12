class IntentClassifier:
    """
    Lightweight rule-based NLU component.
    Maps keywords → intents.
    Easy to extend and fully explainable (great for assignments).
    """

    def __init__(self):
        self.intent_map = {
            "refund": ["refund", "money back", "return"],
            "delivery_issue": ["late", "delay", "package", "not delivered", "missing", "arrive"],
            "account_issue": ["login", "password", "account", "access"],
            "technical_issue": ["error", "bug", "crash", "not working", "issue", "problem"],
            "billing_issue": ["charge", "billing", "invoice", "payment", "bill"],
            "greeting": ["hi", "hello", "hey", "greetings"],
            "farewell": ["bye", "goodbye", "thanks", "thank you"],
        }

    def classify(self, text: str) -> str:
        text = text.lower()

        for intent, keywords in self.intent_map.items():
            if any(word in text for word in keywords):
                return intent

        return "general"
