import json
import os
from typing import Any, AsyncGenerator, Dict, List

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response, StreamingResponse
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

try:
    from engine.audit import audit_cognition, read_recent_audits, summarize_audits
except Exception as audit_import_error:
    audit_cognition = None
    read_recent_audits = None
    summarize_audits = None
    AUDIT_IMPORT_ERROR = str(audit_import_error)
else:
    AUDIT_IMPORT_ERROR = None

try:
    from engine.memory import save_turn, read_recent_memory, summarize_memory, clear_memory
except Exception as memory_import_error:
    save_turn = None
    read_recent_memory = None
    summarize_memory = None
    clear_memory = None
    MEMORY_IMPORT_ERROR = str(memory_import_error)
else:
    MEMORY_IMPORT_ERROR = None

try:
    from engine.reflection import reflect_answer
except Exception as reflection_import_error:
    reflect_answer = None
    REFLECTION_IMPORT_ERROR = str(reflection_import_error)
else:
    REFLECTION_IMPORT_ERROR = None


app = FastAPI(
    title="ATATÜRK DIGITAL TWIN / HOPEVERSE",
    description=(
        "Constitutional cognition engine, HOPEtensor architecture, Vicdan layer, "
        "Streaming SSE, OpenAI TTS, Session Memory Node, Observer Audit Node, "
        "Self-Reflection Node."
    ),
    version="1.3.1",
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

    reasoning_mode = str(reasoning_mode).strip().lower()

    return {
        **payload,
        "prompt": prompt,
        "question": prompt,
        "task": prompt,
        "reasoning_mode": reasoning_mode,
        "reasoningMode": reasoning_mode,
        "mode": reasoning_mode,
        "mode_instruction": payload.get("mode_instruction") or payload.get("modeInstruction") or "",
        "project": payload.get("project", "ATATÜRK DIGITAL TWIN / HOPEVERSE"),
        "doctrine": payload.get("doctrine", DOCTRINE),
        "layer": payload.get("layer", "vicdan"),
        "architecture": payload.get("architecture", "HOPEtensor"),
        "response_language": "Turkish",
        "must_answer_in_turkish": True,
    }


def fallback_answer(payload: Dict[str, Any]) -> str:
    prompt = payload.get("prompt", "")
    reasoning_mode = payload.get("reasoning_mode", "balanced")

    return f"""ATATÜRK DIGITAL TWIN / HOPEVERSE anayasal biliş arayüzü aktif.

Reasoning Mode: {reasoning_mode}

Merkez doktrin:
Peace at home.
Peace in the world.
Peace in the universe and HOPEverse.

Prompt:
{prompt}

LLM motoru geçici olarak fallback modunda. FastAPI arayüzü, streaming endpoint, health endpoint, Session Memory Node, Vicdan katmanı, HOPEtensor routing contract, Observer / Audit Node ve Self-Reflection Node operasyonel durumdadır."""


def safe_reflection(payload: Dict[str, Any], answer: str = "") -> Dict[str, Any] | None:
    if reflect_answer is None:
        return None

    try:
        return reflect_answer(answer=answer, payload=payload)
    except Exception as exc:
        return {
            "status": "error",
            "node": "self_reflection_node",
            "error": str(exc),
        }


def safe_audit(
    payload: Dict[str, Any],
    answer: str = "",
    verification: Dict[str, Any] | None = None,
    status: str = "ok",
    transport: str = "reason",
    error: str | None = None,
) -> Dict[str, Any] | None:
    if audit_cognition is None:
        return None

    try:
        return audit_cognition(
            payload=payload,
            answer=answer,
            verification=verification,
            status=status,
            transport=transport,
            error=error,
        )
    except Exception:
        return None


def safe_memory(
    payload: Dict[str, Any],
    answer: str = "",
    status: str = "ok",
) -> Dict[str, Any] | None:
    if save_turn is None:
        return None

    try:
        return save_turn(
            payload=payload,
            answer=answer,
            status=status,
        )
    except Exception:
        return None


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # New Starlette-compatible signature. This avoids:
    # TypeError: cannot use 'tuple' as a dict key (unhashable type: 'dict')
    return templates.TemplateResponse(request, "index.html", {})


@app.get("/ping")
async def ping():
    return {
        "ok": True,
        "service": "ATATÜRK DIGITAL TWIN / HOPEVERSE",
    }


@app.get("/health")
async def health():
    return {
        "status": "online",
        "service": "ATATÜRK DIGITAL TWIN / HOPEVERSE",
        "version": "1.3.1",
        "doctrine": DOCTRINE,
        "engine_available": ask_llm is not None and stream_llm is not None,
        "tts_available": text_to_speech is not None,
        "audit_available": audit_cognition is not None,
        "memory_available": save_turn is not None,
        "reflection_available": reflect_answer is not None,
        "engine_import_error": ENGINE_IMPORT_ERROR,
        "audit_import_error": AUDIT_IMPORT_ERROR,
        "memory_import_error": MEMORY_IMPORT_ERROR,
        "reflection_import_error": REFLECTION_IMPORT_ERROR,
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "pipeline": [
            "input",
            "session_memory_node",
            "reasoning_node",
            "vicdan_verification_node",
            "observer_audit_node",
            "self_reflection_node",
            "memory_writeback",
            "delivery",
        ],
    }


@app.get("/api/health")
async def api_health():
    return await health()


@app.post("/reason")
async def reason(request: Request):
    payload = normalize_payload(await request.json())

    if ask_llm is None:
        answer = fallback_answer(payload)
        reflection = safe_reflection(payload, answer)

        audit = safe_audit(
            payload=payload,
            answer=answer,
            verification=reflection,
            status="fallback",
            transport="reason",
            error=ENGINE_IMPORT_ERROR,
        )

        memory = safe_memory(
            payload=payload,
            answer=answer,
            status="fallback",
        )

        return JSONResponse(
            {
                "status": "fallback",
                "answer": answer,
                "reasoning_mode": payload["reasoning_mode"],
                "reflection": reflection,
                "audit": audit,
                "memory": memory,
                "engine_import_error": ENGINE_IMPORT_ERROR,
            }
        )

    try:
        answer = await ask_llm(payload)
        reflection = safe_reflection(payload, answer)

        audit = safe_audit(
            payload=payload,
            answer=answer,
            verification=reflection,
            status="ok",
            transport="reason",
        )

        memory = safe_memory(
            payload=payload,
            answer=answer,
            status="ok",
        )

        return {
            "status": "ok",
            "answer": answer,
            "reasoning_mode": payload["reasoning_mode"],
            "reflection": reflection,
            "audit": audit,
            "memory": memory,
        }

    except Exception as exc:
        answer = fallback_answer(payload)
        reflection = safe_reflection(payload, answer)

        audit = safe_audit(
            payload=payload,
            answer=answer,
            verification=reflection,
            status="error_fallback",
            transport="reason",
            error=str(exc),
        )

        memory = safe_memory(
            payload=payload,
            answer=answer,
            status="error_fallback",
        )

        return JSONResponse(
            {
                "status": "error_fallback",
                "answer": answer,
                "reasoning_mode": payload["reasoning_mode"],
                "reflection": reflection,
                "audit": audit,
                "memory": memory,
                "error": str(exc),
            },
            status_code=200,
        )


async def fallback_stream(payload: Dict[str, Any]) -> AsyncGenerator[str, None]:
    text = fallback_answer(payload)

    for word in text.split(" "):
        yield f"data: {json.dumps({'token': word + ' '}, ensure_ascii=False)}\n\n"

    reflection = safe_reflection(payload, text)
    if reflection is not None:
        yield f"data: {json.dumps({'reflection': reflection}, ensure_ascii=False)}\n\n"

    yield "data: [DONE]\n\n"


@app.post("/stream")
async def stream(request: Request):
    payload = normalize_payload(await request.json())

    async def event_generator():
        collected: List[str] = []

        if stream_llm is None:
            fallback_text = fallback_answer(payload)
            reflection = safe_reflection(payload, fallback_text)

            safe_audit(
                payload=payload,
                answer=fallback_text,
                verification=reflection,
                status="fallback",
                transport="stream",
                error=ENGINE_IMPORT_ERROR,
            )

            safe_memory(
                payload=payload,
                answer=fallback_text,
                status="fallback",
            )

            for word in fallback_text.split(" "):
                token = word + " "
                collected.append(token)
                yield f"data: {json.dumps({'token': token}, ensure_ascii=False)}\n\n"

            if reflection is not None:
                yield f"data: {json.dumps({'reflection': reflection}, ensure_ascii=False)}\n\n"

            yield "data: [DONE]\n\n"
            return

        try:
            async for token in stream_llm(payload):
                collected.append(token)
                yield f"data: {json.dumps({'token': token}, ensure_ascii=False)}\n\n"

            final_answer = "".join(collected)
            reflection = safe_reflection(payload, final_answer)

            safe_audit(
                payload=payload,
                answer=final_answer,
                verification=reflection,
                status="ok",
                transport="stream",
            )

            safe_memory(
                payload=payload,
                answer=final_answer,
                status="ok",
            )

            if reflection is not None:
                yield f"data: {json.dumps({'reflection': reflection}, ensure_ascii=False)}\n\n"

            yield "data: [DONE]\n\n"

        except Exception as exc:
            error_text = f"\n\n[Stream fallback triggered: {str(exc)}]\n\n"
            yield f"data: {json.dumps({'token': error_text}, ensure_ascii=False)}\n\n"

            fallback_text = fallback_answer(payload)
            reflection = safe_reflection(payload, fallback_text)

            safe_audit(
                payload=payload,
                answer=fallback_text,
                verification=reflection,
                status="error_fallback",
                transport="stream",
                error=str(exc),
            )

            safe_memory(
                payload=payload,
                answer=fallback_text,
                status="error_fallback",
            )

            for word in fallback_text.split(" "):
                token = word + " "
                yield f"data: {json.dumps({'token': token}, ensure_ascii=False)}\n\n"

            if reflection is not None:
                yield f"data: {json.dumps({'reflection': reflection}, ensure_ascii=False)}\n\n"

            yield "data: [DONE]\n\n"

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

    try:
        audio_bytes = await text_to_speech(text=text, voice=voice)

        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=hopeverse-voice.mp3"},
        )

    except Exception as exc:
        return JSONResponse(
            {
                "error": "TTS generation failed",
                "detail": str(exc),
            },
            status_code=500,
        )


