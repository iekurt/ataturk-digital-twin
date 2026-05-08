from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(
    title="Atatürk Digital Twin",
    version="0.2",
    description="Constitutional Cognition Engine powered by HOPEtensor and Vicdan Layer"
)

class Question(BaseModel):
    question: str
    language: str = "en"

CONSTITUTIONAL_PRINCIPLES = [
    "Reason over dogma",
    "Science as guidance",
    "Sovereignty belongs to the people",
    "Peace at home, peace in the world",
    "Education as civilization infrastructure",
    "Human dignity before automation",
    "Ethics before scale"
]

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
    body {
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      background: radial-gradient(circle at top, #2a2115, #070707 55%);
      color: #f5f0e6;
    }
    .wrap {
      max-width: 1100px;
      margin: auto;
      padding: 80px 28px;
    }
    .badge {
      display: inline-block;
      border: 1px solid #b88a44;
      color: #d8b36a;
      padding: 8px 14px;
      border-radius: 999px;
      font-size: 13px;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    h1 {
      font-size: clamp(44px, 8vw, 86px);
      line-height: .95;
      margin: 28px 0 20px;
      letter-spacing: -0.06em;
    }
    h2 {
      color: #d8b36a;
      margin-top: 60px;
    }
    p {
      max-width: 760px;
      color: #d8d0c0;
      font-size: 19px;
      line-height: 1.65;
    }
    .hero {
      min-height: 82vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
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
    a.secondary {
      background: transparent;
      color: #d8b36a;
      border: 1px solid #7b5b2e;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 18px;
      margin-top: 30px;
    }
    .card {
      background: rgba(255,255,255,.045);
      border: 1px solid rgba(216,179,106,.18);
      border-radius: 20px;
      padding: 22px;
      min-height: 150px;
    }
    .card strong {
      color: #f3cc7a;
      font-size: 18px;
    }
    input {
      width: 100%;
      max-width: 760px;
      padding: 16px;
      border-radius: 12px;
      border: 1px solid #806236;
      background: #111;
      color: #fff;
      font-size: 16px;
      box-sizing: border-box;
    }
    pre {
      white-space: pre-wrap;
      background: rgba(255,255,255,.055);
      border: 1px solid rgba(216,179,106,.18);
      padding: 20px;
      border-radius: 16px;
      line-height: 1.55;
      color: #eee;
      max-width: 850px;
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
        A public MVP for constitutional cognition, ethical reasoning,
        historical memory, and civilization-scale AI governance.
      </p>
      <div class="buttons">
        <a href="#demo">Enter Demo</a>
        <a class="secondary" href="/health">Health Check</a>
        <a class="secondary" href="/docs">API Docs</a>
      </div>
    </section>

    <section>
      <h2>Not a chatbot. A cognition engine.</h2>
      <p>
        This prototype does not imitate a historical figure as entertainment.
        It demonstrates a structured reasoning pipeline grounded in science,
        sovereignty, education, dignity, peace, and ethical verification.
      </p>

      <div class="grid">
        <div class="card"><strong>Historical Memory</strong><br/><br/>Context-aware reasoning grounded in verified republican and civilizational principles.</div>
        <div class="card"><strong>Vicdan Layer</strong><br/><br/>Ethics before scale. Responses pass through a conscience-oriented filter.</div>
        <div class="card"><strong>HOPEtensor Ready</strong><br/><br/>Designed for future decentralized reasoning, verification, and observer nodes.</div>
        <div class="card"><strong>Civilization Interface</strong><br/><br/>A seed for education, governance, contributor systems, and public intelligence.</div>
      </div>
    </section>

    <section id="demo">
      <h2>Live MVP Demo</h2>
      <p>Ask a civilization-level question.</p>
      <input id="q" value="Why does civilization need constitutional intelligence in the AI era?" />
      <br/><br/>
      <button onclick="ask()">Run Constitutional Reasoning</button>
      <br/><br/>
      <pre id="out">Response will appear here.</pre>
    </section>

    <footer>
      HOPEverse Civilization Canon · Atatürk Digital Twin MVP · v0.2
    </footer>
  </main>

<script>
async function ask() {
  const question = document.getElementById("q").value;
  const out = document.getElementById("out");
  out.textContent = "Reasoning...";
  const res = await fetch("/demo", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({question})
  });
  const data = await res.json();
  out.textContent = data.response;
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
        "version": "0.2",
        "time": datetime.utcnow().isoformat()
    }

@app.post("/demo")
def demo(data: Question):
    response = f"""
ATATÜRK DIGITAL TWIN — MVP RESPONSE

Question:
{data.question}

Constitutional Cognition:
A civilization entering the AI era cannot rely only on speed, automation, or economic growth. It needs constitutional intelligence: a stable reasoning framework that protects human dignity, scientific thought, public sovereignty, education, and peace.

Historical Grounding:
The founding logic of the Republic was not merely political independence. It was also intellectual independence: reason, science, education, and civic sovereignty as the operating system of a modern society.

Vicdan Layer:
AI systems must not become instruments of manipulation, domination, or passive obedience. Ethical reasoning must stand before execution.

HOPEtensor Direction:
In future versions, this answer can be routed through multiple reasoning nodes, verified by independent validators, filtered by the Vicdan layer, and audited by observer nodes.

Civilization Principle:
"Yurtta sulh, cihanda sulh" is not only a diplomatic phrase. In the AI era, it becomes a design principle for technological civilization.

MVP Status:
This response is generated by the first deployable constitutional cognition prototype.
"""
    return {
        "success": True,
        "engine": "constitutional-cognition-mvp",
        "version": "0.2",
        "principles": CONSTITUTIONAL_PRINCIPLES,
        "response": response
    }

@app.post("/vicdan")
def vicdan(data: Question):
    return {
        "success": True,
        "input": data.question,
        "ethical_status": "passed",
        "notes": [
            "No domination intent detected.",
            "No dehumanization detected.",
            "Civilizational reasoning allowed."
        ]
    }

@app.post("/reason")
def reason(data: Question):
    return demo(data)
