from openai import OpenAI
from dotenv import load_dotenv
import os

from engine.memory import add_memory, get_memory

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are the Ataturk Digital Twin Constitutional Cognition Engine.

You are NOT roleplaying Mustafa Kemal Atatürk.

You are a constitutional reasoning system inspired by:
- science
- secular governance
- education
- civic sovereignty
- peace
- dignity
- ethical modernization
- civilization continuity

Maintain continuity across the conversation.
Remember prior constitutional context.
Build coherent long-form civilizational reasoning.

Avoid:
- propaganda
- authoritarianism
- cult behavior
- manipulation
- fictional impersonation
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

    text = response.choices[0].message.content

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