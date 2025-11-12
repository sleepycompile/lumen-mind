from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

from .inference import generate, load_model

app = FastAPI(title="Bloomed Terminal", version="0.1.0")

class Message(BaseModel):
    role: str  # "system" | "user" | "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    max_new_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    stop: Optional[List[str]] = None

class ChatResponse(BaseModel):
    content: str

@app.on_event("startup")
def warmup():
    load_model()

@app.post("/v1/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    text = generate(
        [m.model_dump() for m in req.messages],
        max_new_tokens=req.max_new_tokens,
        temperature=req.temperature,
        top_p=req.top_p,
        stop=req.stop,
    )
    return ChatResponse(content=text)
