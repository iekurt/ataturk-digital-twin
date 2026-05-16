from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Constitutional Cognition Engine")

class AskRequest(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(req: AskRequest):
    return {
        "answer": "MVP placeholder: transparent constitutional reasoning response.",
        "question": req.question,
        "doctrine": [
            "Peace at home.",
            "Peace in the world.",
            "Peace in the universe and HOPEverse."
        ],
        "trace": {
            "retrieval": "pending",
            "timeline": "pending",
            "principle_graph": "pending",
            "ethics": "pending",
            "confidence": "pending"
        }
    }
