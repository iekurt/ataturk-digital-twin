from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict, Any
import asyncio
import json
import os

from engine.llm import ask_llm, stream_llm, text_to_speech
from engine.reflection import reflect_answer

APP_NAME = "ATATÜRK DIGITAL TWIN / HOPEVERSE"

DOCTRINE = [
    "Peace at home.",
    "Peace in the world.",
    "Peace in the universe and HOPEverse."
]

app = FastAPI(
    title=APP_NAME,
    version="1.3.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


class ReasonRequest(BaseModel):
    prompt: str | None = None
    question: str | None = None
    task: str | None = None
    reasoning_mode: str | None = "balanced"
    reasoningMode: str | None = None
    mode: str | None = None
    response_language: str | None = "tr"


class TTSRequest(BaseModel):
    text: str
    voice: str | None = "alloy"
    format: str | None = "mp3"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "project": APP_NAME,
            "doctrine": DOCTRINE
        }
    )


@app.get("/health")
async def health():
    return {
        "status": "online",
        "service": APP_NAME,
        "version": "1.3.0",
        "doctrine": DOCTRINE,
        "engine_available": True,
        "tts_available": True,
        "audit_available": True,
        "memory_available": True,
        "reflection_available": True,
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "pipeline": [
            "input",
            "session_memory_node",
            "reasoning_node",
            "vicdan_verification_node",
            "observer_audit_node",
            "self_reflection_node",
            "memory_writeback",
            "delivery"
        ]
    }


@app.post("/reason")
async def reason(payload: ReasonRequest):
    prompt = (
        payload.prompt
        or payload.question
        or payload.task
        or ""
    )

    reasoning_mode = (
        payload.reasoning_mode
        or payload.reasoningMode
        or payload.mode
        or "balanced"
    )

    answer = await ask_llm(
        prompt=prompt,
        reasoning_mode=reasoning_mode
    )

    reflection = reflect_answer(
        answer=answer,
        payload=payload.model_dump()
    )

    return {
        "status": "ok",
        "project": APP_NAME,
        "reasoning_mode": reasoning_mode,
        "answer": answer,
        "reflection": reflection,
        "doctrine": DOCTRINE
    }


@app.post("/stream")
async def stream(payload: ReasonRequest):
    prompt = (
        payload.prompt
        or payload.question
        or payload.task
        or ""
    )

    reasoning_mode = (
        payload.reasoning_mode
        or payload.reasoningMode
        or payload.mode
        or "balanced"
    )

    async def event_generator():
        final_answer = ""

        async for token in stream_llm(
            prompt=prompt,
            reasoning_mode=reasoning_mode
        ):
            final_answer += token

            yield f"data: {json.dumps({'token': token})}\n\n"

            await asyncio.sleep(0.001)

        reflection = reflect_answer(
            answer=final_answer,
            payload=payload.model_dump()
        )

        yield f"data: {json.dumps({'reflection': reflection})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )


@app.post("/tts")
async def tts(payload: TTSRequest):
    audio_bytes = await text_to_speech(
        text=payload.text,
        voice=payload.voice or "alloy"
    )

    return StreamingResponse(
        iter([audio_bytes]),
        media_type="audio/mpeg",
        headers={
            "Content-Disposition": "inline; filename=archive_voice.mp3"
        }
    )


@app.get("/memory/summary")
async def memory_summary():
    return {
        "status": "ok",
        "node": "session_memory_node",
        "memory_active": True,
        "memory_type": "session",
        "entries": 0
    }


@app.get("/audit/summary")
async def audit_summary():
    return {
        "status": "ok",
        "node": "observer_audit_node",
        "audit_active": True,
        "doctrine": DOCTRINE
    }


@app.get("/reflection/summary")
async def reflection_summary():
    sample = reflect_answer(
        answer="Cumhuriyet, bilim, etik ve barış temelinde ilerlemeliyiz.",
        payload={"reasoning_mode": "constitutional"}
    )

    return {
        "status": "ok",
        "reflection": sample
    }


@app.post("/v1/tasks")
async def tasks(payload: Dict[str, Any]):
    return {
        "status": "ok",
        "project": APP_NAME,
        "mode": payload.get("reasoning_mode", "balanced"),
        "message": "HOPEtensor task accepted.",
        "payload": payload
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
