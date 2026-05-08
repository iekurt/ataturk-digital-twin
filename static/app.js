async function ask() {
  const question = document.getElementById("q").value;
  const mode = document.getElementById("mode").value;
  const out = document.getElementById("out");

  out.textContent = "Reasoning through constitutional cognition pipeline...";

  const res = await fetch("/demo", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({question, mode})
  });

  const data = await res.json();
  out.textContent = data.response;
}

async function checkVicdan() {
  const question = document.getElementById("q").value;
  const out = document.getElementById("out");

  out.textContent = "Running Vicdan ethical review...";

  const res = await fetch("/vicdan", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({question})
  });

  const data = await res.json();
  out.textContent = JSON.stringify(data, null, 2);
}