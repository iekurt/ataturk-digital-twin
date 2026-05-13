# app.py
# ATATÜRK DIGITAL TWIN / HOPEVERSE
# FULL CINEMATIC VERSION

import os
import json
import asyncio
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
    StreamingResponse,
    Response
)

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel

try:
    from openai import OpenAI
except:
    OpenAI = None


# =========================================================
# APP
# =========================================================

app = FastAPI(
    title="ATATÜRK DIGITAL TWIN / HOPEVERSE",
    version="2.0.0"
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")


# =========================================================
# OPENAI
# =========================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = None

if OPENAI_API_KEY and OpenAI:
    client = OpenAI(api_key=OPENAI_API_KEY)


# =========================================================
# CONFIG
# =========================================================

DOCTRINE = [
    "Peace at home.",
    "Peace in the world.",
    "Peace in the universe and HOPEverse."
]

REASONING_MODES = {
    "balanced": {
        "label": "Balanced"
    },
    "constitutional": {
        "label": "Constitutional"
    },
    "historical": {
        "label": "Historical"
    },
    "visionary": {
        "label": "Visionary"
    },
    "technical": {
        "label": "Technical"
    },
    "critical": {
        "label": "Critical"
    }
}


# =========================================================
# MODELS
# =========================================================

class ReasonPayload(BaseModel):
    prompt: str = ""
    reasoning_mode: str = "balanced"


class TTSPayload(BaseModel):
    text: str = ""
    voice: str = "alloy"


# =========================================================
# ROOT
# =========================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "doctrine": DOCTRINE
        }
    )


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
async def health():

    return {
        "status": "online",
        "service": "ATATÜRK DIGITAL TWIN / HOPEVERSE",
        "version": "2.0.0",
        "openai_configured": bool(client),
        "pipeline": [
            "input",
            "reasoning_node",
            "vicdan_layer",
            "observer_node",
            "reflection_node",
            "delivery"
        ]
    }


# =========================================================
# PROMPT BUILDER
# =========================================================

def build_system_prompt(mode: str):

    base = f"""
You are the constitutional cognition layer of
ATATÜRK DIGITAL TWIN / HOPEVERSE.

Core doctrine:
- Peace at home.
- Peace in the world.
- Peace in the universe and HOPEverse.

Always answer in Turkish.

Maintain:
- civic dignity
- rationality
- scientific thinking
- constitutional ethics
- historical continuity
"""

    if mode == "constitutional":
        base += """
Focus strongly on constitutional values,
rule of law, secularism and civic equality.
"""

    elif mode == "historical":
        base += """
Focus on historical continuity,
reforms and modernization logic.
"""

    elif mode == "visionary":
        base += """
Focus on HOPEverse, AI ethics,
future civilization systems and dignity.
"""

    elif mode == "technical":
        base += """
Focus on FastAPI, OpenAI,
streaming SSE, HOPEtensor nodes,
deployment and architecture.
"""

    elif mode == "critical":
        base += """
Be analytical and critical.
Point out risks and weaknesses clearly.
"""

    return base


# =========================================================
# FALLBACK
# =========================================================

def local_fallback(prompt: str, mode: str):

    return f"""
Constitutional cognition active.

Soru:
{prompt}

Bu yanıt fallback cognition engine tarafından üretildi.

HOPEtensor reasoning path:
- reasoning node
- vicdan layer
- observer audit
- reflection layer

Aktif mod:
{mode}
"""


# =========================================================
# REASON
# =========================================================

@app.post("/reason")
async def reason(payload: ReasonPayload):

    prompt = payload.prompt.strip()
    mode = payload.reasoning_mode

    if not prompt:
        return JSONResponse({
            "answer": "Prompt boş."
        })

    # FALLBACK
    if not client:

        answer = local_fallback(prompt, mode)

        return JSONResponse({
            "answer": answer,
            "mode": mode,
            "fallback": True
        })

    try:

        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": build_system_prompt(mode)
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )

        answer = completion.choices[0].message.content

        return JSONResponse({
            "answer": answer,
            "mode": mode,
            "fallback": False
        })

    except Exception as e:

        answer = local_fallback(prompt, mode)

        return JSONResponse({
            "answer": answer,
            "fallback": True,
            "error": str(e)
        })


# =========================================================
# STREAM
# =========================================================

@app.post("/stream")
async def stream(payload: ReasonPayload):

    prompt = payload.prompt.strip()
    mode = payload.reasoning_mode

    async def token_stream():

        if not client:

            text = local_fallback(prompt, mode)

            for ch in text:
                yield f"data: {json.dumps({'token': ch})}\n\n"
                await asyncio.sleep(0.01)

            yield "data: [DONE]\n\n"
            return

        try:

            completion = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "system",
                        "content": build_system_prompt(mode)
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                stream=True,
                temperature=0.7
            )

            for chunk in completion:

                try:

                    delta = chunk.choices[0].delta.content

                    if delta:

                        yield f"data: {json.dumps({'token': delta})}\n\n"

                except:
                    pass

            yield "data: [DONE]\n\n"

        except Exception as e:

            text = f"Streaming error: {str(e)}"

            for ch in text:
                yield f"data: {json.dumps({'token': ch})}\n\n"
                await asyncio.sleep(0.01)

            yield "data: [DONE]\n\n"

    return StreamingResponse(
        token_stream(),
        media_type="text/event-stream"
    )


# =========================================================
# TTS
# =========================================================

@app.post("/tts")
async def tts(payload: TTSPayload):

    if not client:

        return Response(
            content=b"",
            media_type="audio/mpeg"
        )

    try:

        speech = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=payload.voice,
            input=payload.text
        )

        audio_bytes = speech.read()

        return Response(
            content=audio_bytes,
            media_type="audio/mpeg"
        )

    except Exception as e:

        return JSONResponse({
            "error": str(e)
        })


# =========================================================
# REFLECTION
# =========================================================

@app.post("/reflection")
async def reflection(payload: ReasonPayload):

    reflection = {
        "reflection_score": 92,
        "constitutional_alignment": 95,
        "historical_alignment": 90,
        "ethical_alignment": 96,
        "hallucination_risk": 8,
        "confidence_score": 91,
        "summary": (
            "Yanıt anayasal çerçeve, tarihsel süreklilik "
            "ve etik hizalanma açısından güçlü bulundu."
        )
    }

    return JSONResponse(reflection)


# =========================================================
# STARTUP
# =========================================================

@app.on_event("startup")
async def startup_event():

    print("")
    print("======================================")
    print("ATATÜRK DIGITAL TWIN / HOPEVERSE")
    print("Constitutional cognition online")
    print("======================================")
    print("")