# tests/test_sentiment.py
from src.components.sentiment_component import SentimentComponent

def test_vader_or_fallback():
    comp = SentimentComponent(use_transformers=False)
    r = comp.analyze_statement("I love this product, it's great!")
    assert r.label in ("positive","neutral","negative")
    r2 = comp.analyze_statement("This is terrible and awful")
    assert r2.label in ("negative","neutral","positive")
