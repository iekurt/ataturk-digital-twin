/* =========================================
   static/app.js
   FULL LONG CINEMATIC VERSION
========================================= */

"use strict";


/* =========================================
   TRACE
========================================= */

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


/* =========================================
   PREMIUM TTS
========================================= */

async function speakAnswer(text){

    if(!text) return;

    try{

        addTrace(
            "Archive Voice",
            "Premium constitutional TTS rendering initialized."
        );

        const response =
            await fetch("/tts",{

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({
                    text:text
                })
            });

        const type =
            response.headers.get(
                "content-type"
            );

        if(
            !type ||
            !type.includes("audio")
        ){

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

        audio.pause();

        audio.src = url;

        audio.load();

        audio.playbackRate = 0.96;

        await audio.play();

        addTrace(
            "Archive Voice",
            "Constitutional voice playback active."
        );

    }catch(err){

        console.error(err);

        addTrace(
            "Voice Error",
            String(err)
        );
    }
}


/* =========================================
   SSE STREAMING
========================================= */

async function cinematicReason(prompt){

    addTrace(
        "Input Layer",
        "Prompt constitutional cognition pipeline içine alındı."
    );

    addTrace(
        "HOPEtensor Routing",
        "Distributed reasoning federation initialized."
    );

    addTrace(
        "Vicdan Layer",
        "Ethical verification active."
    );

    addTrace(
        "Observer Node",
        "Reflection telemetry hazırlanıyor."
    );

    const output =
        document.getElementById(
            "answerOutput"
        );

    output.innerHTML =
        '<span class="live-cursor">█</span>';

    const response =
        await fetch("/stream",{

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

    const reader =
        response.body.getReader();

    const decoder =
        new TextDecoder();

    let fullText = "";

    while(true){

        const {
            done,
            value
        } = await reader.read();

        if(done) break;

        const chunk =
            decoder.decode(value);

        const lines =
            chunk.split("\n");

        for(const line of lines){

            if(
                !line.startsWith("data:")
            ) continue;

            const payload =
                line.replace(
                    "data:",
                    ""
                ).trim();

            if(
                payload === "[DONE]"
            ){

                output.innerText =
                    fullText;

                addTrace(
                    "Delivery Layer",
                    "Streaming completed successfully."
                );

                await speakAnswer(
                    fullText
                );

                return fullText;
            }

            try{

                const parsed =
                    JSON.parse(payload);

                if(parsed.token){

                    fullText +=
                        parsed.token;

                    output.innerHTML =

                        fullText +

                        '<span class="live-cursor">█</span>';
                }

            }catch(err){

                console.error(err);
            }
        }
    }

    return fullText;
}


/* =========================================
   RUN
========================================= */

async function runCognition(){

    const input =
        document.getElementById(
            "promptInput"
        );

    if(!input) return;

    const prompt =
        input.value.trim();

    if(!prompt) return;

    if(TRACE){
        TRACE.innerHTML = "";
    }

    addTrace(
        "Constitutional Cognition",
        "Pipeline initialized."
    );

    await cinematicReason(prompt);
}


/* =========================================
   BUTTONS
========================================= */

const askButton =
    document.getElementById(
        "askButton"
    );

if(askButton){

    askButton.onclick =
        runCognition;
}


/* =========================================
   ARCHIVE PLAYBACK
========================================= */

const replayButton =
    document.getElementById(
        "replayVoiceBtn"
    );

if(replayButton){

    replayButton.onclick =
        ()=>{

            const audio =
                new Audio(
                    "/static/archive_voice.mp3"
                );

            audio.playbackRate = 1;

            audio.play();

            addTrace(
                "Archive Voice",
                "Historical archive playback active."
            );
        };
}


/* =========================================
   AUTO TRACE
========================================= */

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