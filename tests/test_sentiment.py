# tests/test_sentiment.py

from src.components.sentiment_component import SentimentComponent

def test_vader_or_fallback():
    comp = SentimentComponent()

    # Positive sentence
    r1 = comp.analyze_statement("I love this product, it's great!")

    assert isinstance(r1, dict), "SentimentComponent must return a dict"
    assert r1["label"] in ("positive", "neutral", "negative"), "Invalid sentiment label"
    assert isinstance(r1["confidence"], float), "Confidence should be a float"

    # Negative sentence
    r2 = comp.analyze_statement("This is terrible and awful")

    assert isinstance(r2, dict)
    assert r2["label"] in ("positive", "neutral", "negative")
    assert isinstance(r2["confidence"], float)
