# tests/test_text_cleaner.py
from src.components.text_cleaner import TextCleaner

def test_basic_cleanup():
    cleaner = TextCleaner()
    s = "I don't like this soooo!!! 😊"
    cleaned = cleaner.clean(s)
    assert "do not" in cleaned or "dont" not in cleaned
    assert "smiley" in cleaned
    assert "NOT_" in cleaner._mark_negations("I don't like this") or "do not" in cleaned
