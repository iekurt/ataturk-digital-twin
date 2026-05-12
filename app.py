import json
import os
from typing import Any, AsyncGenerator, Dict

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

try:
    from engine.llm import ask_llm, stream_llm, text_to_speech
except Exception as import_error:
    ask_llm = None
    stream_llm = None
    text_to_speech = None
    ENGINE_IMPORT_ERROR = str(import_error)
else:
    ENGINE_IMPORT_ERROR = None


app = FastAPI(
    title="ATATÜRK DIGITAL TWIN / HOPEVERSE",
    description="Constitutional cognition engine, HOPEtensor architecture, Vicdan layer, Streaming SSE, OpenAI TTS.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


DOCTRINE = [
    "Peace at home.",
    "Peace in the world.",
    "Peace in the universe and HOPEverse.",
]


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    prompt = (
        payload.get("prompt")
        or payload.get("question")
        or payload.get("task")
        or payload.get("message")
        or ""
    )

    reasoning_mode = (
        payload.get("reasoning_mode")
        or payload.get("reasoningMode")
        or payload.get("mode")
        or "balanced"
    )

    mode_instruction = payload.get("mode_instruction") or payload.get("modeInstruction") or ""

    return {
        **payload,
        "prompt": prompt,
        "question": prompt,
        "task": prompt,
        "reasoning_mode": reasoning_mode,
        "reasoningMode": reasoning_mode,
        "mode": reasoning_mode,
        "mode_instruction": mode_instruction,
        "project": payload.get("project", "ATATÜRK DIGITAL TWIN / HOPEVERSE"),
        "doctrine": payload.get("doctrine", DOCTRINE),
        "layer": payload.get("layer", "vicdan"),
        "architecture": payload.get("architecture", "HOPEtensor"),
    }


def fallback_answer(payload: Dict[str, Any]) -> str:
    prompt = payload.get("prompt", "")
    reasoning_mode = payload.get("reasoning_mode", "balanced")

    return f"""ATATÜRK DIGITAL TWIN / HOPEVERSE fallback cognition is active.

Reasoning Mode: {reasoning_mode}

Doctrine:
Peace at home.
Peace in the world.
Peace in the universe and HOPEverse.

Prompt:
{prompt}

Backend LLM engine is not fully available yet, but the constitutional cognition interface, Vicdan layer, HOPEtensor routing contract, streaming endpoint and health endpoint are operational."""


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

@app.get("/health")
async def health():
    return {
        "status": "online",
        "service": "ATATÜRK DIGITAL TWIN / HOPEVERSE",
        "doctrine": DOCTRINE,
        "engine_import_error": ENGINE_IMPORT_ERROR,
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
    }


@app.get("/api/health")
async def api_health():
    return await health()


@app.post("/reason")
async def reason(request: Request):
    payload = normalize_payload(await request.json())

    if ask_llm is None:
        return JSONResponse(
            {
                "status": "fallback",
                "answer": fallback_answer(payload),
                "reasoning_mode": payload["reasoning_mode"],
                "engine_import_error": ENGINE_IMPORT_ERROR,
            }
        )

    answer = await ask_llm(payload)

    return {
        "status": "ok",
        "answer": answer,
        "reasoning_mode": payload["reasoning_mode"],
    }


async def fallback_stream(payload: Dict[str, Any]) -> AsyncGenerator[str, None]:
    text = fallback_answer(payload)

    for word in text.split(" "):
        yield f"data: {json.dumps({'token': word + ' '})}\n\n"

    yield "data: [DONE]\n\n"


@app.post("/stream")
async def stream(request: Request):
    payload = normalize_payload(await request.json())

    async def event_generator():
        if stream_llm is None:
            async for chunk in fallback_stream(payload):
                yield chunk
            return

        try:
            async for token in stream_llm(payload):
                yield f"data: {json.dumps({'token': token})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as exc:
            error_text = f"\n\n[Stream fallback triggered: {str(exc)}]\n\n"
            yield f"data: {json.dumps({'token': error_text})}\n\n"
            async for chunk in fallback_stream(payload):
                yield chunk

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.post("/tts")
async def tts(request: Request):
    payload = await request.json()
    text = payload.get("text", "")
    voice = payload.get("voice", "alloy")

    if not text:
        return JSONResponse({"error": "No text provided"}, status_code=400)

    if text_to_speech is None:
        return JSONResponse(
            {
                "error": "TTS engine unavailable",
                "engine_import_error": ENGINE_IMPORT_ERROR,
            },
            status_code=503,
        )

    audio_bytes = await text_to_speech(text=text, voice=voice)

    return Response(
        content=audio_bytes,
        media_type="audio/mpeg",
        headers={"Content-Disposition": "inline; filename=hopeverse-voice.mp3"},
    )


@app.post("/v1/tasks")
async def tasks(request: Request):
    payload = normalize_payload(await request.json())

    if ask_llm is None:
        return {
            "status": "fallback",
            "mode": "v1-hybrid",
            "reasoning_mode": payload["reasoning_mode"],
            "local_llm_enabled": False,
            "answer": fallback_answer(payload),
            "engine_import_error": ENGINE_IMPORT_ERROR,
        }

    answer = await ask_llm(payload)

    return {
        "status": "ok",
        "mode": "v1-hybrid",
        "reasoning_mode": payload["reasoning_mode"],
        "local_llm_enabled": True,
        "answer": answer,
    }