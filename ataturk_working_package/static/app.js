async function runDemo(){

const prompt = document.getElementById("promptInput").value;

const res = await fetch("/reason",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
prompt:prompt
})
});

const data = await res.json();

document.getElementById("output").innerText = data.answer;
}
