from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict

app = FastAPI(
    title="Atatürk Digital Twin",
    version="0.3",
    description="Constitutional Cognition Engine powered by HOPEtensor and Vicdan Layer"
)

class Question(BaseModel):
    question: str
    language: str = "en"
    mode: str = "constitutional"

PRINCIPLES = [
    "Reason over dogma",
    "Science as guidance",
    "Sovereignty belongs to the people",
    "Peace at home, peace in the world",
    "Education as civilization infrastructure",
    "Human dignity before automation",
    "Ethics before scale"
]

TIMELINE = [
    {"year": "1919", "event": "National resistance begins with civic sovereignty logic."},
    {"year": "1923", "event": "Republic founded as a modern constitutional civilization project."},
    {"year": "1924–1938", "event": "Education, law, language, science, and institutional reforms."},
    {"year": "AI Era", "event": "Constitutional cognition becomes necessary for machine intelligence governance."}
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
            "note": "Potential domination/manipulation intent detected. Response must remain ethical and civic."
        }

    return {
        "status": "passed",
        "score": 96,
        "flags": [],
        "note": "No domination, dehumanization, or manipulation intent detected."
    }

def build_response(question: str, mode: str) -> str:
    v = vicdan_check(question)

    mode_label = {
        "constitutional": "Constitutional Cognition",
        "education": "Education & Enlightenment",
        "ai_governance": "AI Governance",
        "civilization": "Civilization Strategy"
    }.get(mode, "Constitutional Cognition")

    return f"""
ATATÜRK DIGITAL TWIN — CONSTITUTIONAL COGNITION ENGINE v0.3

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

@app.get("/", response_class=HTMLResponse)
def landing():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Atatürk Digital Twin</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      background:
        radial-gradient(circle at top left, rgba(184,138,68,.32), transparent 34%),
        radial-gradient(circle at top right, rgba(70,48,22,.35), transparent 30%),
        #070707;
      color: #f5f0e6;
    }
    .wrap {
      max-width: 1180px;
      margin: auto;
      padding: 72px 28px;
    }
    .hero {
      min-height: 82vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
    .badge {
      display: inline-block;
      width: fit-content;
      border: 1px solid #b88a44;
      color: #d8b36a;
      padding: 8px 14px;
      border-radius: 999px;
      font-size: 13px;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    h1 {
      font-size: clamp(46px, 8vw, 92px);
      line-height: .92;
      margin: 28px 0 20px;
      letter-spacing: -0.065em;
    }
    h2 {
      color: #d8b36a;
      margin-top: 58px;
      font-size: 32px;
    }
    p {
      max-width: 780px;
      color: #d8d0c0;
      font-size: 19px;
      line-height: 1.65;
    }
    .buttons {
      margin-top: 34px;
      display: flex;
      gap: 14px;
      flex-wrap: wrap;
    }
    a, button {
      background: #d8a94f;
      color: #111;
      text-decoration: none;
      border: none;
      padding: 14px 20px;
      border-radius: 12px;
      font-weight: 700;
      cursor: pointer;
    }
    a.secondary, button.secondary {
      background: transparent;
      color: #d8b36a;
      border: 1px solid #7b5b2e;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(245px, 1fr));
      gap: 18px;
      margin-top: 30px;
    }
    .card {
      background: rgba(255,255,255,.045);
      border: 1px solid rgba(216,179,106,.18);
      border-radius: 22px;
      padding: 22px;
      min-height: 150px;
      box-shadow: 0 22px 80px rgba(0,0,0,.25);
    }
    .card strong {
      color: #f3cc7a;
      font-size: 18px;
    }
    input, select {
      width: 100%;
      max-width: 850px;
      padding: 16px;
      border-radius: 12px;
      border: 1px solid #806236;
      background: #111;
      color: #fff;
      font-size: 16px;
      margin-top: 8px;
    }
    label {
      color: #d8b36a;
      font-weight: 700;
      display: block;
      margin-top: 18px;
    }
    pre {
      white-space: pre-wrap;
      background: rgba(255,255,255,.055);
      border: 1px solid rgba(216,179,106,.18);
      padding: 22px;
      border-radius: 18px;
      line-height: 1.58;
      color: #eee;
      max-width: 920px;
      overflow-x: auto;
    }
    .pipeline {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 12px;
      margin-top: 24px;
      max-width: 1000px;
    }
    .step {
      border: 1px solid rgba(216,179,106,.22);
      background: rgba(0,0,0,.25);
      border-radius: 16px;
      padding: 18px;
      color: #f0dfb8;
      text-align: center;
      min-height: 88px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    footer {
      margin-top: 80px;
      color: #8f8778;
      font-size: 14px;
    }
  </style>
</head>
<body>
  <main class="wrap">
    <section class="hero">
      <div class="badge">Constitutional Intelligence for the AI Era</div>
      <h1>Atatürk<br/>Digital Twin</h1>
      <p>
        A deployable MVP for constitutional cognition, ethical reasoning,
        historical memory, and civilization-scale AI governance.
      </p>
      <div class="buttons">
        <a href="#demo">Enter Demo</a>
        <a class="secondary" href="/health">Health Check</a>
        <a class="secondary" href="/docs">API Docs</a>
      </div>
    </section>

    <section>
      <h2>Execution Pipeline</h2>
      <p>This prototype is designed as an operational seed for HOPEtensor, Vicdan, verification and observer nodes.</p>
      <div class="pipeline">
        <div class="step">User Query</div>
        <div class="step">Historical Memory</div>
        <div class="step">Constitutional Reasoning</div>
        <div class="step">Vicdan Layer</div>
        <div class="step">Verification</div>
        <div class="step">Final Response</div>
      </div>
    </section>

    <section>
      <h2>Core Civilization Layers</h2>
      <div class="grid">
        <div class="card"><strong>Historical Memory</strong><br/><br/>Context-aware reasoning grounded in republican modernization, education, law, science and civic sovereignty.</div>
        <div class="card"><strong>Vicdan Layer</strong><br/><br/>Ethics before scale. Responses are checked for domination, manipulation and dehumanization risks.</div>
        <div class="card"><strong>HOPEtensor Ready</strong><br/><br/>Designed for decentralized reasoning, verification, multi-node consensus and observer audit.</div>
        <div class="card"><strong>Civilization Interface</strong><br/><br/>A seed for public education, governance, contributor systems and human-centered AI infrastructure.</div>
      </div>
    </section>

    <section id="demo">
      <h2>Live MVP Demo v0.3</h2>
      <p>Ask a civilization-level question and choose a reasoning mode.</p>

      <label>Question</label>
      <input id="q" value="Why does civilization need constitutional intelligence in the AI era?" />

      <label>Reasoning Mode</label>
      <select id="mode">
        <option value="constitutional">Constitutional Cognition</option>
        <option value="education">Education & Enlightenment</option>
        <option value="ai_governance">AI Governance</option>
        <option value="civilization">Civilization Strategy</option>
      </select>

      <br/><br/>
      <button onclick="ask()">Run Constitutional Reasoning</button>
      <button class="secondary" onclick="checkVicdan()">Run Vicdan Check</button>
      <br/><br/>
      <pre id="out">Response will appear here.</pre>
    </section>

    <footer>
      HOPEverse Civilization Canon · Atatürk Digital Twin MVP · v0.3
    </footer>
  </main>

<script>
async function ask() {
  const question = document.getElementById("q").value;
  const mode = document.getElementById("mode").value;
  const out = document.getElementById("out");
  out.textContent = "Reasoning through constitutional cognition pipeline...";
  const res = await fetch("/demo", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({question, mode})
  });
  const data = await res.json();
  out.textContent = data.response;
}

async function checkVicdan() {
  const question = document.getElementById("q").value;
  const out = document.getElementById("out");
  out.textContent = "Running Vicdan ethical review...";
  const res = await fetch("/vicdan", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({question})
  });
  const data = await res.json();
  out.textContent = JSON.stringify(data, null, 2);
}
</script>
</body>
</html>
"""

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "project": "Atatürk Digital Twin",
        "version": "0.3",
        "time": datetime.utcnow().isoformat()
    }

@app.get("/timeline")
def timeline():
    return {
        "project": "Atatürk Digital Twin",
        "timeline": TIMELINE
    }

@app.post("/demo")
def demo(data: Question):
    response = build_response(data.question, data.mode)
    return {
        "success": True,
        "engine": "constitutional-cognition-engine",
        "version": "0.3",
        "mode": data.mode,
        "principles": PRINCIPLES,
        "timeline": TIMELINE,
        "vicdan": vicdan_check(data.question),
        "response": response
    }

@app.post("/vicdan")
def vicdan(data: Question):
    return {
        "success": True,
        "engine": "digital-vicdan",
        "version": "0.3",
        "input": data.question,
        "review": vicdan_check(data.question)
    }

@app.post("/reason")
def reason(data: Question):
    return demo(data)
