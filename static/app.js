function setLoading(isLoading, message = "") {
  const loader = document.getElementById("loader");
  const status = document.getElementById("engineStatus");

  if (isLoading) {
    loader.classList.remove("hidden");
    status.textContent = message || "Running";
  } else {
    loader.classList.add("hidden");
  }
}

function setOutput(text) {
  document.getElementById("responseBox").textContent = text;
}

function appendOutput(text) {
  const box = document.getElementById("responseBox");
  box.textContent += text;
}

function setMeta({status, mode, score}) {
  if (status) document.getElementById("engineStatus").textContent = status;
  if (mode) document.getElementById("modeBadge").textContent = mode;
  if (score !== undefined && score !== null) {
    document.getElementById("vicdanScore").textContent = `${score}/100`;
  }
}

async function ask() {
  const question = document.getElementById("q").value;
  const mode = document.getElementById("mode").value;

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