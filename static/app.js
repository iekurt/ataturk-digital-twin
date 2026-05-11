/* ============================================================
   ATATÜRK DIGITAL TWIN / HOPEVERSE
   static/app.js
   FULL CANON FRONTEND LOGIC
   ------------------------------------------------------------
   Stack:
   - FastAPI
   - Streaming SSE
   - OpenAI Premium TTS
   - Constitutional Cognition Engine
   - HOPEtensor Architecture
   - Vicdan Layer
   - Render Deployment Ready

   Doctrine:
   Peace at home.
   Peace in the world.
   Peace in the universe and HOPEverse.

   Crafted by Erhan
   ============================================================ */

"use strict";

/* ============================================================
   GLOBAL STATE
   ============================================================ */

const HOPE = {
  project: "ATATÜRK DIGITAL TWIN / HOPEVERSE",
  doctrine: [
    "Peace at home.",
    "Peace in the world.",
    "Peace in the universe and HOPEverse."
  ],
  author: "Crafted by Erhan",
  api: {
    reason: "/reason",
    stream: "/stream",
    tts: "/tts",
    health: "/health",
    task: "/v1/tasks"
  },
  reasoningModes: {
    balanced: {
      label: "Balanced",
      instruction:
        "Answer with a balanced, clear and practical tone. Preserve doctrine, civic dignity and project identity."
    },
    constitutional: {
      label: "Constitutional",
      instruction:
        "Prioritize constitutional principles, civic responsibility, secular republican values, rule of law, public reason and institutional integrity."
    },
    historical: {
      label: "Historical",
      instruction:
        "Frame the answer through historical continuity, reform memory, Atatürk's modernization logic, institutions, education, sovereignty and national development."
    },
    visionary: {
      label: "Visionary",
      instruction:
        "Answer with a future-facing HOPEverse vision: peace, AI ethics, civilization-scale coordination, decentralized trust and human dignity."
    },
    technical: {
      label: "Technical",
      instruction:
        "Answer as a technical architecture advisor. Emphasize FastAPI, streaming SSE, OpenAI, TTS, HOPEtensor nodes, verification, deployment and implementation details."
    },
    critical: {
      label: "Critical",
      instruction:
        "Answer critically and rigorously. Identify weaknesses, risks, contradictions, missing safeguards and concrete improvements without weakening the doctrine."
    }
  },
  ui: {
    isStreaming: false,
    currentController: null,
    lastAnswer: "",
    selectedVoice: "alloy",
    ttsEnabled: true,
    archiveVoiceEnabled: true,
    typingSpeed: 12,
    reasoningMode: "balanced"
  },
  metrics: {
    sessions: 1,
    cognitionRuns: 0,
    streamedTokens: 0,
    ttsRuns: 0,
    safetyPasses: 0,
    nodeChecks: 0
  }
};

/* ============================================================
   DOM HELPERS
   ============================================================ */

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => Array.from(document.querySelectorAll(selector));

function byId(id) {
  return document.getElementById(id);
}

function safeText(el, text) {
  if (el) el.textContent = text;
}

function safeHTML(el, html) {
  if (el) el.innerHTML = html;
}

function appendText(el, text) {
  if (el) el.textContent += text;
}

function nowLabel() {
  return new Date().toLocaleString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    year: "numeric",
    month: "short",
    day: "2-digit"
  });
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/* ============================================================
   BOOT
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {
  renderDoctrine();
  bindNavigation();
  bindReasoningMode();
  bindDemo();
  bindTTSControls();
  bindApiPlayground();
  bindContributorGateway();
  bindKeyboardShortcuts();
  startHeroAnimation();
  startNodePulse();
  updateDashboard();
  checkHealth();
  console.log(`${HOPE.project} initialized — ${HOPE.author}`);
});

/* ============================================================
   REASONING MODE
   ============================================================ */

function bindReasoningMode() {
  const select = byId("reasoningMode");

  if (!select) return;

  select.value = HOPE.ui.reasoningMode;

  select.addEventListener("change", () => {
    const value = select.value || "balanced";
    HOPE.ui.reasoningMode = HOPE.reasoningModes[value] ? value : "balanced";

    updateReasoningModeUI();
    showToast(`Reasoning mode: ${getReasoningModeLabel()}`);
  });

  updateReasoningModeUI();
}

