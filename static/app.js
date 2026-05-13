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

  ui: {
    isStreaming: false,
    currentController: null,
    ttsController: null,
    lastAnswer: "",
    selectedVoice: "alloy",
    archiveVoiceEnabled: true,
    activeAudio: null,
    activeAudioUrl: null
  }
};

/* ---------------- HELPERS ---------------- */

function byId(id) {
  return document.getElementById(id);
}

function safeText(el, text) {
  if (el) {
    el.textContent = text;
  }
}

function escapeHTML(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function showToast(message) {
  let toast = byId("hopeToast");

  if (!toast) {
    toast = document.createElement("div");
    toast.id = "hopeToast";
    document.body.appendChild(toast);
  }

  toast.textContent = message;
}

/* ---------------- INIT ---------------- */

document.addEventListener("DOMContentLoaded", () => {
  bindReasoningMode();
  bindDemo();
  bindTTSControls();
  resetReflectionPanel();
  checkHealth();
});

/* ---------------- REASONING ---------------- */

function bindReasoningMode() {
  const select = byId("reasoningMode");

  if (!select) return;

  select.addEventListener("change", () => {
    showToast(`Reasoning Mode: ${select.value}`);
  });
}

function getReasoningMode() {
  const select = byId("reasoningMode");

  if (!select) {
    return "balanced";
  }

  return select.value || "balanced";
}

/* ---------------- HEALTH ---------------- */

async function checkHealth() {
  try {
    const res = await fetch("/health");

    if (!res.ok) {
      throw new Error();
    }

    const data = await res.json();

    safeText(
      byId("healthStatus"),
      data.status || "online"
    );

  } catch {
    safeText(
      byId("healthStatus"),
      "fallback"
    );
  }
}

/* ---------------- REFLECTION ---------------- */

function resetReflectionPanel() {
  setReflectionValue("reflectionScore", "—");
  setReflectionValue("constitutionalAlignment", "—");
  setReflectionValue("historicalAlignment", "—");
  setReflectionValue("ethicalAlignment", "—");
  setReflectionValue("hallucinationRisk", "—");
  setReflectionValue("confidenceScore", "—");

  safeText(
    byId("reflectionSummary"),
    "Self-Reflection Node is waiting for cognition output."
  );
}

function setReflectionValue(id, value) {
  const el = byId(id);

  if (!el) return;

  el.textContent = value;
}

function updateReflectionPanel(reflection) {
  if (!reflection) return;

  setReflectionValue(
    "reflectionScore",
    reflection.reflection_score ?? 0
  );

  setReflectionValue(
    "constitutionalAlignment",
    reflection.constitutional_alignment ?? 0
  );

  setReflectionValue(
    "historicalAlignment",
    reflection.historical_alignment ?? 0
  );

  setReflectionValue(
    "ethicalAlignment",
    reflection.ethical_alignment ?? 0
  );

  setReflectionValue(
    "hallucinationRisk",
    reflection.hallucination_risk ?? 0
  );

  setReflectionValue(
    "confidenceScore",
    reflection.confidence_score ?? 0
  );

  safeText(
    byId("reflectionSummary"),
    reflection.summary || "Reflection completed."
  );

  addTrace(
    "Self-Reflection Node",
    reflection.summary || "Reflection completed."
  );
}

/* ---------------- TRACE ---------------- */

function addTrace(title, detail) {
  const trace = byId("cognitionTrace");

  if (!trace) return;

  const item = document.createElement("div");

  item.className = "trace-item";

  item.innerHTML = `
    <div class="trace-time">
      ${new Date().toLocaleTimeString("tr-TR")}
    </div>

    <div class="trace-title">
      ${escapeHTML(title)}
    </div>

    <div class="trace-detail">
      ${escapeHTML(detail)}
    </div>
  `;

  trace.appendChild(item);

  trace.scrollTop = trace.scrollHeight;
}

/* ---------------- PAYLOAD ---------------- */

function buildPayload(prompt) {
  return {
    prompt,
    question: prompt,
    task: prompt,

    response_language: "tr",
    language: "Turkish",
    answer_language: "Turkish",
    must_answer_in_turkish: true,

    reasoning_mode: getReasoningMode(),
    reasoningMode: getReasoningMode(),
    mode: getReasoningMode(),

    architecture: "HOPEtensor",
    layer: "vicdan"
  };
}

/* ---------------- DEMO ---------------- */

function bindDemo() {
  const askBtn = byId("askButton");
  const stopBtn = byId("stopButton");

  if (askBtn) {
    askBtn.addEventListener("click", runCognition);
  }

  if (stopBtn) {
    stopBtn.addEventListener("click", () => {
      stopStreaming();
      stopVoice();
    });
  }
}

async function runCognition() {
  if (HOPE.ui.isStreaming) return;

  resetReflectionPanel();

  const input = byId("promptInput");
  const output = byId("answerOutput");
  const trace = byId("cognitionTrace");

  if (trace) {
    trace.innerHTML = "";
  }

  const prompt = input ? input.value.trim() : "";

  if (!prompt) {
    showToast("Prompt gir.");
    return;
  }

  safeText(output, "");

  addTrace(
    "Input received",
    "Prompt cognition pipeline içine alındı."
  );

  addTrace(
    "Reasoning mode",
    getReasoningMode()
  );

  addTrace(
    "Vicdan layer",
    "Constitutional cognition active."
  );

  addTrace(
    "HOPEtensor routing",
    "Distributed reasoning path initialized."
  );

  HOPE.ui.isStreaming = true;
  HOPE.ui.lastAnswer = "";
  HOPE.ui.currentController = new AbortController();

  try {
    const res = await fetch("/stream", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        "Accept": "text/event-stream"
      },

      body: JSON.stringify(
        buildPayload(prompt)
      ),

      signal: HOPE.ui.currentController.signal
    });

    if (!res.ok || !res.body) {
      throw new Error("Stream unavailable");
    }

    const reader = res.body.getReader();

    const decoder = new TextDecoder("utf-8");

    let buffer = "";

    while (true) {
      const { value, done } = await reader.read();

      if (done) break;

      buffer += decoder.decode(value, {
        stream: true
      });

      const chunks = buffer.split("\n\n");

      buffer = chunks.pop() || "";

      for (const chunk of chunks) {
        processSSEChunk(chunk, output);
      }
    }

    addTrace(
      "Cognition completed",
      "Streaming response finalized."
    );

    if (HOPE.ui.archiveVoiceEnabled) {
      await speakText(HOPE.ui.lastAnswer);
    }

  } catch (err) {
    console.error(err);

    addTrace(
      "Stream error",
      err.message || "Unknown stream error."
    );

    safeText(
      output,
      "Cognition stream error."
    );

  } finally {
    HOPE.ui.isStreaming = false;
    HOPE.ui.currentController = null;
  }
}

