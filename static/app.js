let latestResponse = "";
let speaking = false;
let availableVoices = [];
let currentAudio = null;

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

    if (!speaking) {
      setAvatarSpeaking(false);
    }
  }
}

function setOutput(text) {
  latestResponse = text;

  const box = document.getElementById("responseBox");

  if (box) {
    box.textContent = text;
  }

  updateAvatarSpeech(text);
}

function appendOutput(text) {
  latestResponse += text;

  const box = document.getElementById("responseBox");

  if (box) {
    box.textContent += text;
  }

  if (latestResponse.length % 120 < text.length) {
    updateAvatarSpeech(latestResponse.slice(-260));
  }
}

function setMeta({ status, mode, score }) {
  const engineStatus = document.getElementById("engineStatus");
  const modeBadge = document.getElementById("modeBadge");
  const vicdanScore = document.getElementById("vicdanScore");

  if (status && engineStatus) {
    engineStatus.textContent = status;
  }

  if (mode && modeBadge) {
    modeBadge.textContent = mode;
  }

  if (
    score !== undefined &&
    score !== null &&
    vicdanScore
  ) {
    vicdanScore.textContent = `${score}/100`;
  }
}

function updateAvatarSpeech(text) {
  const speech = document.getElementById("avatarSpeech");

  if (!speech) return;

  if (!text || text.trim().length === 0) {
    speech.textContent =
      "Hazırım. Sorunuzu anayasal düşünme süzgecinden geçireceğim.";
    return;
  }

  const clean = text.replace(/\s+/g, " ").trim();

  speech.textContent =
    clean.length > 220
      ? clean.slice(0, 220) + "..."
      : clean;
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

      buffer += decoder.decode(value, {
        stream: true
      });

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
            score:
              data.vicdan &&
              data.vicdan.score
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
  const question = document.getElementById("q").value;
  const mode = document.getElementById("mode").value;

  stopSpeaking();

  setMeta({
    status: "Vicdan Review",
    mode,
    score: null
  });

  setOutput(
    "Running Vicdan ethical review..."
  );

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

    const score =
      data.review &&
      data.review.score;

    setMeta({
      status:
        data.review
          ? data.review.status
          : "Completed",
      mode,
      score
    });

    setOutput(
      JSON.stringify(data, null, 2)
    );
  } catch (error) {
    setMeta({
      status: "Error",
      mode,
      score: null
    });

    setOutput(
      "Vicdan check error.\n\n" +
      error.message
    );
  } finally {
    setLoading(false);
  }
}

async function clearMemory() {
  stopSpeaking();

  setMeta({
    status: "Memory Reset",
    mode:
      document.getElementById("mode").value,
    score: null
  });

  setOutput(
    "Clearing constitutional conversation memory..."
  );

  try {
    const res = await fetch(
      "/memory/clear",
      {
        method: "POST"
      }
    );

    const data = await res.json();

    setOutput(
      JSON.stringify(data, null, 2)
    );
  } catch (error) {
    setOutput(
      "Memory clear error.\n\n" +
      error.message
    );
  }
}

async function speakCurrentResponse() {
  let text =
    latestResponse ||
    document.getElementById("responseBox")
      .textContent ||
    "";

  text = text.trim();

  if (
    !text ||
    text === "Live response will appear here."
  ) {
    setOutput(
      "Seslendirilecek cevap yok. Önce cevap üret."
    );
    return;
  }

  stopSpeaking();

  setMeta({
    status: "Generating AI Voice",
    mode:
      document.getElementById("mode").value
  });

  setAvatarSpeaking(true);

  try {
    const res = await fetch("/tts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        text,
        voice: "cedar"
      })
    });

    if (!res.ok) {
      throw new Error(
        `TTS backend error: ${res.status}`
      );
    }

    const audioBlob = await res.blob();

    const audioUrl =
      URL.createObjectURL(audioBlob);

    currentAudio = new Audio(audioUrl);

    currentAudio.preload = "auto";

    currentAudio.onplay = () => {
      speaking = true;

      setAvatarSpeaking(true);

      setMeta({
        status: "Speaking AI Narration",
        mode:
          document.getElementById("mode")
            .value
      });
    };

    currentAudio.onended = () => {
      speaking = false;

      setAvatarSpeaking(false);

      setMeta({
        status: "Completed",
        mode:
          document.getElementById("mode")
            .value
      });

      URL.revokeObjectURL(audioUrl);

      currentAudio = null;
    };

    currentAudio.onerror = () => {
      speaking = false;

      setAvatarSpeaking(false);

      setMeta({
        status: "Voice Error",
        mode:
          document.getElementById("mode")
            .value
      });

      setOutput(
        text +
        "\n\n[Voice Error: Audio playback failed.]"
      );

      URL.revokeObjectURL(audioUrl);

      currentAudio = null;
    };

    await currentAudio.play();
  } catch (error) {
    speaking = false;

    setAvatarSpeaking(false);

    setMeta({
      status: "Voice Error",
      mode:
        document.getElementById("mode").value
    });

    setOutput(
      text +
      "\n\n[Voice Error: " +
      error.message +
      "]"
    );
  }
}

function playArchivalVoice() {
  stopSpeaking();

  const audioUrl =
    "/static/ataturk-archival-voice.mp3?v=" +
    Date.now();

  setMeta({
    status: "Playing Archival Voice",
    mode:
      document.getElementById("mode").value
  });

  updateAvatarSpeech(
    "Gerçek tarihî arşiv kaydı oynatılıyor."
  );

  currentAudio = new Audio(audioUrl);

  currentAudio.preload = "auto";

  currentAudio.volume = 1;

  speaking = true;

  setAvatarSpeaking(true);

  currentAudio.play()
    .then(() => {
      setMeta({
        status: "Playing Archival Voice",
        mode:
          document.getElementById("mode")
            .value
      });
    })
    .catch((err) => {
      speaking = false;

      setAvatarSpeaking(false);

      updateAvatarSpeech(
        "Arşiv sesi oynatılamadı: " +
        err.message
      );

      setMeta({
        status: "Archive Voice Error",
        mode:
          document.getElementById("mode")
            .value
      });
    });

  currentAudio.onended = () => {
    speaking = false;

    setAvatarSpeaking(false);

    setMeta({
      status: "Completed",
      mode:
        document.getElementById("mode")
          .value
    });

    currentAudio = null;
  };
}

function stopSpeaking() {
  if (currentAudio) {
    try {
      currentAudio.pause();

      currentAudio.currentTime = 0;
    } catch (e) {
      console.warn(
        "Audio stop warning:",
        e
      );
    }

    currentAudio = null;
  }

  if ("speechSynthesis" in window) {
    window.speechSynthesis.cancel();
  }

  speaking = false;

  setAvatarSpeaking(false);
}