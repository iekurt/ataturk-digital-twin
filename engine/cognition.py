from typing import Dict

PRINCIPLES = [
    "Reason over dogma",
    "Science as guidance",
    "Sovereignty belongs to the people",
    "Peace at home, peace in the world",
    "Education as civilization infrastructure",
    "Human dignity before automation",
    "Ethics before scale",
]

TIMELINE = [
    {"year": "1919", "event": "National resistance begins with civic sovereignty logic."},
    {"year": "1923", "event": "Republic founded as a modern constitutional civilization project."},
    {"year": "1924–1938", "event": "Education, law, language, science, and institutional reforms."},
    {"year": "AI Era", "event": "Constitutional cognition becomes necessary for machine intelligence governance."},
]

def vicdan_check(question: str) -> Dict:
    risk_terms = ["dominate", "manipulate", "deceive", "propaganda", "hate"]
    lowered = question.lower()
    flags = [term for term in risk_terms if term in lowered]

    if flags:
        return {
            "status": "review_required",
            "score": 72,
            "flags": flags,
            "note": "Potential domination/manipulation intent detected. Response must remain ethical and civic.",
        }

    return {
        "status": "passed",
        "score": 96,
        "flags": [],
        "note": "No domination, dehumanization, or manipulation intent detected.",
    }

def build_response(question: str, mode: str) -> str:
    v = vicdan_check(question)

    mode_label = {
        "constitutional": "Constitutional Cognition",
        "education": "Education & Enlightenment",
        "ai_governance": "AI Governance",
        "civilization": "Civilization Strategy",
    }.get(mode, "Constitutional Cognition")

    return f"""
ATATÜRK DIGITAL TWIN — CONSTITUTIONAL COGNITION ENGINE v0.4

Question:
{question}

Mode:
{mode_label}

1. Historical Grounding
The founding logic of the Republic was not only political independence.
It was intellectual independence: reason, science, education, civic dignity,
and sovereignty as the operating system of a modern society.

2. Constitutional Reasoning
In the AI era, intelligence without constitutional limits can become speed without wisdom.
A society needs principles that decide what must be automated, what must remain human,
and what must never be surrendered to opaque systems.

3. Vicdan Layer
Ethical Status: {v["status"]}
Vicdan Score: {v["score"]}/100
Notes: {v["note"]}

4. HOPEtensor Direction
Future versions should route this question through:
- Coordinator Node
- Historical Memory Node
- Reasoning Nodes
- Verification Node
- Vicdan Ethics Node
- Observer Audit Node

5. Civilization Principle
“Yurtta sulh, cihanda sulh” becomes a technological design principle:
peace requires truthful systems, educated citizens, sovereign institutions,
and ethical intelligence.

6. MVP Output
This is not roleplay.
This is an early prototype of constitutional cognition.
"""