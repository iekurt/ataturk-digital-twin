from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
import json
from engine.memory import get_memory, clear_memory


from engine.cognition import (
    PRINCIPLES,
    TIMELINE,
    vicdan_check
)

from engine.llm import ask_llm, stream_llm

app = FastAPI(
    title="Atatürk Digital Twin",
    version="0.8",
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
        "version": "0.8",
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

@app.get("/memory")
def memory():
    return {
        "session": "global",
        "memory": get_memory("global")
    }


@app.post("/memory/clear")
def memory_clear():

    clear_memory("global")

    return {
        "success": True,
        "message": "Conversation memory cleared."
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
        "version": "0.8",
        "mode": data.mode,
        "principles": PRINCIPLES,
        "timeline": TIMELINE,
        "vicdan": vicdan,
        "response": response
    }


@app.post("/stream")
def stream(data: Question):
    vicdan = vicdan_check(data.question)

    def event_generator():
        meta = {
            "type": "meta",
            "success": True,
            "engine": "constitutional-cognition-engine",
            "version": "0.8",
            "mode": data.mode,
            "vicdan": vicdan
        }
        yield f"data: {json.dumps(meta)}\n\n"

        try:
            for chunk in stream_llm(data.question, data.mode):
                payload = {
                    "type": "token",
                    "token": chunk
                }
                yield f"data: {json.dumps(payload)}\n\n"

            done = {
                "type": "done"
            }
            yield f"data: {json.dumps(done)}\n\n"

        except Exception as e:
            error = {
                "type": "error",
                "message": str(e)
            }
            yield f"data: {json.dumps(error)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )


@app.post("/vicdan")
def vicdan(data: Question):
    return {
        "success": True,
        "engine": "digital-vicdan",
        "version": "0.8",
        "input": data.question,
        "review": vicdan_check(data.question)
    }


@app.post("/reason")
def reason(data: Question):
    return demo(data)