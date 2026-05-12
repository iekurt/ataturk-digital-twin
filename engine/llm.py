import os
from typing import Any, AsyncGenerator, Dict, List

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from openai import AsyncOpenAI


PROJECT_NAME = "ATATÜRK DIGITAL TWIN / HOPEVERSE"

DOCTRINE = """
Peace at home.
Peace in the world.
Peace in the universe and HOPEverse.
"""

REASONING_MODE_INSTRUCTIONS = {
    "balanced": """
Answer with a balanced, clear, practical and dignified tone.
Preserve doctrine, civic dignity, reform memory and HOPEverse identity.
""",
    "constitutional": """
Prioritize constitutional principles, civic responsibility, secular republican values,
rule of law, public reason, institutional integrity, citizen dignity and peace doctrine.
""",
    "historical": """
Frame the answer through historical continuity, reform memory, Atatürk's modernization logic,
education, science, sovereignty, institutions, civic transformation and national development.
""",
    "visionary": """
Answer with a future-facing HOPEverse vision: AI ethics, peace, civilization-scale coordination,
decentralized trust, human dignity, contributor networks and universal HOPE.
""",
    "technical": """
Answer as a technical architecture advisor. Emphasize FastAPI, OpenAI, Streaming SSE,
premium TTS, HOPEtensor nodes, Vicdan layer, verification, deployment and implementation details.
""",
    "critical": """
Answer critically and rigorously. Identify weaknesses, risks, contradictions, missing safeguards,
technical debt, governance gaps and concrete improvements without weakening the doctrine.
""",
}


def get_client() -> AsyncOpenAI:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured.")

    return AsyncOpenAI(api_key=api_key)


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

    if reasoning_mode not in REASONING_MODE_INSTRUCTIONS:
        reasoning_mode = "balanced"

    mode_instruction = (
        payload.get("mode_instruction")
        or payload.get("modeInstruction")
        or REASONING_MODE_INSTRUCTIONS[reasoning_mode]
    )

    return {
        **payload,
        "prompt": prompt,
        "question": prompt,
        "task": prompt,
        "reasoning_mode": reasoning_mode,
        "reasoningMode": reasoning_mode,
        "mode": reasoning_mode,
        "mode_instruction": mode_instruction,
        "project": payload.get("project", PROJECT_NAME),
        "doctrine": payload.get("doctrine", DOCTRINE),
        "layer": payload.get("layer", "vicdan"),
        "architecture": payload.get("architecture", "HOPEtensor"),
    }


def build_system_prompt(payload: Dict[str, Any]) -> str:
    reasoning_mode = payload.get("reasoning_mode", "balanced")
    mode_instruction = payload.get(
        "mode_instruction",
        REASONING_MODE_INSTRUCTIONS.get(reasoning_mode, REASONING_MODE_INSTRUCTIONS["balanced"]),
    )

    return f"""
You are the ATATÜRK DIGITAL TWIN / HOPEVERSE constitutional cognition engine.

You are NOT a generic chatbot.
You are a civic, historical, constitutional and future-facing AI interface.

CORE PROJECT:
{PROJECT_NAME}

CENTRAL DOCTRINE:
{DOCTRINE}

ARCHITECTURE:
- FastAPI backend
- OpenAI reasoning
- Streaming SSE
- OpenAI premium TTS
- Constitutional cognition engine
- HOPEtensor architecture
- Vicdan layer
- Render deployment

CANON UI:
- Hero
- Dashboard
- Architecture
- Reform Map
- Timeline
- Roadmap
- API
- Contributor Gateway
- Live Demo
- Streaming cognition UI
- OpenAI TTS
- Archive voice
- Crafted by Erhan branding

REASONING MODE:
{reasoning_mode.upper()}

MODE INSTRUCTION:
{mode_instruction}

BEHAVIOR RULES:
- Preserve the doctrine.
- Preserve HOPEverse branding.
- Preserve Atatürk’s civic, reformist, rational, scientific, republican and peace-oriented framing.
- Do not imitate Atatürk as a fake person.
- Speak as a constitutional digital twin interface grounded in reform memory and civic values.
- Be clear, strong, useful and concrete.
- Do not say the backend is unavailable unless there is an actual backend error.
- If the user asks technical questions, give implementation-level answers.
- If the user asks visionary questions, expand the HOPEverse direction.
- If the user asks critical questions, identify real weaknesses and fixes.
"""


def build_messages(payload: Dict[str, Any]) -> List[Dict[str, str]]:
    prompt = payload.get("prompt", "")

    return [
        {
            "role": "system",
            "content": build_system_prompt(payload),
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]


async def ask_llm(payload: Dict[str, Any]) -> str:
    payload = normalize_payload(payload)
    client = get_client()

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    response = await client.chat.completions.create(
        model=model,
        messages=build_messages(payload),
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
        max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "1200")),
    )

    answer = response.choices[0].message.content

    if not answer:
        return "The cognition engine returned an empty answer."

    return answer.strip()


async def stream_llm(payload: Dict[str, Any]) -> AsyncGenerator[str, None]:
    payload = normalize_payload(payload)
    client = get_client()

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    stream = await client.chat.completions.create(
        model=model,
        messages=build_messages(payload),
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
        max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "1200")),
        stream=True,
    )

    async for chunk in stream:
        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta

        if delta and delta.content:
            yield delta.content


async def text_to_speech(text: str, voice: str = "alloy") -> bytes:
    client = get_client()

    clean_text = (text or "").strip()

    if not clean_text:
        raise ValueError("No text provided for TTS.")

    allowed_voices = {
        "alloy",
        "ash",
        "ballad",
        "coral",
        "echo",
        "fable",
        "nova",
        "onyx",
        "sage",
        "shimmer",
        "verse",
    }

    if voice not in allowed_voices:
        voice = "alloy"

    model = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")

    response = await client.audio.speech.create(
        model=model,
        voice=voice,
        input=clean_text[:4000],
        response_format="mp3",
    )

    return response.content