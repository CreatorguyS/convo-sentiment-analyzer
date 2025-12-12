# src/components/text_cleaner.py
import re
import html
from typing import List

_CONTRACTIONS = {
    "ain't": "is not", "aren't": "are not", "can't": "cannot",
    "couldn't": "could not", "didn't": "did not", "doesn't": "does not",
    "don't": "do not", "i'm": "i am", "i've": "i have", "i'll": "i will",
    "isn't": "is not", "it's": "it is", "let's": "let us", "she's": "she is",
    "he's": "he is", "that's": "that is", "there's": "there is", "they're": "they are",
    "we're": "we are", "won't": "will not", "wouldn't": "would not", "you're": "you are",
    "you've": "you have", "could've": "could have",
}

_SLANG = {
    "u": "you", "ur": "your", "pls": "please", "plz": "please",
    "thx": "thanks", "ty": "thanks", "idk": "i do not know",
    "imo": "in my opinion", "btw": "by the way",
}

_EMOJI_MAP = {
    "😊": "smiley", "😞": "sad", "😐": "neutral", "😂": "laugh", "😡": "angry",
    "👍": "thumbs_up", "👎": "thumbs_down", "❤️": "love", "💔": "broken_heart",
}

_NEGATIONS = {
    "not", "no", "never", "none", "cannot", "can't", "don't",
    "didn't", "won't", "wouldn't", "isn't", "aren't", "ain't",
}

URL_RE = re.compile(r"https?://\S+|www\.\S+")
EMAIL_RE = re.compile(r"\S+@\S+")
PHONE_RE = re.compile(r"\+?\d[\d\-\s]{7,}\d")
HTML_TAG_RE = re.compile(r"<.*?>")
MULTI_PUNCT_RE = re.compile(r"([!?.,]){2,}")
ELONG_RE = re.compile(r"(.)\1{2,}", re.DOTALL)
NON_PRINTABLE_RE = re.compile(r"[\x00-\x1f\x7f-\x9f]")
TOKEN_SPLIT_RE = re.compile(r"\s+")
WORD_RE = re.compile(r"[A-Za-z0-9_]+(?:'[A-Za-z0-9_]+)?|[^\s]")

class TextCleaner:
    def __init__(self, contractions=None, slang_map=None, emoji_map=None, negation_set=None, max_elongation=2):
        self.contractions = contractions or _CONTRACTIONS
        self.slang_map = slang_map or _SLANG
        self.emoji_map = emoji_map or _EMOJI_MAP
        self.negation_set = negation_set or _NEGATIONS
        self.max_elongation = max_elongation

    def clean(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return ""
        text = html.unescape(text)
        text = HTML_TAG_RE.sub(" ", text)
        text = URL_RE.sub(" ", text)
        text = EMAIL_RE.sub(" ", text)
        text = PHONE_RE.sub(" ", text)
        text = NON_PRINTABLE_RE.sub(" ", text)
        text = text.strip()
        text = text.lower()
        for emo, emo_word in self.emoji_map.items():
            if emo in text:
                text = text.replace(emo, f" {emo_word} ")
        text = self._expand_contractions(text)
        text = self._replace_slang(text)
        text = self._normalize_elongations(text)
        text = MULTI_PUNCT_RE.sub(r"\1", text)
        text = self._mark_negations(text)
        text = re.sub(r"[^0-9a-zA-Z\s\.,!?'\-_:;]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def tokenize(self, text: str) -> List[str]:
        if not text:
            return []
        return WORD_RE.findall(text)

    def _expand_contractions(self, text: str) -> str:
        for contr in sorted(self.contractions.keys(), key=lambda s: -len(s)):
            pattern = r"\b" + re.escape(contr) + r"\b"
            repl = self.contractions[contr]
            text = re.sub(pattern, repl, text)
        return text

    def _replace_slang(self, text: str) -> str:
        for slang, full in self.slang_map.items():
            pattern = r"\b" + re.escape(slang) + r"\b"
            text = re.sub(pattern, full, text)
        return text

    def _normalize_elongations(self, text: str) -> str:
        def _repl(m):
            ch = m.group(1)
            return ch * self.max_elongation
        return ELONG_RE.sub(_repl, text)

    def _mark_negations(self, text: str) -> str:
        tokens = TOKEN_SPLIT_RE.split(text)
        out_tokens = []
        negating = False
        neg_scope = 0
        MAX_NEG_SCOPE = 8
        for tok in tokens:
            if not tok:
                continue
            stripped = tok.strip()
            if any(p in stripped for p in ".!?," ):
                if negating and stripped not in self.negation_set:
                    if re.search(r"[A-Za-z0-9]", stripped):
                        out_tokens.append("NOT_" + stripped)
                    else:
                        out_tokens.append(stripped)
                else:
                    out_tokens.append(stripped)
                negating = False
                neg_scope = 0
                continue
            low = stripped.lower()
            if low in self.negation_set:
                negating = True
                neg_scope = 0
                out_tokens.append(low)
                continue
            if negating and neg_scope < MAX_NEG_SCOPE:
                out_tokens.append("NOT_" + stripped)
                neg_scope += 1
            else:
                out_tokens.append(stripped)
        return " ".join(out_tokens)

if __name__ == "__main__":
    cleaner = TextCleaner()
    examples = [
        "I don't like this at all!!!",
        "This is soooo goooood 😊😊!!!",
        "Worst. service. ever. I won't use it again.",
        "u r amazing!! thx",
        "Visit https://example.com or mail me at me@ex.com"
    ]
    for ex in examples:
        print("ORIG:", ex)
        print("CLEAN:", cleaner.clean(ex))
        print("TOKENS:", cleaner.tokenize(cleaner.clean(ex)))
        print("---")
