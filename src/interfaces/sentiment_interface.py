# src/interfaces/sentiment_interface.py
from typing import List, Protocol

class SentimentInterface(Protocol):
    def analyze_statement(self, text: str):
        ...

    def analyze_conversation(self, texts: List[str]):
        ...
