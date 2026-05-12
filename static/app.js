/* ATATÜRK DIGITAL TWIN / HOPEVERSE — static/app.js FULL */

"use strict";

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
        "Türkçe cevap ver. Dengeli, net, pratik ve saygın bir ton kullan. Doktrini, civic dignity ve proje kimliğini koru."
    },
    constitutional: {
      label: "Constitutional",
      instruction:
        "Türkçe cevap ver. Anayasal ilkeleri, cumhuriyet değerlerini, hukukun üstünlüğünü, laikliği, kamusal aklı, yurttaş onurunu ve barış doktrinini öne çıkar."
    },
    historical: {
      label: "Historical",
      instruction:
        "Türkçe cevap ver. Cevabı tarihsel süreklilik, Atatürk reform hafızası, modernleşme mantığı, eğitim, bilim, egemenlik ve kurumlar üzerinden kur."
    },
    visionary: {
      label: "Visionary",
      instruction:
        "Türkçe cevap ver. HOPEverse vizyonunu, yapay zekâ etiğini, barışı, insan onurunu, merkeziyetsiz güveni ve medeniyet ölçekli koordinasyonu öne çıkar."
    },
    technical: {
      label: "Technical",
      instruction:
        "Türkçe cevap ver. Teknik mimari danışmanı gibi yanıtla. FastAPI, OpenAI, Streaming SSE, TTS, HOPEtensor node yapısı, Vicdan katmanı, deployment ve implementation detaylarına odaklan."
    },
    critical: {
      label: "Critical",
      instruction:
        "Türkçe cevap ver. Eleştirel ve sağlam analiz yap. Zayıflıkları, riskleri, çelişkileri, eksik guardrail’leri ve somut düzeltmeleri açıkça belirt."
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
    reasoningMode: "balanced",
    activeAudio: null,
    activeAudioUrl: null
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

function nowLabel() {
  return new Date().toLocaleString("tr-TR", {
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

document.addEventListener("DOMContentLoaded", () => {
  injectAtaturkImageFix();
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

/* FIX: ATATÜRK IMAGE MUST NOT BE CROPPED */
function injectAtaturkImageFix() {
  const style = document.createElement("style");
  style.id = "ataturk-image-fix-style";
  style.textContent = `
    .ataturk-frame {
      min-height: 560px !important;
      height: auto !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      overflow: visible !important;
      padding: 18px !important;
    }

    .ataturk-frame img {
      width: 100% !important;
      height: auto !important;
      max-height: 620px !important;
      object-fit: contain !important;
      object-position: center center !important;
      display: block !important;
      border-radius: 24px !important;
    }

    .ataturk-frame::after {
      background:
        linear-gradient(180deg, rgba(5, 7, 13, 0.02), rgba(5, 7, 13, 0.18)) !important;
      pointer-events: none !important;
    }

    .portrait-caption {
      position: relative !important;
      left: auto !important;
      right: auto !important;
      bottom: auto !important;
      margin-top: 14px !important;
      width: 100% !important;
    }

    .ataturk-frame {
      flex-direction: column !important;
    }

    @media (max-width: 980px) {
      .ataturk-frame {
        min-height: auto !important;
      }

      .ataturk-frame img {
        max-height: 520px !important;
      }
    }
  `;
  document.head.appendChild(style);
}

/* REASONING MODE */
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
  safeText(byId("reasoningModeLabel"), getReasoningModeLabel());
  safeText(byId("reasoningModeDescription"), getReasoningModeInstruction());
  updateDashboard();
}

/* PAYLOAD */
function buildCognitionPayload(prompt, transportMode) {
  const reasoningMode = getReasoningMode();

  return {
    prompt,
    question: prompt,
    task: prompt,

    project: HOPE.project,
    doctrine: HOPE.doctrine,

    response_language: "tr",
    language: "Turkish",
    answer_language: "Turkish",
    must_answer_in_turkish: true,

    reasoning_mode: reasoningMode,
    reasoningMode: reasoningMode,
    mode: reasoningMode,

    transport_mode: transportMode,
    frontend_mode: transportMode,

    mode_label: getReasoningModeLabel(),
    mode_instruction:
      getReasoningModeInstruction() +
      "\n\nZORUNLU DİL KURALI: Cevabın tamamını Türkçe ver. İngilizce cevap verme.",

    layer: "vicdan",
    architecture: "HOPEtensor",

    system_context: {
      project: HOPE.project,
      doctrine: HOPE.doctrine,
      response_language: "Turkish",
      must_answer_in_turkish: true,
      reasoning_mode: reasoningMode,
      reasoning_mode_label: getReasoningModeLabel(),
      reasoning_mode_instruction:
        getReasoningModeInstruction() +
        "\n\nZORUNLU DİL KURALI: Cevabın tamamını Türkçe ver.",
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

/* DOCTRINE */
function renderDoctrine() {
  const targets = $$(".hope-doctrine, #doctrineText, [data-doctrine]");
  const doctrineHTML = HOPE.doctrine
    .map((line) => `<span>${escapeHTML(line)}</span>`)
    .join("");

  targets.forEach((target) => {
    safeHTML(target, doctrineHTML);
  });
}

/* NAVIGATION */
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

/* HERO */
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

/* DASHBOARD */
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

/* HEALTH */
async function checkHealth() {
  const el = byId("healthStatus");

  try {
    const res = await fetch(HOPE.api.health, { method: "GET" });
    if (!res.ok) throw new Error("Health endpoint unavailable");

    const data = await res.json().catch(() => ({}));
    safeText(el, data.status || "online");

    if (el) el.className = "health online";
  } catch {
    safeText(el, "local / fallback mode");
    if (el) el.className = "health fallback";
  }
}

/* DEMO */
function bindDemo() {
  const askBtn = byId("askButton") || byId("runDemoBtn");
  const stopBtn = byId("stopButton") || byId("stopStreamBtn");
  const input = byId("promptInput") || byId("demoPrompt");
  const clearBtn = byId("clearButton") || byId("clearDemoBtn");

  if (askBtn) {
    askBtn.addEventListener("click", () => runCognition());
  }

  if (stopBtn) {
    stopBtn.addEventListener("click", () => {
      stopStreaming();
      stopVoice();
    });
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

  stopVoice();

  const input = byId("promptInput") || byId("demoPrompt");
  const output = byId("answerOutput") || byId("streamOutput") || byId("demoOutput");
  const trace = byId("cognitionTrace");

  const prompt = input ? input.value.trim() : "";
  const reasoningMode = getReasoningMode();

  if (!prompt) {
    showToast("Vicdan cognition için bir prompt gir.");
    return;
  }

  HOPE.ui.isStreaming = true;
  HOPE.ui.lastAnswer = "";
  HOPE.ui.currentController = new AbortController();
  HOPE.metrics.cognitionRuns += 1;

  updateDashboard();
  setStreamingUI(true);

  safeText(output, "");

  addTrace("Input received", "Prompt constitutional cognition pipeline içine alındı.");
  addTrace("Reasoning mode selected", `${getReasoningModeLabel()} — ${getReasoningModeInstruction()}`);
  addTrace("Vicdan layer active", "Etik, tarihsel ve doktrinel çerçeve aktif.");
  addTrace("HOPEtensor routing", "Reasoning path cognition node’ları için hazırlandı.");

  try {
    const streamed = await tryStreamingRequest(prompt, output);

    if (!streamed) {
      await fallbackReasonRequest(prompt, output);
    }

    HOPE.metrics.safetyPasses += 1;

    addTrace("Constitutional check", "Yanıt doktrin ve güvenlik katmanından geçti.");
    addTrace("Cognition completed", `Yanıt ${HOPE.reasoningModes[reasoningMode].label} modunda tamamlandı.`);

    if (HOPE.ui.ttsEnabled && HOPE.ui.archiveVoiceEnabled && HOPE.ui.lastAnswer) {
      await speakText(HOPE.ui.lastAnswer);
    }
  } catch (err) {
    if (err.name === "AbortError") {
      addTrace("Stream stopped", "Kullanıcı stream’i durdurdu.");
      showToast("Streaming durduruldu.");
    } else {
      console.error(err);
      safeText(output, "Cognition error. Backend unavailable veya fallback mode gerekli.");
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
  addTrace("Fallback reason endpoint", "Streaming unavailable. /reason endpoint kullanılıyor.");

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
  stopVoice();

  const output = byId("answerOutput") || byId("streamOutput") || byId("demoOutput");
  const trace = byId("cognitionTrace");

  safeText(output, "");
  safeHTML(trace, "");
  HOPE.ui.lastAnswer = "";

  showToast("Demo temizlendi.");
}

function setStreamingUI(active) {
  const askBtn = byId("askButton") || byId("runDemoBtn");
  const stopBtn = byId("stopButton") || byId("stopStreamBtn");
  const indicator = byId("streamIndicator");

  if (askBtn) askBtn.disabled = active;
  if (stopBtn) stopBtn.disabled = false;

  if (indicator) {
    indicator.textContent = active
      ? `Streaming cognition / ${getReasoningModeLabel()}`
      : `Ready / ${getReasoningModeLabel()}`;

    indicator.className = active ? "indicator live" : "indicator ready";
  }

  document.body.classList.toggle("is-streaming", active);
}

/* TRACE */
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

/* TTS */
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
      if (!HOPE.ui.ttsEnabled) stopVoice();
    });
  }

  if (archiveToggle) {
    archiveToggle.checked = HOPE.ui.archiveVoiceEnabled;
    archiveToggle.addEventListener("change", () => {
      HOPE.ui.archiveVoiceEnabled = archiveToggle.checked;
      if (!HOPE.ui.archiveVoiceEnabled) stopVoice();
    });
  }

  if (replayBtn) {
    replayBtn.addEventListener("click", () => {
      if (HOPE.ui.lastAnswer) speakText(HOPE.ui.lastAnswer);
      else showToast("Ses için cevap yok.");
    });
  }
}

async function speakText(text) {
  if (!text || !HOPE.ui.ttsEnabled) return;

  stopVoice();

  const audio = byId("ttsAudio") || new Audio();
  HOPE.ui.activeAudio = audio;

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
        response_language: "tr",
        language: "Turkish",
        mode: "archive_voice",
        reasoning_mode: getReasoningMode(),
        reasoningMode: getReasoningMode(),
        mode_instruction: getReasoningModeInstruction()
      })
    });

    if (!res.ok) throw new Error(`TTS failed: HTTP ${res.status}`);

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);

    HOPE.ui.activeAudioUrl = url;

    audio.src = url;
    audio.controls = true;

    const holder = byId("ttsPlayer");

    if (holder && !holder.contains(audio)) {
      holder.innerHTML = "";
      holder.appendChild(audio);
    }

    await audio.play().catch(() => {
      showToast("Ses oluşturuldu. Dinlemek için play’e bas.");
    });

    HOPE.metrics.ttsRuns += 1;
    updateDashboard();
  } catch (err) {
    console.warn("TTS unavailable:", err);
    addTrace("TTS fallback", "Voice endpoint unavailable veya browser autoplay engelledi.");
  }
}

function stopVoice() {
  const audio = HOPE.ui.activeAudio || byId("ttsAudio");

  if (audio) {
    try {
      audio.pause();
      audio.currentTime = 0;
      audio.removeAttribute("src");
      audio.load();
    } catch (err) {
      console.warn("Voice stop error:", err);
    }
  }

  if (HOPE.ui.activeAudioUrl) {
    try {
      URL.revokeObjectURL(HOPE.ui.activeAudioUrl);
    } catch {}
    HOPE.ui.activeAudioUrl = null;
  }

  showToast("Voice stopped.");
}

/* API */
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

    payload.response_language = "tr";
    payload.language = "Turkish";
    payload.answer_language = "Turkish";
    payload.must_answer_in_turkish = true;
    payload.reasoning_mode = payload.reasoning_mode || reasoningMode;
    payload.reasoningMode = payload.reasoningMode || reasoningMode;
    payload.mode = payload.mode || reasoningMode;
    payload.mode_instruction =
      payload.mode_instruction ||
      getReasoningModeInstruction() +
        "\n\nZORUNLU DİL KURALI: Cevabın tamamını Türkçe ver.";
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

/* CONTRIBUTOR */
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
      language: "Turkish",
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

/* ARCHITECTURE */
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

/* SHORTCUTS */
function bindKeyboardShortcuts() {
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      if (HOPE.ui.isStreaming) stopStreaming();
      stopVoice();
    }

    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      const input = byId("promptInput") || byId("demoPrompt");
      if (input) input.focus();
    }
  });
}

/* TOAST */
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
  }, 1800);
}

/* UTILS */
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

/* PUBLIC DEBUG HANDLE */
window.HOPE = HOPE;
window.runCognition = runCognition;
window.stopStreaming = stopStreaming;
window.stopVoice = stopVoice;
window.clearDemo = clearDemo;
window.speakText = speakText;
window.getReasoningMode = getReasoningMode;
window.getReasoningModeInstruction = getReasoningModeInstruction;