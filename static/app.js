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
    ttsEnabled: true,
    archiveVoiceEnabled: true,
    activeAudio: null,
    activeAudioUrl: null,
    lastReflection: null
  }
};

function byId(id) {
  return document.getElementById(id);
}

function safeText(el, text) {
  if (el) el.textContent = text;
}

function escapeHTML(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

document.addEventListener("DOMContentLoaded", () => {
  bindReasoningMode();
  bindDemo();
  bindTTSControls();
  resetReflectionPanel();
  checkHealth();
});

/* ---------------- REASONING MODE ---------------- */

function bindReasoningMode() {
  const select = byId("reasoningMode");
  if (!select) return;

  select.addEventListener("change", () => {
    showToast(`Reasoning Mode: ${select.value}`);
  });
}

function getReasoningMode() {
  const select = byId("reasoningMode");
  return select ? select.value : "balanced";
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

/* ---------------- HEALTH ---------------- */

async function checkHealth() {
  try {
    const res = await fetch("/health");

    if (!res.ok) throw new Error();

    const data = await res.json();

    const el = byId("healthStatus");

    if (el) {
      el.textContent = data.status || "online";
    }
  } catch {
    const el = byId("healthStatus");

    if (el) {
      el.textContent = "fallback";
    }
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

  const prompt = input ? input.value.trim() : "";

  if (!prompt) {
    showToast("Prompt gir.");
    return;
  }

  safeText(output, "");

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
      body: JSON.stringify(buildPayload(prompt)),
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

      buffer += decoder.decode(value, { stream: true });

      const chunks = buffer.split("\n\n");
      buffer = chunks.pop() || "";

      for (const chunk of chunks) {
        processSSEChunk(chunk, output);
      }
    }

    if (HOPE.ui.archiveVoiceEnabled) {
      await speakText(HOPE.ui.lastAnswer);
    }

  } catch (err) {
    console.error(err);

    safeText(
      output,
      "Cognition stream error."
    );

  } finally {
    HOPE.ui.isStreaming = false;
    HOPE.ui.currentController = null;
  }
}

function processSSEChunk(chunk, output) {
  const lines = chunk.split(/\r?\n/);

  for (const line of lines) {
    const trimmed = line.trim();

    if (!trimmed.startsWith("data:")) continue;

    const raw = trimmed.replace(/^data:\s*/, "");

    if (raw === "[DONE]") continue;

    try {
      const json = JSON.parse(raw);

      if (json.reflection) {
        updateReflectionPanel(json.reflection);
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
        await speakText(HOPE.ui.lastAnswer);
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
  if (!text) return;

  stopVoice(false);

  HOPE.ui.ttsController = new AbortController();

  try {
    const res = await fetch("/tts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        text,
        voice: HOPE.ui.selectedVoice
      }),
      signal: HOPE.ui.ttsController.signal
    });

    if (!res.ok) {
      throw new Error("TTS failed");
    }

    const blob = await res.blob();

    const audio = ensureAudioPlayer();

    if (HOPE.ui.activeAudioUrl) {
      URL.revokeObjectURL(HOPE.ui.activeAudioUrl);
    }

    const url = URL.createObjectURL(blob);

    HOPE.ui.activeAudioUrl = url;

    audio.src = url;

    await audio.play();

  } catch (err) {
    console.error(err);
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

/* ---------------- TOAST ---------------- */

function showToast(message) {
  let toast = byId("hopeToast");

  if (!toast) {
    toast = document.createElement("div");
    toast.id = "hopeToast";
    document.body.appendChild(toast);
  }

  toast.textContent = message;
}

/* ---------------- DEBUG ---------------- */

window.HOPE = HOPE;
window.runCognition = runCognition;
window.stopStreaming = stopStreaming;
window.stopVoice = stopVoice;
window.updateReflectionPanel = updateReflectionPanel;