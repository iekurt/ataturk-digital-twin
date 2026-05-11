from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
import json

from engine.cognition import (
    PRINCIPLES,
    TIMELINE,
    vicdan_check
)

from engine.llm import ask_llm, stream_llm, text_to_speech

try:
    from engine.memory import get_memory, clear_memory
except Exception:
    def get_memory(session_id: str):
        return []

    def clear_memory(session_id: str):
        return None


app = FastAPI(
    title="Atatürk Digital Twin",
    version="1.2",
    description="Constitutional Cognition Engine powered by HOPEtensor, Vicdan Layer and OpenAI TTS"
)

app.mount("/static", StaticFiles(directory="static"), name="static")


class Question(BaseModel):
    question: str
    language: str = "tr"
    mode: str = "constitutional"


class SpeechRequest(BaseModel):
    text: str
    voice: str = "cedar"


@app.get("/", response_class=HTMLResponse)
def landing():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "project": "Atatürk Digital Twin",
        "version": "1.2",
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
        "version": "1.2",
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
            "version": "1.2",
            "mode": data.mode,
            "vicdan": vicdan
        }
        yield f"data: {json.dumps(meta, ensure_ascii=False)}\n\n"

        try:
            for chunk in stream_llm(data.question, data.mode):
                payload = {
                    "type": "token",
                    "token": chunk
                }
                yield f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"

            done = {
                "type": "done"
            }
            yield f"data: {json.dumps(done, ensure_ascii=False)}\n\n"

        except Exception as e:
            error = {
                "type": "error",
                "message": str(e)
            }
            yield f"data: {json.dumps(error, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )


@app.post("/tts")
def tts(data: SpeechRequest):
    audio_bytes = text_to_speech(
        text=data.text,
        voice=data.voice
    )

    return Response(
        content=audio_bytes,
        media_type="audio/mpeg",
        headers={
            "Content-Disposition": "inline; filename=ataturk-digital-twin-voice.mp3"
        }
    )


@app.post("/vicdan")
def vicdan(data: Question):
    return {
        "success": True,
        "engine": "digital-vicdan",
        "version": "1.2",
        "input": data.question,
        "review": vicdan_check(data.question)
    }


@app.post("/reason")
def reason(data: Question):
    return demo(data)