@app.post("/v1/tasks")
async def tasks(request: Request):
    payload = normalize_payload(await request.json())

    if ask_llm is None:
        answer = fallback_answer(payload)
        reflection = safe_reflection(payload, answer)

        audit = safe_audit(
            payload=payload,
            answer=answer,
            verification=reflection,
            status="fallback",
            transport="v1_tasks",
            error=ENGINE_IMPORT_ERROR,
        )

        memory = safe_memory(
            payload=payload,
            answer=answer,
            status="fallback",
        )

        return {
            "status": "fallback",
            "mode": "v1-hybrid",
            "reasoning_mode": payload["reasoning_mode"],
            "local_llm_enabled": False,
            "answer": answer,
            "reflection": reflection,
            "audit": audit,
            "memory": memory,
            "engine_import_error": ENGINE_IMPORT_ERROR,
        }

    try:
        answer = await ask_llm(payload)
        reflection = safe_reflection(payload, answer)

        audit = safe_audit(
            payload=payload,
            answer=answer,
            verification=reflection,
            status="ok",
            transport="v1_tasks",
        )

        memory = safe_memory(
            payload=payload,
            answer=answer,
            status="ok",
        )

        return {
            "status": "ok",
            "mode": "v1-hybrid",
            "reasoning_mode": payload["reasoning_mode"],
            "local_llm_enabled": True,
            "answer": answer,
            "reflection": reflection,
            "audit": audit,
            "memory": memory,
        }

    except Exception as exc:
        answer = fallback_answer(payload)
        reflection = safe_reflection(payload, answer)

        audit = safe_audit(
            payload=payload,
            answer=answer,
            verification=reflection,
            status="error_fallback",
            transport="v1_tasks",
            error=str(exc),
        )

        memory = safe_memory(
            payload=payload,
            answer=answer,
            status="error_fallback",
        )

        return {
            "status": "error_fallback",
            "mode": "v1-hybrid",
            "reasoning_mode": payload["reasoning_mode"],
            "local_llm_enabled": False,
            "answer": answer,
            "reflection": reflection,
            "audit": audit,
            "memory": memory,
            "error": str(exc),
        }


