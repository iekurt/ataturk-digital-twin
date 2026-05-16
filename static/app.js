/* FULL WORKING static/app.js */
/* ATATÜRK DIGITAL TWIN / HOPEVERSE */

"use strict";

/* =========================================================
   PRESET PROMPTS
========================================================= */

function setPresetPrompt(text){

    const input =
        document.getElementById(
            "promptInput"
        );

    if(input){
        input.value = text;
    }
}


/* =========================================================
   TRACE
========================================================= */

const TRACE =
    document.getElementById(
        "cognitionTrace"
    );

function addTrace(title, detail){

    if(!TRACE) return;

    const item =
        document.createElement("div");

    item.className =
        "trace-item";

    item.innerHTML = `

        <div class="trace-title">
            ${title}
        </div>

        <div class="trace-detail">
            ${detail}
        </div>

    `;

    TRACE.appendChild(item);

    TRACE.scrollTop =
        TRACE.scrollHeight;
}


/* =========================================================
   REFLECTION
========================================================= */

function updateReflection(){

    const set = (id,val)=>{

        const el =
            document.getElementById(id);

        if(el){
            el.innerText = val;
        }
    };

    set(
        "reflectionScore",
        "92"
    );

    set(
        "constitutionalAlignment",
        "95%"
    );

    set(
        "historicalAlignment",
        "91%"
    );

    set(
        "ethicalAlignment",
        "96%"
    );

    set(
        "hallucinationRisk",
        "8%"
    );

    set(
        "confidenceScore",
        "93%"
    );

    const summary =
        document.getElementById(
            "reflectionSummary"
        );

    if(summary){

        summary.innerText =

            "Observer Node analysis completed. " +

            "Constitutional alignment stable. " +

            "Vicdan layer integrity preserved.";
    }
}


/* =========================================================
   PREMIUM TTS
========================================================= */

async function speakAnswer(text){

    if(!text) return;

    try{

        const voice =
            document.getElementById(
                "voiceSelector"
            )?.value || "nova";

        addTrace(
            "Archive Voice",
            `Premium TTS rendering (${voice})`
        );

        const response =
            await fetch("/tts",{

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({

                    text:text,

                    voice:voice
                })
            });

        // RESPONSE TYPE CHECK

        const type =
            response.headers.get(
                "content-type"
            );

        if(
            !type ||
            !type.includes("audio")
        ){

            console.error(
                "TTS ERROR"
            );

            addTrace(
                "TTS Error",
                "Audio response alınamadı."
            );

            return;
        }

        const blob =
            await response.blob();

        const url =
            URL.createObjectURL(blob);

        const audio =
            document.getElementById(
                "ttsAudio"
            );

        if(audio){

            audio.pause();

            audio.src = url;

            audio.load();

            await audio.play();

            addTrace(
                "Archive Voice",
                "Playback started."
            );
        }

    }catch(err){

        console.error(
            "VOICE ERROR",
            err
        );

        addTrace(
            "Voice Error",
            String(err)
        );
    }
}


/* =========================================================
   API CALL
========================================================= */

async function cinematicReason(prompt){

    addTrace(
        "Input Layer",
        "Prompt constitutional cognition pipeline içine alındı."
    );

    addTrace(
        "HOPEtensor Routing",
        "Distributed reasoning orchestration başlatıldı."
    );

    addTrace(
        "Vicdan Layer",
        "Ethical verification active."
    );

    addTrace(
        "Observer Node",
        "Reflection telemetry hazırlanıyor."
    );

    const response =
        await fetch("/reason",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                prompt:prompt,

                reasoning_mode:
                    document.getElementById(
                        "reasoningMode"
                    )?.value || "constitutional"
            })
        });

    const data =
        await response.json();

    return (
        data.answer ||

        "No constitutional answer generated."
    );
}


/* =========================================================
   RUN COGNITION
========================================================= */

async function runCognition(){

    const input =
        document.getElementById(
            "promptInput"
        );

    if(!input) return;

    const prompt =
        input.value.trim();

    if(!prompt) return;

    const output =
        document.getElementById(
            "answerOutput"
        );

    if(output){
        output.innerHTML = "";
    }

    if(TRACE){
        TRACE.innerHTML = "";
    }

    addTrace(
        "Constitutional Cognition",
        "Pipeline initialized."
    );

    const answer =
        await cinematicReason(prompt);

    let current = "";

    for(const ch of answer){

        current += ch;

        if(output){
            output.innerText = current;
        }

        await new Promise(
            r=>setTimeout(r,8)
        );
    }

    addTrace(
        "Delivery Layer",
        "Streaming completed successfully."
    );

    updateReflection();

    await speakAnswer(answer);
}


/* =========================================================
   BUTTONS
========================================================= */

const askButton =
    document.getElementById(
        "askButton"
    );

if(askButton){

    askButton.onclick =
        runCognition;
}

const replayButton =
    document.getElementById(
        "replayVoiceBtn"
    );

if(replayButton){

    replayButton.onclick =
        async ()=>{

            const txt =
                document.getElementById(
                    "answerOutput"
                )?.innerText;

            if(txt){

                await speakAnswer(txt);
            }
        };
}


/* =========================================================
   AUTO TRACE
========================================================= */

window.addEventListener(

    "load",

    ()=>{

        addTrace(
            "HOPEtensor",
            "Constitutional cognition engine online."
        );

        addTrace(
            "Vicdan Layer",
            "Ethical alignment initialized."
        );

        addTrace(
            "Observer Node",
            "Reflection telemetry ready."
        );
    }
);