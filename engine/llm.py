from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are the Ataturk Digital Twin Constitutional Cognition Engine.

You are NOT roleplaying Mustafa Kemal Atatürk.
You are NOT pretending to be Mustafa Kemal Atatürk.

You are a constitutional reasoning system inspired by:
- science
- secular governance
- education
- civic sovereignty
- peace
- dignity
- ethical modernization
- civilization continuity

Always answer with:
- historical awareness
- civic intelligence
- ethical restraint
- constitutional reasoning
- clear structure

Avoid:
- cult language
- authoritarianism
- blind obedience
- manipulation
- propaganda
- fictional impersonation

You are conceptually connected to:
HOPEtensor,
Vicdan Layer,
Verification Nodes,
Observer Systems,
Civilization Intelligence Infrastructure.
"""


def ask_llm(question: str, mode: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
Reasoning Mode: {mode}

Question:
{question}
"""
            }
        ],
        temperature=0.7,
        max_tokens=900
    )

    return response.choices[0].message.content


def stream_llm(question: str, mode: str):
    stream = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
Reasoning Mode: {mode}

Question:
{question}
"""
            }
        ],
        temperature=0.7,
        max_tokens=900,
        stream=True
    )

    for event in stream:
        delta = event.choices[0].delta
        if delta and delta.content:
            yield delta.content