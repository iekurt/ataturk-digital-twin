function setPresetPrompt(text){
document.getElementById("promptInput").value=text;
}

const answers = {
"Cumhuriyet reformlarının temel mantığı nedir?":
"Cumhuriyet reformlarının temel mantığı; akıl, bilim, laiklik, ulusal egemenlik ve çağdaşlaşma ekseninde modern bir toplum oluşturmaktır.",

"Laiklik neden önemlidir?":
"Laiklik devletin tüm yurttaşlara eşit mesafede durmasını sağlar. Hukukun üstünlüğünü ve özgür düşünceyi güçlendirir.",

"HOPEtensor mimarisi nasıl çalışır?":
"HOPEtensor; reasoning node, observer node, Vicdan layer ve self reflection node üzerinden dağıtık anayasal biliş mimarisi oluşturur.",

"Bilim neden medeniyetin temelidir?":
"Bilim üretim, teknoloji, eğitim ve kurumsal gelişimin temelidir. Bilim olmadan sürdürülebilir modernleşme mümkün değildir."
};

document.getElementById("askButton").addEventListener("click", async ()=>{

const input=document.getElementById("promptInput").value.trim();
const output=document.getElementById("answerOutput");

const answer=answers[input] || "Constitutional cognition active. Türkçe reasoning response generated.";

output.innerText=answer;

speak(answer);

});

document.getElementById("replayVoiceBtn").addEventListener("click", ()=>{
const txt=document.getElementById("answerOutput").innerText;
if(txt){ speak(txt); }
});

function speak(text){

if(!window.speechSynthesis) return;

window.speechSynthesis.cancel();

const utterance = new SpeechSynthesisUtterance(text);

utterance.lang="tr-TR";
utterance.rate=0.95;

window.speechSynthesis.speak(utterance);

}
