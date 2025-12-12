# src/repository/conversation_repository.py
import json
import os
from typing import Dict
from pathlib import Path

class ConversationRepository:
    def __init__(self, path: str = "data/conversations.jsonl"):
        self.path = Path(path)
        if not self.path.parent.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("")  # create empty file

    def save_conversation(self, conversation):
        # append JSON line
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(conversation.to_dict(), ensure_ascii=False) + "\n")

    def load_all(self):
        convs = []
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                convs.append(json.loads(line))
        return convs