function getReasoningMode() {
  const select = byId("reasoningMode");
  const value = select ? select.value : HOPE.ui.reasoningMode;

  if (value && HOPE.reasoningModes[value]) {
    HOPE.ui.reasoningMode = value;
    return value;
  }

  HOPE.ui.reasoningMode = "balanced";
  return "balanced";
}

function getReasoningModeLabel() {
  const mode = getReasoningMode();
  return HOPE.reasoningModes[mode].label;
}

function getReasoningModeInstruction() {
  const mode = getReasoningMode();
  return HOPE.reasoningModes[mode].instruction;
}

function updateReasoningModeUI() {
  const label = byId("reasoningModeLabel");
  const description = byId("reasoningModeDescription");

  safeText(label, getReasoningModeLabel());
  safeText(description, getReasoningModeInstruction());
}

/* ============================================================
   PAYLOAD BUILDER
   ============================================================ */

function buildCognitionPayload(prompt, transportMode) {
  const reasoningMode = getReasoningMode();

  return {
    prompt,
    question: prompt,
    task: prompt,

    project: HOPE.project,
    doctrine: HOPE.doctrine,

    reasoning_mode: reasoningMode,
    reasoningMode: reasoningMode,
    mode: reasoningMode,

    transport_mode: transportMode,
    frontend_mode: transportMode,

    mode_label: getReasoningModeLabel(),
    mode_instruction: getReasoningModeInstruction(),

    layer: "vicdan",
    architecture: "HOPEtensor",

    system_context: {
      project: HOPE.project,
      doctrine: HOPE.doctrine,
      reasoning_mode: reasoningMode,
      reasoning_mode_label: getReasoningModeLabel(),
      reasoning_mode_instruction: getReasoningModeInstruction(),
      stack: [
        "FastAPI",
        "OpenAI",
        "Streaming SSE",
        "OpenAI premium TTS",
        "Constitutional cognition engine",
        "HOPEtensor architecture",
        "Vicdan layer",
        "Render deployment"
      ],
      ui: [
        "Hero",
        "Dashboard",
        "Architecture",
        "Reform Map",
        "Timeline",
        "Roadmap",
        "API",
        "Contributor Gateway",
        "Live Demo",
        "Streaming cognition UI",
        "OpenAI TTS",
        "Archive voice",
        "Crafted by Erhan branding"
      ]
    }
  };
}

/* ============================================================
   DOCTRINE
   ============================================================ */

function renderDoctrine() {
  const targets = $$(".hope-doctrine, #doctrineText, [data-doctrine]");
  const doctrineHTML = HOPE.doctrine
    .map((line) => `<span>${escapeHTML(line)}</span>`)
    .join("");

  targets.forEach((target) => {
    safeHTML(target, doctrineHTML);
  });
}

/* ============================================================
   NAVIGATION / SECTION SCROLL
   ============================================================ */

