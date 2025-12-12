# src/analytics/mood_shift_detector.py
from typing import List, Dict

def detect_mood_shifts(sentiments: List[float]) -> Dict:
    if not sentiments:
        return {"trend":"stable","volatility":0.0,"has_shift":False}
    if len(sentiments) < 2:
        return {"trend":"stable","volatility":0.0,"has_shift":False}
    import numpy as np
    trend = "improving" if sentiments[-1] > sentiments[0] else "worsening"
    volatility = float(np.std(sentiments))
    has_shift = abs(sentiments[-1] - sentiments[0]) > 0.3
    return {"trend":trend,"volatility":volatility,"has_shift":has_shift}