@app.get("/audit/recent")
async def audit_recent(limit: int = 20):
    if read_recent_audits is None:
        return JSONResponse(
            {
                "status": "unavailable",
                "audit_import_error": AUDIT_IMPORT_ERROR,
            },
            status_code=503,
        )

    return read_recent_audits(limit=limit)


@app.get("/audit/summary")
async def audit_summary(limit: int = 50):
    if summarize_audits is None:
        return JSONResponse(
            {
                "status": "unavailable",
                "audit_import_error": AUDIT_IMPORT_ERROR,
            },
            status_code=503,
        )

    return summarize_audits(limit=limit)


@app.get("/v1/audit/recent")
async def v1_audit_recent(limit: int = 20):
    return await audit_recent(limit=limit)


@app.get("/v1/audit/summary")
async def v1_audit_summary(limit: int = 50):
    return await audit_summary(limit=limit)


@app.get("/memory/recent")
async def memory_recent(limit: int = 8):
    if read_recent_memory is None:
        return JSONResponse(
            {
                "status": "unavailable",
                "memory_import_error": MEMORY_IMPORT_ERROR,
            },
            status_code=503,
        )

    return {
        "status": "ok",
        "records": read_recent_memory(limit=limit),
    }


@app.get("/memory/summary")
async def memory_summary(limit: int = 20):
    if summarize_memory is None:
        return JSONResponse(
            {
                "status": "unavailable",
                "memory_import_error": MEMORY_IMPORT_ERROR,
            },
            status_code=503,
        )

    return summarize_memory(limit=limit)


@app.post("/memory/clear")
async def memory_clear():
    if clear_memory is None:
        return JSONResponse(
            {
                "status": "unavailable",
                "memory_import_error": MEMORY_IMPORT_ERROR,
            },
            status_code=503,
        )

    return clear_memory()


@app.get("/v1/memory/recent")
async def v1_memory_recent(limit: int = 8):
    return await memory_recent(limit=limit)


@app.get("/v1/memory/summary")
async def v1_memory_summary(limit: int = 20):
    return await memory_summary(limit=limit)


@app.get("/reflection/summary")
async def reflection_summary():
    if reflect_answer is None:
        return JSONResponse(
            {
                "status": "unavailable",
                "reflection_import_error": REFLECTION_IMPORT_ERROR,
            },
            status_code=503,
        )

    sample = reflect_answer(
        answer="Cumhuriyet, bilim, etik ve barış temelinde ilerlemeliyiz.",
        payload={"reasoning_mode": "constitutional"},
    )

    return {
        "status": "ok",
        "reflection": sample,
    }