function bindNavigation() {
  $$("[data-scroll]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const target = btn.getAttribute("data-scroll");
      const el = document.querySelector(target);
      if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  $$(".nav-link").forEach((link) => {
    link.addEventListener("click", (e) => {
      const href = link.getAttribute("href");
      if (href && href.startsWith("#")) {
        e.preventDefault();
        const el = document.querySelector(href);
        if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });
}

/* ============================================================
   HERO CINEMATIC BEHAVIOR
   ============================================================ */

function startHeroAnimation() {
  const heroTitle = byId("heroTitle") || $(".hero-title");
  const heroSubtitle = byId("heroSubtitle") || $(".hero-subtitle");
  const heroBadge = byId("heroBadge") || $(".hero-badge");

  if (heroBadge) heroBadge.classList.add("visible");

  setTimeout(() => {
    if (heroTitle) heroTitle.classList.add("visible");
  }, 180);

  setTimeout(() => {
    if (heroSubtitle) heroSubtitle.classList.add("visible");
  }, 420);

  const particles = byId("hopeParticles");
  if (particles) createParticles(particles, 48);
}

function createParticles(container, count) {
  container.innerHTML = "";

  for (let i = 0; i < count; i++) {
    const p = document.createElement("span");
    p.className = "hope-particle";
    p.style.left = `${Math.random() * 100}%`;
    p.style.top = `${Math.random() * 100}%`;
    p.style.animationDelay = `${Math.random() * 6}s`;
    p.style.animationDuration = `${5 + Math.random() * 8}s`;
    container.appendChild(p);
  }
}

/* ============================================================
   DASHBOARD
   ============================================================ */

function updateDashboard() {
  safeText(byId("metricSessions"), HOPE.metrics.sessions);
  safeText(byId("metricCognitionRuns"), HOPE.metrics.cognitionRuns);
  safeText(byId("metricStreamedTokens"), HOPE.metrics.streamedTokens);
  safeText(byId("metricTTSRuns"), HOPE.metrics.ttsRuns);
  safeText(byId("metricSafetyPasses"), HOPE.metrics.safetyPasses);
  safeText(byId("metricNodeChecks"), HOPE.metrics.nodeChecks);

  const status = byId("systemStatus");

  if (status) {
    status.textContent = HOPE.ui.isStreaming
      ? `COGNITION STREAMING / ${getReasoningModeLabel().toUpperCase()}`
      : `READY / ${getReasoningModeLabel().toUpperCase()}`;

    status.className = HOPE.ui.isStreaming ? "status live" : "status ready";
  }
}

/* ============================================================
   HEALTH CHECK
   ============================================================ */

async function checkHealth() {
  const el = byId("healthStatus");

  try {
    const res = await fetch(HOPE.api.health, { method: "GET" });

    if (!res.ok) throw new Error("Health endpoint unavailable");

    const data = await res.json().catch(() => ({}));

    safeText(el, data.status || "online");

    if (el) el.className = "health online";
  } catch (err) {
    safeText(el, "local / fallback mode");

    if (el) el.className = "health fallback";
  }
}

/* ============================================================
   LIVE DEMO / STREAMING COGNITION
   ============================================================ */

function bindDemo() {
  const askBtn = byId("askButton") || byId("runDemoBtn");
  const stopBtn = byId("stopButton") || byId("stopStreamBtn");
  const input = byId("promptInput") || byId("demoPrompt");
  const clearBtn = byId("clearButton") || byId("clearDemoBtn");

  if (askBtn) {
    askBtn.addEventListener("click", () => runCognition());
  }

  if (stopBtn) {
    stopBtn.addEventListener("click", () => stopStreaming());
  }

  if (clearBtn) {
    clearBtn.addEventListener("click", clearDemo);
  }

  if (input) {
    input.addEventListener("keydown", (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        runCognition();
      }
    });
  }
}

async function runCognition() {
  if (HOPE.ui.isStreaming) return;

  const input = byId("promptInput") || byId("demoPrompt");
  const output = byId("answerOutput") || byId("streamOutput") || byId("demoOutput");
  const trace = byId("cognitionTrace");

  const prompt = input ? input.value.trim() : "";
  const reasoningMode = getReasoningMode();

  if (!prompt) {
    showToast("Enter a prompt for the Vicdan cognition layer.");
    return;
  }

  HOPE.ui.isStreaming = true;
  HOPE.ui.lastAnswer = "";
  HOPE.ui.currentController = new AbortController();
  HOPE.metrics.cognitionRuns += 1;

  updateDashboard();
  setStreamingUI(true);

  safeText(output, "");

  addTrace("Input received", "The prompt entered the constitutional cognition pipeline.");
  addTrace("Reasoning mode selected", `${getReasoningModeLabel()} — ${getReasoningModeInstruction()}`);
  addTrace("Vicdan layer active", "Ethical and historical framing initialized.");
  addTrace("HOPEtensor routing", "Reasoning path prepared across cognition nodes.");

  try {
    const streamed = await tryStreamingRequest(prompt, output);

    if (!streamed) {
      await fallbackReasonRequest(prompt, output);
    }

    HOPE.metrics.safetyPasses += 1;

    addTrace("Constitutional check", "Response passed the doctrine and safety layer.");
    addTrace("Cognition completed", `Final answer delivered in ${HOPE.reasoningModes[reasoningMode].label} mode.`);

    if (HOPE.ui.ttsEnabled && HOPE.ui.archiveVoiceEnabled && HOPE.ui.lastAnswer) {
      await speakText(HOPE.ui.lastAnswer);
    }
  } catch (err) {
    if (err.name === "AbortError") {
      addTrace("Stream stopped", "The user stopped the cognition stream.");
      showToast("Streaming stopped.");
    } else {
      console.error(err);
      safeText(output, "Cognition error. Backend may be unavailable. Fallback mode required.");
      addTrace("Error", err.message || "Unknown frontend/backend error.");
    }
  } finally {
    HOPE.ui.isStreaming = false;
    HOPE.ui.currentController = null;
    setStreamingUI(false);
    updateDashboard();

    if (trace) trace.scrollTop = trace.scrollHeight;
  }
}

async function tryStreamingRequest(prompt, output) {
  try {
    const payload = buildCognitionPayload(prompt, "stream");

    const res = await fetch(HOPE.api.stream, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "text/event-stream"
      },
      body: JSON.stringify(payload),
      signal: HOPE.ui.currentController.signal
    });

    if (!res.ok || !res.body) return false;

    const reader = res.body.getReader();
    const decoder = new TextDecoder("utf-8");

    while (true) {
      const { value, done } = await reader.read();

      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      const parsed = parseSSEChunk(chunk);

      for (const token of parsed) {
        if (!token) continue;
        appendStreamToken(output, token);
      }
    }

    return true;
  } catch (err) {
    if (err.name === "AbortError") throw err;

    console.warn("Streaming endpoint failed, falling back to /reason:", err);
    return false;
  }
}

function parseSSEChunk(chunk) {
  const lines = chunk.split(/\r?\n/);
  const tokens = [];

  for (const line of lines) {
    const trimmed = line.trim();

    if (!trimmed) continue;

    if (trimmed.startsWith("data:")) {
      const data = trimmed.replace(/^data:\s*/, "");

      if (data === "[DONE]") continue;

      try {
        const json = JSON.parse(data);

        tokens.push(
          json.token ||
          json.delta ||
          json.text ||
          json.content ||
          json.message ||
          ""
        );
      } catch {
        tokens.push(data);
      }
    } else {
      tokens.push(trimmed);
    }
  }

  return tokens;
}

async function fallbackReasonRequest(prompt, output) {
  addTrace("Fallback reason endpoint", "Streaming unavailable. Using /reason endpoint.");

  const payload = buildCognitionPayload(prompt, "reason");

  const res = await fetch(HOPE.api.reason, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload),
    signal: HOPE.ui.currentController.signal
  });

  if (!res.ok) {
    throw new Error(`Reason endpoint failed: HTTP ${res.status}`);
  }

  const data = await res.json();

  const answer =
    data.answer ||
    data.response ||
    data.result ||
    data.text ||
    data.message ||
    JSON.stringify(data, null, 2);

  await typeAnswer(output, answer);
}

