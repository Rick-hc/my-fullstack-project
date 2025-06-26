# backend/api.py
from fastapi import FastAPI
from pydantic import BaseModel
from runRag import ask_rag  # runRag.py に ask_rag(question: str) → str が定義されている想定

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

app = FastAPI()

# CORS 設定（React dev サーバー向け）
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    answer = ask_rag(req.question)
    return ChatResponse(answer=answer)
