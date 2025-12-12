# src/services/sentiment_service.py
from typing import List
from src.components.sentiment_component import SentimentComponent, SentimentResult
import logging

logger = logging.getLogger(__name__)

class SentimentService:
    def __init__(self, use_transformers=False):
        self.component = SentimentComponent(use_transformers=use_transformers)

    def analyze_statement(self, text: str) -> SentimentResult:
        return self.component.analyze_statement(text)

    def analyze_conversation(self, texts: List[str]) -> SentimentResult:
        return self.component.analyze_conversation(texts)

    def detect_mood_shifts(self, texts: List[str]):
        vals = []
        for t in texts:
            r = self.analyze_statement(t)
            if r.label == 'positive':
                vals.append(r.confidence)
            elif r.label == 'negative':
                vals.append(-r.confidence)
            else:
                vals.append(0.0)
        # simple trend detection
        if len(vals) < 2:
            return {"trend":"stable", "volatility":0.0, "details": vals}
        trend = "improving" if vals[-1] > vals[0] else "worsening"
        import numpy as np
        return {"trend":trend, "volatility": float(np.std(vals)), "values": vals}
