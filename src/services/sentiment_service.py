from src.components.sentiment_component import SentimentComponent

class SentimentService:
    """
    Wrapper around SentimentComponent.
    No transformer support (VADER-only).
    """

    def __init__(self):
        self.component = SentimentComponent()

    def analyze_statement(self, text: str):
        return self.component.analyze_statement(text)

    def analyze_conversation(self, messages: list):
        return self.component.analyze_conversation(messages)

    def detect_mood_shifts(self, messages: list):
        return self.component.detect_mood_shift(messages)
