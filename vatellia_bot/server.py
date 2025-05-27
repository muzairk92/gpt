import os
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

from .database import save_lead
from .agent import chat

app = FastAPI(title="Vatellia AI Agent")


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    name: str = ""
    email: str = ""
    phone: str = ""
    requirements: str = ""


@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    messages = [m.dict() for m in req.messages]
    try:
        answer = chat(messages)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    if req.email:
        save_lead(req.name, req.email, req.phone, req.requirements)
    return {"answer": answer}


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("vatellia_bot.server:app", host=host, port=port, reload=True)
