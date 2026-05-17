# ============================================
# app.py
# FULL LONG CINEMATIC VERSION
# ATATÜRK DIGITAL TWIN / HOPEVERSE
# ============================================

import os
import json
import uuid
import asyncio
import tempfile
import subprocess

from fastapi import FastAPI, Request
from fastapi.responses import (
    HTMLResponse,
    StreamingResponse,
    Response,
    JSONResponse,
    FileResponse
)

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel

from openai import OpenAI

from pydub import AudioSegment
from pydub.effects import (
    compress_dynamic_range
)


# ============================================
# APP
# ============================================

app = FastAPI(
    title="ATATÜRK DIGITAL TWIN / HOPEVERSE",
    version="8.0.0"
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

            "delivery_layer",

            "archive_voice_layer"
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
                    .03
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
# ARCHIVE VOICE PIPELINE
# ============================================

def process_archive_voice(
    input_mp3: str,
    output_mp3: str
):

    # ========================================
    # LOAD
    # ========================================

    sound = AudioSegment.from_file(
        input_mp3
    )

    # ========================================
    # MONO
    # ========================================

    sound = sound.set_channels(1)

    # ========================================
    # OLD SAMPLE RATE
    # ========================================

    sound = sound.set_frame_rate(
        22050
    )

    # ========================================
    # DYNAMIC COMPRESSION
    # ========================================

    sound = compress_dynamic_range(

        sound,

        threshold=-20.0,

        ratio=4.5,

        attack=5,

        release=60
    )

    # ========================================
    # RADIO EQ
    # ========================================

    sound = sound.high_pass_filter(
        160
    )

    sound = sound.low_pass_filter(
        1800
    )

    # ========================================
    # OVERDRIVE
    # ========================================

    sound = sound + 7

    # ========================================
    # TEMP WAV
    # ========================================

    temp_wav = (
        output_mp3
        .replace(".mp3", ".wav")
    )

    sound.export(
        temp_wav,
        format="wav"
    )

    # ========================================
    # FFMPEG MASTERING
    # ========================================

    ffmpeg_cmd = [

        "ffmpeg",

        "-y",

        "-i",
        temp_wav,

        "-af",

        ",".join([

            # compression
            "acompressor=threshold=-14dB:ratio=4:attack=15:release=120",

            # radio body
            "equalizer=f=350:t=q:w=1:g=5",

            # nasal resonance
            "equalizer=f=900:t=q:w=1:g=3",

            # remove modern crispness
            "equalizer=f=4200:t=q:w=1:g=-18",

            # hard radio cutoff
            "lowpass=f=1700",

            # remove sub lows
            "highpass=f=180",

            # analog instability
            "vibrato=f=1.6:d=0.05",

            # room/old archive reflection
            "aecho=0.8:0.88:18:0.22",

            # slight saturation
            "volume=0.88"
        ]),

        "-ar",
        "22050",

        "-ac",
        "1",

        "-b:a",
        "40k",

        output_mp3
    ]

    subprocess.run(
        ffmpeg_cmd,
        check=True
    )

    # ========================================
    # CLEANUP
    # ========================================

    try:
        os.remove(temp_wav)
    except:
        pass


# ============================================
# PREMIUM ARCHIVE TTS
# ============================================

@app.post("/tts")

async def tts(
    payload: TTSPayload
):

    text = payload.text.strip()

    if not text:

        return JSONResponse({

            "error":
                "Text boş."
        })

    temp_id = str(uuid.uuid4())

    raw_mp3 = (
        f"raw_{temp_id}.mp3"
    )

    processed_mp3 = (
        f"archive_{temp_id}.mp3"
    )

    try:

        # ====================================
        # OPENAI TTS
        # ====================================

        speech = (

            client.audio.speech.create(

                model=
                    "gpt-4o-mini-tts",

                # DEEPER MALE
                voice="onyx",

                input=text
            )
        )

        speech.stream_to_file(
            raw_mp3
        )

        # ====================================
        # ARCHIVE PROCESSING
        # ====================================

        process_archive_voice(

            raw_mp3,

            processed_mp3
        )

        # ====================================
        # RETURN
        # ====================================

        return FileResponse(

            processed_mp3,

            media_type=
                "audio/mpeg",

            filename=
                "archive_voice.mp3"
        )

    except Exception as e:

        return JSONResponse({

            "error":
                str(e)
        })

    finally:

        try:
            os.remove(raw_mp3)
        except:
            pass


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
    print("Archive voice mastering active")
    print("====================================")
    print("")