from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from raaag import ask_rag
import os

app = FastAPI(
    title="Financial RAG API",
    description="Conversational Financial Knowledge Assistant",
    version="1.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str


@app.post("/chat", response_model=AnswerResponse)
def chat(request: QuestionRequest):

    answer = ask_rag(request.question)

    return {"answer": answer}


# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/asset", StaticFiles(directory="asset"), name="asset")