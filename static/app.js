const TRACE=document.getElementById("cognitionTrace");

function addTrace(title,detail){

const item=document.createElement("div");

item.innerHTML=`
<b>${title}</b><br>${detail}<br><br>
`;

TRACE.appendChild(item);
}

async function speakAnswer(text){

const response=await fetch("/tts",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
text:text
})
});

const blob=await response.blob();

const url=URL.createObjectURL(blob);

const audio=document.getElementById("ttsAudio");

audio.src=url;

audio.preservesPitch=false;

audio.playbackRate=0.88;

audio.load();

await audio.play();
}

async function cinematicReason(prompt){

const output=document.getElementById("answerOutput");

output.innerHTML='<span class="live-cursor">█</span>';

const response=await fetch("/stream",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
prompt:prompt
})
});

const reader=response.body.getReader();

const decoder=new TextDecoder();

let fullText="";

while(true){

const {done,value}=await reader.read();

if(done) break;

const chunk=decoder.decode(value);

const lines=chunk.split("\\n");

for(const line of lines){

if(!line.startsWith("data:")) continue;

const payload=line.replace("data:","").trim();

if(payload==="[DONE]"){

await speakAnswer(fullText);

return;
}

try{

const parsed=JSON.parse(payload);

if(parsed.token){

fullText+=parsed.token;

output.innerHTML=
fullText +
'<span class="live-cursor">█</span>';
}

}catch(e){}
}
}
}

document.getElementById("askButton").onclick=async()=>{

TRACE.innerHTML="";

addTrace(
"Constitutional Cognition",
"Pipeline initialized."
);

const prompt=document.getElementById("promptInput").value;

await cinematicReason(prompt);
};

document.getElementById("replayVoiceBtn").onclick=()=>{

const audio=new Audio("/static/archive_voice.mp3");

audio.preservesPitch=false;

audio.playbackRate=0.88;

audio.play();

addTrace(
"Archive Voice",
"Historical archive playback active."
);
};
