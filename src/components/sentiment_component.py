# src/components/sentiment_component.py
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except Exception:
    TRANSFORMERS_AVAILABLE = False

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except Exception:
    VADER_AVAILABLE = False

class SentimentResult:
    def __init__(self, label: str, confidence: float, scores: Dict):
        self.label = label
        self.confidence = confidence
        self.scores = scores

class SentimentComponent:
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english", use_transformers=False):
        self.model_name = model_name
        self.pipeline = None
        self.vader = None
        self.use_transformers = use_transformers and TRANSFORMERS_AVAILABLE
        if self.use_transformers:
            try:
                self.pipeline = pipeline("sentiment-analysis", model=self.model_name, return_all_scores=True)
                logger.info("Loaded transformers sentiment pipeline")
            except Exception as e:
                logger.warning("Could not load transformers pipeline: %s", e)
                self.pipeline = None
        if not self.pipeline and VADER_AVAILABLE:
            self.vader = SentimentIntensityAnalyzer()
            logger.info("Using VADER sentiment analyzer")

    def analyze_statement(self, text: str) -> SentimentResult:
        if not text:
            return SentimentResult("neutral", 0.5, {"neutral":1.0})
        if self.pipeline:
            try:
                res = self.pipeline(text)[0]  # list of dicts
                scores = {d['label'].lower(): d['score'] for d in res}
                if 'positive' in scores and scores['positive'] > scores.get('negative', 0):
                    return SentimentResult("positive", float(scores['positive']), scores)
                elif 'negative' in scores and scores['negative'] > scores.get('positive', 0):
                    return SentimentResult("negative", float(scores['negative']), scores)
                else:
                    return SentimentResult("neutral", 0.5, scores)
            except Exception as e:
                logger.warning("Transformers pipeline failed: %s", e)
        if self.vader:
            s = self.vader.polarity_scores(text)
            comp = s.get("compound", 0.0)
            if comp >= 0.05:
                return SentimentResult("positive", float(s.get("pos", comp)), s)
            elif comp <= -0.05:
                return SentimentResult("negative", float(s.get("neg", abs(comp))), s)
            else:
                return SentimentResult("neutral", float(s.get("neu", 0.5)), s)
        # simple keyword fallback
        text_l = text.lower()
        positive_words = ['good','great','excellent','love','nice','helpful','happy']
        negative_words = ['bad','terrible','awful','hate','disappoint','worst','rude']
        pos = sum(1 for w in positive_words if w in text_l)
        neg = sum(1 for w in negative_words if w in text_l)
        if pos > neg:
            return SentimentResult("positive", min(0.7, pos/len(positive_words)), {"pos":pos,"neg":neg})
        elif neg > pos:
            return SentimentResult("negative", min(0.7, neg/len(negative_words)), {"pos":pos,"neg":neg})
        else:
            return SentimentResult("neutral", 0.5, {})
    def analyze_conversation(self, statements: List[str]):
        if not statements:
            return SentimentResult("neutral", 0.5, {})
        vals = []
        weights = []
        for s in statements:
            r = self.analyze_statement(s)
            if r.label == "positive":
                v = r.confidence
            elif r.label == "negative":
                v = -r.confidence
            else:
                v = 0.0
            w = max(1.0, len(s.split()))
            vals.append(v)
            weights.append(w)
        import numpy as np
        if sum(weights) == 0:
            avg = 0.0
        else:
            avg = float(np.average(vals, weights=weights))
        if avg >= 0.1:
            overall = "positive"
        elif avg <= -0.1:
            overall = "negative"
        else:
            overall = "neutral"
        return SentimentResult(overall, abs(avg), {"weighted_avg": avg})