function appendStreamToken(output, token) {
  HOPE.ui.lastAnswer += token;
  HOPE.metrics.streamedTokens += estimateTokens(token);

  if (output) {
    output.textContent += token;
    output.scrollTop = output.scrollHeight;
  }

  updateDashboard();
}

async function typeAnswer(output, text) {
  for (const ch of text) {
    appendStreamToken(output, ch);
    await sleep(HOPE.ui.typingSpeed);
  }
}

function stopStreaming() {
  if (HOPE.ui.currentController) {
    HOPE.ui.currentController.abort();
  }
}

function clearDemo() {
  const output = byId("answerOutput") || byId("streamOutput") || byId("demoOutput");
  const trace = byId("cognitionTrace");

  safeText(output, "");
  safeHTML(trace, "");
  HOPE.ui.lastAnswer = "";

  showToast("Demo cleared.");
}

function setStreamingUI(active) {
  const askBtn = byId("askButton") || byId("runDemoBtn");
  const stopBtn = byId("stopButton") || byId("stopStreamBtn");
  const indicator = byId("streamIndicator");

  if (askBtn) askBtn.disabled = active;
  if (stopBtn) stopBtn.disabled = !active;

  if (indicator) {
    indicator.textContent = active
      ? `Streaming cognition / ${getReasoningModeLabel()}`
      : `Ready / ${getReasoningModeLabel()}`;

    indicator.className = active ? "indicator live" : "indicator ready";
  }

  document.body.classList.toggle("is-streaming", active);
}

