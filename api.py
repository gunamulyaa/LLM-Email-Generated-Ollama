from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import ask

app = FastAPI(title="Internal Email Chatbot API")

class Question(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "API hidup"}

@app.post("/chat")
def chat(data: Question):
    return {
        "question": data.question,
        "answer": ask(data.question)
    }
