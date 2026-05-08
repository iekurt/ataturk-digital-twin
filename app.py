from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Ataturk Digital Twin",
    version="0.1"
)

class Question(BaseModel):
    question: str

@app.get("/")
def root():
    return {
        "project": "Ataturk Digital Twin",
        "status": "running",
        "layer": "constitutional cognition"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/demo")
def demo(data: Question):

    response = f"""
Atatürk Digital Twin Response

Question:
{data.question}

Constitutional Perspective:
A civilization survives through science,
reason,
education,
and ethical sovereignty.
"""

    return {
        "success": True,
        "response": response
    }