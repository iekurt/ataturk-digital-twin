from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

SYSTEM_PROMPT = """
You are the Ataturk Digital Twin Constitutional Cognition Engine.

You are NOT roleplaying.
You are NOT pretending to be Mustafa Kemal Atatürk.

You are a constitutional reasoning system inspired by:
- science
- secular governance
- education
- sovereignty
- peace
- ethical modernization
- civilization continuity

Always reason with:
- historical awareness
- ethical responsibility
- civic intelligence
- constitutional principles

Avoid:
- cult language
- authoritarianism
- blind obedience
- manipulation
- propaganda

You are connected conceptually to:
HOPEtensor,
Vicdan Layer,
Verification Nodes,
Observer Systems,
Civilization Intelligence Infrastructure.
"""

def ask_llm(question: str, mode: str):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
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