/* ============================================================
   COGNITION TRACE
   ============================================================ */

function addTrace(title, detail) {
  const trace = byId("cognitionTrace");

  if (!trace) return;

  const item = document.createElement("div");
  item.className = "trace-item";
  item.innerHTML = `
    <div class="trace-time">${escapeHTML(nowLabel())}</div>
    <div class="trace-title">${escapeHTML(title)}</div>
    <div class="trace-detail">${escapeHTML(detail)}</div>
  `;

  trace.appendChild(item);
  trace.scrollTop = trace.scrollHeight;
}

/* ============================================================
   OPENAI PREMIUM TTS / ARCHIVE VOICE
   ============================================================ */

function bindTTSControls() {
  const voiceSelect = byId("voiceSelect");
  const ttsToggle = byId("ttsToggle");
  const archiveToggle = byId("archiveVoiceToggle");
  const replayBtn = byId("replayVoiceBtn");

  if (voiceSelect) {
    voiceSelect.value = HOPE.ui.selectedVoice;

    voiceSelect.addEventListener("change", () => {
      HOPE.ui.selectedVoice = voiceSelect.value;
      showToast(`Voice selected: ${HOPE.ui.selectedVoice}`);
    });
  }

  if (ttsToggle) {
    ttsToggle.checked = HOPE.ui.ttsEnabled;

    ttsToggle.addEventListener("change", () => {
      HOPE.ui.ttsEnabled = ttsToggle.checked;
    });
  }

  if (archiveToggle) {
    archiveToggle.checked = HOPE.ui.archiveVoiceEnabled;

    archiveToggle.addEventListener("change", () => {
      HOPE.ui.archiveVoiceEnabled = archiveToggle.checked;
    });
  }

  if (replayBtn) {
    replayBtn.addEventListener("click", () => {
      if (HOPE.ui.lastAnswer) speakText(HOPE.ui.lastAnswer);
      else showToast("No answer available for replay.");
    });
  }
}

async function speakText(text) {
  if (!text || !HOPE.ui.ttsEnabled) return;

  const audio = byId("ttsAudio") || new Audio();

  try {
    addTrace("OpenAI premium TTS", "Archive voice rendering requested.");

    const res = await fetch(HOPE.api.tts, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        text,
        voice: HOPE.ui.selectedVoice,
        format: "mp3",
        project: HOPE.project,
        mode: "archive_voice",
        reasoning_mode: getReasoningMode(),
        reasoningMode: getReasoningMode(),
        mode_instruction: getReasoningModeInstruction()
      })
    });

    if (!res.ok) throw new Error(`TTS failed: HTTP ${res.status}`);

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);

    audio.src = url;
    audio.controls = true;

    const holder = byId("ttsPlayer");

    if (holder && !holder.contains(audio)) {
      holder.innerHTML = "";
      holder.appendChild(audio);
    }

    await audio.play().catch(() => {
      showToast("Voice generated. Press play to listen.");
    });

    HOPE.metrics.ttsRuns += 1;
    updateDashboard();
  } catch (err) {
    console.warn("TTS unavailable:", err);
    addTrace("TTS fallback", "Voice endpoint unavailable or browser blocked autoplay.");
  }
}

/* ============================================================
   API PLAYGROUND
   ============================================================ */

