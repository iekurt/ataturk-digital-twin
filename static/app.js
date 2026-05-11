let latestResponse = "";
let speaking = false;
let generatingVoice = false;
let currentAudio = null;
let currentAudioUrl = null;
let currentUtterance = null;
let availableVoices = [];

function safeGet(id) {
  return document.getElementById(id);
}

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
  const loader = safeGet("loader");
  const status = safeGet("engineStatus");

  if (isLoading) {
    if (loader) loader.classList.remove("hidden");
    if (status) status.textContent = message || "Running";
    setAvatarSpeaking(true);
  } else {
    if (loader) loader.classList.add("hidden");
    if (!speaking && !generatingVoice) setAvatarSpeaking(false);
  }
}

function setOutput(text) {
  latestResponse = text || "";
  const box = safeGet("responseBox");
  if (box) box.textContent = latestResponse;
  updateAvatarSpeech(latestResponse);
}

function appendOutput(text) {
  latestResponse += text || "";
  const box = safeGet("responseBox");
  if (box) box.textContent += text || "";

  if (latestResponse.length % 120 < (text || "").length) {
    updateAvatarSpeech(latestResponse.slice(-260));
  }
}

function setMeta({ status, mode, score }) {
  const engineStatus = safeGet("engineStatus");
  const modeBadge = safeGet("modeBadge");
  const vicdanScore = safeGet("vicdanScore");

  if (status && engineStatus) engineStatus.textContent = status;
  if (mode && modeBadge) modeBadge.textContent = mode;

  if (score !== undefined && score !== null && vicdanScore) {
    vicdanScore.textContent = `${score}/100`;
  }
}

function updateAvatarSpeech(text) {
  const speech = safeGet("avatarSpeech");
  if (!speech) return;

  if (!text || text.trim().length === 0) {
    speech.textContent = "Hazırım. Sorunuzu anayasal düşünme süzgecinden geçireceğim.";
    return;
  }

  const clean = text.replace(/\s+/g, " ").trim();
  speech.textContent = clean.length > 220 ? clean.slice(0, 220) + "..." : clean;
}

function setAvatarSpeaking(active) {
  const mouth = safeGet("avatarMouth");
  if (!mouth) return;

  if (active || speaking || generatingVoice) {
    mouth.classList.add("speaking");
  } else {
    mouth.classList.remove("speaking");
  }
}

async function ask() {
  const question = safeGet("q").value;
  const mode = safeGet("mode").value;

  stopSpeaking();

  latestResponse = "";

  setMeta({
    status: "Initializing",
    mode,
    score: null
  });

  setOutput("");
  setLoading(true, "Streaming");

  try {
    const res = await fetch("/stream", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        question,
        mode
      })
    });

    if (!res.ok) {
      throw new Error(`Backend error: ${res.status}`);
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let buffer = "";

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });

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
          setMeta({
            status: "Completed",
            mode
          });
        }

        if (data.type === "error") {
          throw new Error(data.message);
        }
      }
    }
  } catch (error) {
    setMeta({
      status: "Error",
      mode,
      score: null
    });

    setOutput(
      "Streaming engine error.\n\n" +
      error.message +
      "\n\nCheck Render logs, OPENAI_API_KEY, /stream endpoint and backend status."
    );
  } finally {
    setLoading(false);
  }
}

async function checkVicdan() {
  const question = safeGet("q").value;
  const mode = safeGet("mode").value;

  stopSpeaking();

  setMeta({
    status: "Vicdan Review",
    mode,
    score: null
  });

  setOutput("Running Vicdan ethical review...");
  setLoading(true, "Reviewing");

  try {
    const res = await fetch("/vicdan", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        question,
        mode
      })
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
    setMeta({
      status: "Error",
      mode,
      score: null
    });

    setOutput("Vicdan check error.\n\n" + error.message);
  } finally {
    setLoading(false);
  }
}

