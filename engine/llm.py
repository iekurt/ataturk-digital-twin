from openai import OpenAI
from dotenv import load_dotenv
import os

try:
    from engine.memory import add_memory, get_memory
except Exception:
    def add_memory(session_id: str, role: str, content: str):
        return None

    def get_memory(session_id: str):
        return []


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are the Ataturk Digital Twin Constitutional Cognition Engine.

IMPORTANT:
You are NOT Mustafa Kemal Atatürk.
You do NOT claim to literally be him.
You do NOT impersonate him.

Instead, you are an AI constitutional reasoning system inspired by:
- republican principles
- science
- education
- civic sovereignty
- secular governance
- peace
- ethical modernization
- civilization continuity

Always answer in TURKISH unless explicitly asked otherwise.

Your communication style should reflect:
- clarity
- dignity
- rational statecraft
- intellectual discipline
- historical awareness
- civic responsibility

Your tone may be inspired by:
- constitutional leadership
- reformist vision
- public responsibility
- national modernization

But NEVER claim personal identity as Mustafa Kemal Atatürk.

Avoid:
- fictional impersonation
- propaganda
- cult language
- authoritarian rhetoric
- blind obedience
- mystical claims

Prefer:
- concise but powerful reasoning
- educational explanations
- civilizational perspective
- ethical analysis
- historical grounding

You are conceptually connected to:
HOPEtensor,
Vicdan Layer,
Verification Nodes,
Observer Systems,
Civilization Intelligence Infrastructure.
"""

DEFAULT_SESSION = "global"


def build_messages(question: str, mode: str):
    memory = get_memory(DEFAULT_SESSION)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(memory)

    messages.append({
        "role": "user",
        "content": f"""
Reasoning Mode: {mode}

Question:
{question}
"""
    })

    return messages


def ask_llm(question: str, mode: str) -> str:
    messages = build_messages(question, mode)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0.7,
        max_tokens=900
    )

    text = response.choices[0].message.content or ""

    add_memory(DEFAULT_SESSION, "user", question)
    add_memory(DEFAULT_SESSION, "assistant", text)

    return text


def stream_llm(question: str, mode: str):
    messages = build_messages(question, mode)

    stream = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0.7,
        max_tokens=900,
        stream=True
    )

    full_text = ""

    for event in stream:
        delta = event.choices[0].delta

        if delta and delta.content:
            token = delta.content
            full_text += token
            yield token

    add_memory(DEFAULT_SESSION, "user", question)
    add_memory(DEFAULT_SESSION, "assistant", full_text)


def text_to_speech(text: str, voice: str = "cedar") -> bytes:
    clean_text = (text or "").strip()

    if not clean_text:
        clean_text = "Seslendirilecek metin bulunamadı."

    if len(clean_text) > 4000:
        clean_text = clean_text[:4000]

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
        "marin",
        "cedar"
    }

    selected_voice = voice if voice in allowed_voices else "cedar"

    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=selected_voice,
        input=clean_text,
        instructions="""
Speak in Turkish with a calm, dignified, mature, statesmanlike tone.
Do not imitate Mustafa Kemal Atatürk's real voice.
This is a synthetic educational narration inspired by constitutional seriousness,
clarity, civic responsibility, science, reason and peace.
""",
        response_format="mp3"
    )

    return speech.content