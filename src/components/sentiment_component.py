from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentComponent:
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()

    def analyze_statement(self, text: str) -> dict:
        if not text:
            return {"label": "neutral", "confidence": 0.5, "scores": {}}

        scores = self.vader.polarity_scores(text)
        compound = scores["compound"]

        if compound >= 0.05:
            label = "positive"
            confidence = scores["pos"]
        elif compound <= -0.05:
            label = "negative"
            confidence = scores["neg"]
        else:
            label = "neutral"
            confidence = scores["neu"]

        return {
            "label": label,
            "confidence": round(confidence, 3),
            "scores": scores
        }

    def analyze_conversation(self, messages: list) -> dict:
        if not messages:
            return {"label": "neutral", "confidence": 0.5, "scores": {"compound": 0}}

        compounds = [self.vader.polarity_scores(m)["compound"] for m in messages]
        avg = sum(compounds) / len(compounds)

        if avg >= 0.05:
            label = "positive"
        elif avg <= -0.05:
            label = "negative"
        else:
            label = "neutral"

        return {
            "label": label,
            "confidence": round(abs(avg), 3),
            "scores": {"compound": avg}
        }

    def detect_mood_shift(self, messages: list) -> dict:
        if len(messages) < 2:
            return {"trend": "stable", "significant_shift": False}

        scores = [self.vader.polarity_scores(m)["compound"] for m in messages]
        trend = "improving" if scores[-1] > scores[0] else "worsening"
        significant = abs(scores[-1] - scores[0]) > 0.3

        return {
            "trend": trend,
            "significant_shift": significant
        }