async function clearMemory() {
  stopSpeaking();

  const mode = safeGet("mode").value;

  setMeta({
    status: "Memory Reset",
    mode,
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
  const mode = safeGet("mode").value;

  if (generatingVoice || speaking || currentAudio || currentUtterance) {
    setMeta({
      status: "Already Speaking",
      mode
    });
    updateAvatarSpeech("Ses zaten çalışıyor. Önce Stop Voice ile durdurun.");
    return;
  }

  if (!("speechSynthesis" in window)) {
    setMeta({
      status: "Local Voice Unsupported",
      mode
    });
    updateAvatarSpeech("Bu tarayıcı local seslendirmeyi desteklemiyor.");
    return;
  }

  let text =
    latestResponse ||
    (safeGet("responseBox") ? safeGet("responseBox").textContent : "") ||
    "";

  text = text.trim();

  if (!text || text === "Live response will appear here.") {
    setOutput("Seslendirilecek cevap yok. Önce cevap üret.");
    return;
  }

  loadVoices();

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

  currentUtterance = new SpeechSynthesisUtterance(text);
  currentUtterance.lang = "tr-TR";
  currentUtterance.rate = 0.88;
  currentUtterance.pitch = 0.78;
  currentUtterance.volume = 1;

  if (trVoice) {
    currentUtterance.voice = trVoice;
  }

  currentUtterance.onstart = () => {
    speaking = true;
    setAvatarSpeaking(true);
    setMeta({
      status: "Speaking Local Voice",
      mode
    });
  };

  currentUtterance.onend = () => {
    currentUtterance = null;
    speaking = false;
    setAvatarSpeaking(false);
    setMeta({
      status: "Completed",
      mode
    });
  };

  currentUtterance.onerror = (event) => {
    currentUtterance = null;
    speaking = false;
    setAvatarSpeaking(false);
    setMeta({
      status: "Local Voice Error",
      mode
    });
    updateAvatarSpeech("Local seslendirme hatası: " + (event.error || "unknown"));
  };

  window.speechSynthesis.cancel();

  setTimeout(() => {
    window.speechSynthesis.speak(currentUtterance);
  }, 120);
}

function playArchivalVoice() {
  const mode = safeGet("mode").value;

  if (generatingVoice || speaking || currentAudio || currentUtterance) {
    setMeta({
      status: "Already Speaking",
      mode
    });
    updateAvatarSpeech("Ses zaten çalışıyor. Önce Stop Voice ile durdurun.");
    return;
  }

  const audioUrl =
    "/static/ataturk-archival-voice.mp3?v=" +
    Date.now();

  setMeta({
    status: "Starting Archival Voice",
    mode
  });

  updateAvatarSpeech("Gerçek tarihî arşiv kaydı başlatılıyor.");

  currentAudio = new Audio(audioUrl);
  currentAudio.preload = "auto";
  currentAudio.volume = 1;

  currentAudio.onplay = () => {
    speaking = true;
    setAvatarSpeaking(true);
    updateAvatarSpeech("Gerçek tarihî arşiv kaydı oynatılıyor.");
    setMeta({
      status: "Playing Archival Voice",
      mode
    });
  };

  currentAudio.onended = () => {
    cleanupAudio();
    setMeta({
      status: "Completed",
      mode
    });
    updateAvatarSpeech("Arşiv sesi tamamlandı.");
  };

  currentAudio.onerror = () => {
    cleanupAudio();
    updateAvatarSpeech(
      "Arşiv sesi oynatılamadı. Dosya yolu: /static/ataturk-archival-voice.mp3"
    );
    setMeta({
      status: "Archive Voice Error",
      mode
    });
  };

  currentAudio.play().catch((err) => {
    cleanupAudio();
    updateAvatarSpeech("Arşiv sesi oynatılamadı: " + err.message);
    setMeta({
      status: "Archive Voice Error",
      mode
    });
  });
}

function cleanupAudio() {
  if (currentAudio) {
    try {
      currentAudio.pause();
      currentAudio.src = "";
      currentAudio.load();
    } catch (e) {
      console.warn("Audio cleanup warning:", e);
    }
  }

  if (currentAudioUrl) {
    try {
      URL.revokeObjectURL(currentAudioUrl);
    } catch (e) {
      console.warn("URL revoke warning:", e);
    }
  }

  currentAudio = null;
  currentAudioUrl = null;
  speaking = false;
  generatingVoice = false;
  setAvatarSpeaking(false);
}

function stopSpeaking() {
  cleanupAudio();

  if ("speechSynthesis" in window) {
    try {
      window.speechSynthesis.cancel();
    } catch (e) {
      console.warn("Speech synthesis cancel warning:", e);
    }
  }

  currentUtterance = null;
  speaking = false;
  generatingVoice = false;
  setAvatarSpeaking(false);

  const modeElement = safeGet("mode");

  setMeta({
    status: "Stopped",
    mode: modeElement ? modeElement.value : "constitutional"
  });

  updateAvatarSpeech("Ses durduruldu.");
}