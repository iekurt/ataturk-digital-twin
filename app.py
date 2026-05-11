from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime

from engine.cognition import (
    PRINCIPLES,
    TIMELINE,
    vicdan_check
)

from engine.llm import ask_llm

app = FastAPI(
    title="Atatürk Digital Twin",
    version="0.6",
    description="Constitutional Cognition Engine powered by HOPEtensor and Vicdan Layer"
)

app.mount("/static", StaticFiles(directory="static"), name="static")


class Question(BaseModel):
    question: str
    language: str = "en"
    mode: str = "constitutional"


@app.get("/", response_class=HTMLResponse)
def landing():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "project": "Atatürk Digital Twin",
        "version": "0.6",
        "time": datetime.utcnow().isoformat()
    }


@app.get("/timeline")
def timeline():
    return {
        "project": "Atatürk Digital Twin",
        "timeline": TIMELINE
    }


@app.get("/principles")
def principles():
    return {
        "project": "Atatürk Digital Twin",
        "principles": PRINCIPLES
    }


@app.post("/demo")
def demo(data: Question):

    vicdan = vicdan_check(data.question)

    response = ask_llm(
        question=data.question,
        mode=data.mode
    )

    return {
        "success": True,
        "engine": "constitutional-cognition-engine",
        "version": "0.6",
        "mode": data.mode,
        "principles": PRINCIPLES,
        "timeline": TIMELINE,
        "vicdan": vicdan,
        "response": response
    }


@app.post("/vicdan")
def vicdan(data: Question):
    return {
        "success": True,
        "engine": "digital-vicdan",
        "version": "0.6",
        "input": data.question,
        "review": vicdan_check(data.question)
    }


@app.post("/reason")
def reason(data: Question):
    return demo(data)