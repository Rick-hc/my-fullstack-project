from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .ragPromptBuilder import generate_query
from .search_embeddings import chunk_search
from .qa_utils import get_answer

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

class QueryItem(BaseModel):
    id: str
    q: str
    score: float

class QueryResponse(BaseModel):
    items: list[QueryItem]

class AnswerRequest(BaseModel):
    chunk_id: str
    question: str

class AnswerResponse(BaseModel):
    answer: str

@app.post("/api/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    q1 = generate_query(req.question)
    items = chunk_search(q1, top_k=5)
    return {"items": items}

@app.post("/api/answer", response_model=AnswerResponse)
async def answer_endpoint(req: AnswerRequest):
    answer = get_answer(req.chunk_id)
    return {"answer": answer}
