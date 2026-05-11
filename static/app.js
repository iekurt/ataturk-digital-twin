let latestResponse = "";
let speaking = false;
let availableVoices = [];

function loadVoices() {
  if ("speechSynthesis" in window) {
    availableVoices = window.speechSynthesis.getVoices();
  }
}

if ("speechSynthesis" in window) {
  loadVoices();
  window.speechSynthesis.onvoiceschanged = loadVoices;
}

function setLoading(isLoading, message = "") {
  const loader = document.getElementById("loader");
  const status = document.getElementById("engineStatus");

  if (isLoading) {
    loader.classList.remove("hidden");
    status.textContent = message || "Running";
    setAvatarSpeaking(true);
  } else {
    loader.classList.add("hidden");
    if (!speaking) setAvatarSpeaking(false);
  }
}

function setOutput(text) {
  latestResponse = text;
  document.getElementById("responseBox").textContent = text;
  updateAvatarSpeech(text);
}

function appendOutput(text) {
  latestResponse += text;
  const box = document.getElementById("responseBox");
  box.textContent += text;

  if (latestResponse.length % 120 < text.length) {
    updateAvatarSpeech(latestResponse.slice(-260));
  }
}

function setMeta({status, mode, score}) {
  if (status) document.getElementById("engineStatus").textContent = status;
  if (mode) document.getElementById("modeBadge").textContent = mode;
  if (score !== undefined && score !== null) {
    document.getElementById("vicdanScore").textContent = `${score}/100`;
  }
}

function updateAvatarSpeech(text) {
  const speech = document.getElementById("avatarSpeech");
  if (!speech) return;

  if (!text || text.trim().length === 0) {
    speech.textContent = "Hazırım. Sorunuzu anayasal düşünme süzgecinden geçireceğim.";
    return;
  }

  const clean = text.replace(/\s+/g, " ").trim();
  speech.textContent = clean.length > 220 ? clean.slice(0, 220) + "..." : clean;
}

function setAvatarSpeaking(active) {
  const mouth = document.getElementById("avatarMouth");
  if (!mouth) return;

  if (active || speaking) {
    mouth.classList.add("speaking");
  } else {
    mouth.classList.remove("speaking");
  }
}

async function ask() {
  const question = document.getElementById("q").value;
  const mode = document.getElementById("mode").value;

  stopSpeaking();

  latestResponse = "";
  setMeta({status: "Initializing", mode, score: null});
  setOutput("");
  setLoading(true, "Streaming");

  try {
    const res = await fetch("/stream", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({question, mode})
    });

    if (!res.ok) {
      throw new Error(`Backend error: ${res.status}`);
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let buffer = "";

    while (true) {
      const {value, done} = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, {stream: true});

      const events = buffer.split("\n\n");
      buffer = events.pop();

      for (const event of events) {
        if (!event.startsWith("data: ")) continue;

        const raw = event.replace("data: ", "").trim();
        if (!raw) continue;

        const data = JSON.parse(raw);

        if (data.type === "meta") {
          setMeta({
            status: "Streaming",
            mode: data.mode || mode,
            score: data.vicdan && data.vicdan.score
          });
        }

        if (data.type === "token") {
          appendOutput(data.token);
        }

        if (data.type === "done") {
          setMeta({status: "Completed", mode});
        }

        if (data.type === "error") {
          throw new Error(data.message);
        }
      }
    }
  } catch (error) {
    setMeta({status: "Error", mode, score: null});
    setOutput(
      "Streaming engine error.\n\n" +
      error.message +
      "\n\nCheck Render logs, OPENAI_API_KEY, /health, and /stream endpoint."
    );
  } finally {
    setLoading(false);
  }
}

async function checkVicdan() {
  const question = document.getElementById("q").value;
  const mode = document.getElementById("mode").value;

  stopSpeaking();

  setMeta({status: "Vicdan Review", mode, score: null});
  setOutput("Running Vicdan ethical review...");
  setLoading(true, "Reviewing");

  try {
    const res = await fetch("/vicdan", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({question, mode})
    });

    if (!res.ok) {
      throw new Error(`Backend error: ${res.status}`);
    }

    const data = await res.json();
    const score = data.review && data.review.score;

    setMeta({
      status: data.review ? data.review.status : "Completed",
      mode,
      score
    });

    setOutput(JSON.stringify(data, null, 2));
  } catch (error) {
    setMeta({status: "Error", mode, score: null});
    setOutput("Vicdan check error.\n\n" + error.message);
  } finally {
    setLoading(false);
  }
}

async function clearMemory() {
  stopSpeaking();

  setMeta({
    status: "Memory Reset",
    mode: document.getElementById("mode").value,
    score: null
  });

  setOutput("Clearing constitutional conversation memory...");

  try {
    const res = await fetch("/memory/clear", {
      method: "POST"
    });

    const data = await res.json();
    setOutput(JSON.stringify(data, null, 2));
  } catch (error) {
    setOutput("Memory clear error.\n\n" + error.message);
  }
}

function speakCurrentResponse() {
  if (!("speechSynthesis" in window)) {
    setOutput("Bu tarayıcı Speech Synthesis desteklemiyor.");
    return;
  }

  loadVoices();

  let text =
    latestResponse ||
    document.getElementById("responseBox").textContent ||
    "";

  text = text.trim();

  if (!text || text === "Live response will appear here.") {
    setOutput("Seslendirilecek cevap yok. Önce Run Live Avatar Engine ile cevap üret.");
    return;
  }

  stopSpeaking();

  setTimeout(() => {
    const utterance = new SpeechSynthesisUtterance(text);

    utterance.lang = "tr-TR";
    utterance.rate = 0.88;
    utterance.pitch = 0.78;
    utterance.volume = 1;

    const voices = availableVoices.length
      ? availableVoices
      : window.speechSynthesis.getVoices();

    const trVoice =
      voices.find(v => v.lang === "tr-TR") ||
      voices.find(v => v.lang && v.lang.toLowerCase().startsWith("tr")) ||
      voices.find(v => v.name && v.name.toLowerCase().includes("turkish")) ||
      voices.find(v => v.name && v.name.toLowerCase().includes("tolga")) ||
      voices.find(v => v.name && v.name.toLowerCase().includes("yelda")) ||
      voices[0];

    if (trVoice) {
      utterance.voice = trVoice;
    }

    utterance.onstart = () => {
      speaking = true;
      setAvatarSpeaking(true);
      setMeta({
        status: "Speaking",
        mode: document.getElementById("mode").value
      });
    };

    utterance.onend = () => {
      speaking = false;
      setAvatarSpeaking(false);
      setMeta({
        status: "Completed",
        mode: document.getElementById("mode").value
      });
    };

    utterance.onerror = (event) => {
      speaking = false;
      setAvatarSpeaking(false);
      setMeta({
        status: "Voice Error",
        mode: document.getElementById("mode").value
      });

      const originalText = text;
      setOutput(
        originalText +
        "\n\n[Voice Error: " +
        (event.error || "unknown") +
        "]"
      );
    };

    window.speechSynthesis.speak(utterance);
  }, 250);
}

function stopSpeaking() {
  if ("speechSynthesis" in window) {
    window.speechSynthesis.cancel();
  }

  speaking = false;
  setAvatarSpeaking(false);
}