/* ---------------- STREAM ---------------- */

function processSSEChunk(chunk, output) {
  const lines = chunk.split(/\r?\n/);

  for (const line of lines) {
    const trimmed = line.trim();

    if (!trimmed.startsWith("data:")) {
      continue;
    }

    const raw = trimmed.replace(/^data:\s*/, "");

    if (raw === "[DONE]") {
      continue;
    }

    try {
      const json = JSON.parse(raw);

      if (json.reflection) {
        updateReflectionPanel(
          json.reflection
        );

        continue;
      }

      const token =
        json.token ||
        json.delta ||
        json.text ||
        json.content ||
        "";

      if (token) {
        appendToken(output, token);
      }

    } catch {
      appendToken(output, raw);
    }
  }
}

function appendToken(output, token) {
  HOPE.ui.lastAnswer += token;

  if (output) {
    output.textContent += token;
    output.scrollTop = output.scrollHeight;
  }
}

function stopStreaming() {
  if (HOPE.ui.currentController) {
    HOPE.ui.currentController.abort();
  }
}

/* ---------------- TTS ---------------- */

function bindTTSControls() {
  ensureAudioPlayer();

  const replayBtn = byId("replayVoiceBtn");

  if (replayBtn) {
    replayBtn.addEventListener("click", async () => {
      if (HOPE.ui.lastAnswer) {
        await speakText(
          HOPE.ui.lastAnswer
        );
      }
    });
  }
}

function ensureAudioPlayer() {
  let audio = byId("ttsAudio");

  if (!audio) {
    audio = document.createElement("audio");

    audio.id = "ttsAudio";

    audio.controls = true;

    document.body.appendChild(audio);
  }

  HOPE.ui.activeAudio = audio;

  return audio;
}

async function speakText(text) {
/* PLAY ARCHIVE VOICE FIX — static/app.js FULL PATCHED FUNCTION */

async function speakText(text) {
  if (!text) return;

  stopVoice(false);

  HOPE.ui.ttsController =
    new AbortController();

  try {
    addTrace(
      "OpenAI TTS",
      "Archive voice generation started."
    );

    const res = await fetch("/tts", {
      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify({
        text: text,
        voice: HOPE.ui.selectedVoice || "alloy",
        format: "mp3",
        response_language: "tr",
        language: "Turkish"
      }),

      signal: HOPE.ui.ttsController.signal
    });

    if (!res.ok) {
      const errText =
        await res.text().catch(() => "");

      throw new Error(
        `TTS failed: HTTP ${res.status} ${errText}`
      );
    }

    const blob = await res.blob();

    if (!blob || blob.size === 0) {
      throw new Error(
        "TTS returned empty audio blob."
      );
    }

    const audio =
      ensureAudioPlayer();

    if (HOPE.ui.activeAudioUrl) {
      URL.revokeObjectURL(
        HOPE.ui.activeAudioUrl
      );
    }

    const url =
      URL.createObjectURL(blob);

    HOPE.ui.activeAudioUrl = url;

    audio.pause();
    audio.currentTime = 0;

    audio.src = url;

    audio.load();

    const playPromise =
      audio.play();

    if (playPromise !== undefined) {
      await playPromise;
    }

    addTrace(
      "Archive Voice",
      "Voice playback started."
    );

  } catch (err) {
    console.error(err);

    addTrace(
      "TTS error",
      err.message || "Voice playback error."
    );

    showToast(
      "Archive Voice failed."
    );
  }
}
}

function stopVoice(show = true) {
  if (HOPE.ui.ttsController) {
    HOPE.ui.ttsController.abort();
  }

  const audio = HOPE.ui.activeAudio;

  if (audio) {
    audio.pause();
    audio.currentTime = 0;
  }

  if (show) {
    showToast("Voice stopped.");
  }
}

/* ---------------- DEBUG ---------------- */

window.HOPE = HOPE;
window.runCognition = runCognition;
window.stopStreaming = stopStreaming;
window.stopVoice = stopVoice;
window.updateReflectionPanel = updateReflectionPanel;
