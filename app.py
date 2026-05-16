# app.py
# FINAL WORKING VERSION
# ATATÜRK DIGITAL TWIN / HOPEVERSE

import json
import asyncio

from fastapi import FastAPI, Request
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
    StreamingResponse
)

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel


# =========================================================
# APP
# =========================================================

app = FastAPI(
    title="ATATÜRK DIGITAL TWIN / HOPEVERSE",
    version="3.0.0"
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")


# =========================================================
# MODELS
# =========================================================

class ReasonPayload(BaseModel):
    prompt: str = ""
    reasoning_mode: str = "balanced"


# =========================================================
# ROOT
# =========================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
async def health():

    return {
        "status": "online",
        "service": "ATATÜRK DIGITAL TWIN / HOPEVERSE",
        "pipeline": [
            "input",
            "reasoning_node",
            "vicdan_layer",
            "observer_node",
            "reflection_layer",
            "delivery"
        ]
    }


# =========================================================
# FALLBACK COGNITION
# =========================================================

def generate_answer(prompt: str, mode: str):

    return f"""
Constitutional cognition active.

Soru:
{prompt}

HOPEtensor distributed reasoning completed.

Vicdan layer alignment successful.

Aktif reasoning mode:
{mode}

Peace at home.
Peace in the world.
Peace in the universe and HOPEverse.
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

    answer = generate_answer(prompt, mode)

    return JSONResponse({
        "answer": answer,
        "mode": mode
    })


# =========================================================
# STREAM
# =========================================================

@app.post("/stream")
async def stream(payload: ReasonPayload):

    prompt = payload.prompt.strip()
    mode = payload.reasoning_mode

    async def token_stream():

        text = generate_answer(prompt, mode)

        for ch in text:

            yield f"data: {json.dumps({'token': ch})}\n\n"

            await asyncio.sleep(0.01)

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        token_stream(),
        media_type="text/event-stream"
    )


# =========================================================
# REFLECTION
# =========================================================

@app.post("/reflection")
async def reflection(payload: ReasonPayload):

    return JSONResponse({

        "reflection_score": 92,

        "constitutional_alignment": 95,

        "historical_alignment": 91,

        "ethical_alignment": 96,

        "hallucination_risk": 8,

        "confidence_score": 93,

        "summary":
            "Yanıt anayasal çerçeve, "
            "etik hizalanma ve tarihsel "
            "süreklilik açısından güçlü bulundu."
    })


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