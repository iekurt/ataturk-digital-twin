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
  setOutput("Preparing constitutional cognition request...");
  setLoading(true, "Reasoning");

  try {
    const res = await fetch("/demo", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({question, mode})
    });

    if (!res.ok) {
      throw new Error(`Backend error: ${res.status}`);
    }

    const data = await res.json();

    setMeta({
      status: data.success ? "Completed" : "Failed",
      mode: data.mode || mode,
      score: data.vicdan && data.vicdan.score
    });

    setOutput(data.response || JSON.stringify(data, null, 2));
  } catch (error) {
    setMeta({status: "Error", mode, score: null});
    setOutput(
      "Engine error.\n\n" +
      error.message +
      "\n\nCheck Render logs, OPENAI_API_KEY, and /health endpoint."
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