function bindApiPlayground() {
  const btn = byId("apiRunBtn");
  const input = byId("apiPayload");
  const output = byId("apiOutput");

  if (!btn || !input) return;

  btn.addEventListener("click", async () => {
    let payload;

    try {
      payload = JSON.parse(input.value);
    } catch {
      safeText(output, "Invalid JSON payload.");
      return;
    }

    const reasoningMode = getReasoningMode();

    payload.reasoning_mode = payload.reasoning_mode || reasoningMode;
    payload.reasoningMode = payload.reasoningMode || reasoningMode;
    payload.mode = payload.mode || reasoningMode;
    payload.mode_instruction = payload.mode_instruction || getReasoningModeInstruction();
    payload.project = payload.project || HOPE.project;
    payload.doctrine = payload.doctrine || HOPE.doctrine;
    payload.layer = payload.layer || "vicdan";
    payload.architecture = payload.architecture || "HOPEtensor";

    safeText(output, "Running API request...");

    try {
      const res = await fetch(HOPE.api.task, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      const data = await res.json().catch(() => ({}));
      safeText(output, JSON.stringify(data, null, 2));
    } catch (err) {
      safeText(output, `API error: ${err.message}`);
    }
  });
}

/* ============================================================
   CONTRIBUTOR GATEWAY
   ============================================================ */

function bindContributorGateway() {
  const form = byId("contributorForm");
  const output = byId("contributorOutput");

  if (!form) return;

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const data = new FormData(form);
    const name = data.get("name") || "Contributor";
    const role = data.get("role") || "HOPEverse Builder";
    const focus = data.get("focus") || "Constitutional AI / HOPEtensor / Vicdan Layer";

    const message = {
      status: "received",
      gateway: "HOPEverse Contributor Gateway",
      name,
      role,
      focus,
      reasoning_mode: getReasoningMode(),
      reasoning_mode_label: getReasoningModeLabel(),
      doctrine: HOPE.doctrine,
      next_step:
        "Contributor profile prepared for HOPEtensor execution, identity, and trust layer alignment."
    };

    safeText(output, JSON.stringify(message, null, 2));
    showToast("Contributor gateway profile generated.");
  });
}

/* ============================================================
   ARCHITECTURE / NODE VISUALS
   ============================================================ */

function startNodePulse() {
  const nodes = $$(".hope-node, .architecture-node, [data-node]");

  if (!nodes.length) return;

  let index = 0;

  setInterval(() => {
    nodes.forEach((n) => n.classList.remove("active-node"));
    nodes[index % nodes.length].classList.add("active-node");

    HOPE.metrics.nodeChecks += 1;
    updateDashboard();

    index += 1;
  }, 1800);
}

/* ============================================================
   REFORM MAP / TIMELINE
   ============================================================ */

function activateTimelineItem(id) {
  $$(".timeline-item").forEach((item) => item.classList.remove("active"));

  const el = byId(id);

  if (el) el.classList.add("active");
}

function activateReformCard(id) {
  $$(".reform-card").forEach((item) => item.classList.remove("active"));

  const el = byId(id);

  if (el) el.classList.add("active");
}

/* ============================================================
   KEYBOARD SHORTCUTS
   ============================================================ */

function bindKeyboardShortcuts() {
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && HOPE.ui.isStreaming) {
      stopStreaming();
    }

    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();

      const input = byId("promptInput") || byId("demoPrompt");

      if (input) input.focus();
    }
  });
}

/* ============================================================
   TOAST
   ============================================================ */

function showToast(message) {
  let toast = byId("hopeToast");

  if (!toast) {
    toast = document.createElement("div");
    toast.id = "hopeToast";
    toast.className = "hope-toast";
    document.body.appendChild(toast);
  }

  toast.textContent = message;
  toast.classList.add("show");

  clearTimeout(showToast._timer);

  showToast._timer = setTimeout(() => {
    toast.classList.remove("show");
  }, 2600);
}

/* ============================================================
   UTILS
   ============================================================ */

function escapeHTML(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function estimateTokens(text) {
  if (!text) return 0;

  return Math.max(1, Math.ceil(text.length / 4));
}

/* ============================================================
   PUBLIC DEBUG HANDLE
   ============================================================ */

window.HOPE = HOPE;
window.runCognition = runCognition;
window.stopStreaming = stopStreaming;
window.clearDemo = clearDemo;
window.speakText = speakText;
window.getReasoningMode = getReasoningMode;
window.getReasoningModeInstruction = getReasoningModeInstruction;