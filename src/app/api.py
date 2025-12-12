# src/app/api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.utils.logger import setup_logging
from src.chatbot.chatbot import Chatbot

setup_logging()
app = FastAPI(title="Leoplus Sentiment Chatbot API")
chatbot = Chatbot()

class ChatRequest(BaseModel):
    message: str

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/chat")
def chat(req: ChatRequest):
    res = chatbot.process_message(req.message)
    if not res.get('success'):
        raise HTTPException(status_code=500, detail=res.get('error','processing error'))
    return res

@app.post("/end")
def end():
    res = chatbot.end_conversation()
    return res
