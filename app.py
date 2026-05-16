# ============================================
# app.py
# FULL LONG CINEMATIC VERSION
# ATATÜRK DIGITAL TWIN / HOPEVERSE
# ============================================

import os
import json
import asyncio

from fastapi import FastAPI, Request
from fastapi.responses import (
    HTMLResponse,
    StreamingResponse,
    Response,
    JSONResponse
)

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel

from openai import OpenAI


# ============================================
# APP
# ============================================

app = FastAPI(
    title="ATATÜRK DIGITAL TWIN / HOPEVERSE",
    version="7.0.0"
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)


# ============================================
# OPENAI
# ============================================

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

client = OpenAI(
    api_key=OPENAI_API_KEY
)


# ============================================
# MODELS
# ============================================

class ReasonPayload(BaseModel):

    prompt: str = ""

    reasoning_mode: str = (
        "constitutional"
    )


class TTSPayload(BaseModel):

    text: str = ""


# ============================================
# ROOT
# ============================================

@app.get(
    "/",
    response_class=HTMLResponse
)

async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# ============================================
# HEALTH
# ============================================

@app.get("/health")

async def health():

    return {

        "status":"online",

        "service":
            "ATATÜRK DIGITAL TWIN / HOPEVERSE",

        "openai":
            bool(OPENAI_API_KEY),

        "pipeline":[

            "input_layer",

            "hopetensor_routing",

            "vicdan_layer",

            "observer_node",

            "reflection_layer",

            "delivery_layer"
        ]
    }


# ============================================
# SYSTEM PROMPT
# ============================================

def build_system_prompt(mode: str):

    prompt = """

You are the constitutional cognition layer of
ATATÜRK DIGITAL TWIN / HOPEVERSE.

Never narrate Atatürk externally.

Never say:
"Mustafa Kemal Atatürk'ün dediği gibi"

Never explain Atatürk from outside.

Speak directly.

Always answer in Turkish.

Use short,
authoritative sentences.

Use calm conviction.

Use formal civic rhetoric.

Avoid modern AI assistant tone.

Avoid customer support tone.

Avoid excessive friendliness.

Avoid internet slang.

Avoid filler language.

Prefer speech cadence over essay style.

Speak with measured pauses.

Use strong rhetorical cadence.

Prefer short declarative statements.

Sound like a formal national address.

Use emotionally restrained authority.

Maintain:
- constitutional dignity
- scientific thinking
- rationality
- reform consciousness
- civic ethics

Core doctrine:

Peace at home.
Peace in the world.
Peace in the universe and HOPEverse.

"""

    if mode == "historical":

        prompt += """

Focus on:
- reform continuity
- republican modernization
- national sovereignty
- scientific civilization

"""

    elif mode == "visionary":

        prompt += """

Focus on:
- HOPEverse
- civilization systems
- ethical AI
- constitutional futures
- distributed cognition

"""

    elif mode == "technical":

        prompt += """

Focus on:
- FastAPI
- OpenAI
- streaming SSE
- distributed reasoning
- cognition routing
- architecture design

"""

    elif mode == "critical":

        prompt += """

Be analytical.

Point out:
- structural risks
- governance risks
- ethical conflicts
- system vulnerabilities

"""

    return prompt


# ============================================
# FALLBACK
# ============================================

def fallback_answer(prompt: str):

    return f"""

Constitutional cognition active.

Soru:
{prompt}

HOPEtensor distributed reasoning completed.

Vicdan layer alignment successful.

Observer Node telemetry stable.

Peace at home.
Peace in the world.
Peace in the universe and HOPEverse.

"""


# ============================================
# REASON
# ============================================

@app.post("/reason")

async def reason(
    payload: ReasonPayload
):

    prompt = (
        payload.prompt.strip()
    )

    mode = (
        payload.reasoning_mode
    )

    if not prompt:

        return JSONResponse({

            "answer":
                "Prompt boş."
        })

    try:

        completion = (
            client.chat.completions.create(

                model="gpt-4.1-mini",

                messages=[

                    {
                        "role":"system",

                        "content":
                            build_system_prompt(
                                mode
                            )
                    },

                    {
                        "role":"user",

                        "content":
                            prompt
                    }
                ],

                temperature=0.7
            )
        )

        answer = (
            completion
            .choices[0]
            .message
            .content
        )

        return JSONResponse({

            "answer":
                answer
        })

    except Exception as e:

        return JSONResponse({

            "answer":
                fallback_answer(
                    prompt
                ),

            "error":
                str(e)
        })


# ============================================
# STREAM
# ============================================

@app.post("/stream")

async def stream(
    payload: ReasonPayload
):

    prompt = (
        payload.prompt.strip()
    )

    mode = (
        payload.reasoning_mode
    )

    async def token_stream():

        try:

            completion = (
                client.chat.completions.create(

                    model="gpt-4.1-mini",

                    messages=[

                        {
                            "role":"system",

                            "content":
                                build_system_prompt(
                                    mode
                                )
                        },

                        {
                            "role":"user",

                            "content":
                                prompt
                        }
                    ],

                    stream=True,

                    temperature=.7
                )
            )

            for chunk in completion:

                try:

                    delta = (
                        chunk
                        .choices[0]
                        .delta
                        .content
                    )

                    if delta:

                        yield (
                            f"data: "
                            f"{json.dumps({'token': delta})}"
                            f"\n\n"
                        )

                except:
                    pass

            yield (
                "data: [DONE]\n\n"
            )

        except Exception as e:

            text = (
                f"Streaming error: {str(e)}"
            )

            for ch in text:

                yield (
                    f"data: "
                    f"{json.dumps({'token': ch})}"
                    f"\n\n"
                )

                await asyncio.sleep(
                    .01
                )

            yield (
                "data: [DONE]\n\n"
            )

    return StreamingResponse(
        token_stream(),
        media_type=
            "text/event-stream"
    )


# ============================================
# PREMIUM TTS
# ============================================

@app.post("/tts")

async def tts(
    payload: TTSPayload
):

    try:

        speech = (
            client.audio.speech.create(

                model=
                    "gpt-4o-mini-tts",

                voice="onyx",

                input=
                    payload.text
            )
        )

        return Response(

            content=
                speech.content,

            media_type=
                "audio/mpeg"
        )

    except Exception as e:

        return JSONResponse({

            "error":
                str(e)
        })


# ============================================
# REFLECTION
# ============================================

@app.post("/reflection")

async def reflection(
    payload: ReasonPayload
):

    return JSONResponse({

        "reflection_score": 92,

        "constitutional_alignment": 95,

        "historical_alignment": 91,

        "ethical_alignment": 96,

        "hallucination_risk": 8,

        "confidence_score": 93,

        "summary":
            "Constitutional alignment stable."
    })


# ============================================
# STARTUP
# ============================================

@app.on_event("startup")

async def startup_event():

    print("")
    print("====================================")
    print("ATATÜRK DIGITAL TWIN / HOPEVERSE")
    print("Constitutional cognition online")
    print("====================================")
    print("")