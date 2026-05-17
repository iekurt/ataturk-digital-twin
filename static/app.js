/* =========================================
   static/app.js
   FULL LONG CINEMATIC VERSION
========================================= */

"use strict";


/* =========================================
   GLOBAL AUDIO CONTROL
========================================= */

let activeAudio = null;

function stopAllAudio(){

    try{

        if(activeAudio){

            activeAudio.pause();

            activeAudio.currentTime = 0;

            activeAudio = null;
        }

        const ttsAudio =
            document.getElementById(
                "ttsAudio"
            );

        if(ttsAudio){

            ttsAudio.pause();

            ttsAudio.currentTime = 0;
        }

        if(
            "speechSynthesis" in window
        ){

            speechSynthesis.cancel();
        }

        addTrace(
            "Audio Controller",
            "All active audio streams terminated."
        );

    }catch(err){

        console.error(err);
    }
}


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

        stopAllAudio();

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

        audio.currentTime = 0;

        audio.src = url;

        audio.load();

        audio.playbackRate = 0.96;

        activeAudio = audio;

        await audio.play();

        addTrace(
            "Archive Voice",
            "Constitutional voice playback active."
        );

        audio.onended = ()=>{

            activeAudio = null;

            addTrace(
                "Audio Controller",
                "Playback session completed."
            );
        };

    }catch(err){

        console.error(err);

        addTrace(
            "Voice Error",
            String(err)
        );
    }
}


/* =========================================
   CINEMATIC TYPEWRITER
========================================= */

let renderText = "";

let tokenQueue = [];

let typingActive = false;

async function cinematicTypewriter(output){

    if(typingActive) return;

    typingActive = true;

    while(tokenQueue.length > 0){

        const next =
            tokenQueue.shift();

        renderText += next;

        output.innerHTML =

            renderText +

            '<span class="live-cursor breathing-cursor">█</span>';

        await new Promise(r =>
            setTimeout(r, 22)
        );
    }

    typingActive = false;
}


/* =========================================
   SSE STREAMING
========================================= */

async function cinematicReason(prompt){

    stopAllAudio();

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

    renderText = "";

    tokenQueue = [];

    typingActive = false;

    output.innerHTML =
        '<span class="live-cursor breathing-cursor">█</span>';

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

                while(tokenQueue.length > 0){

                    await new Promise(r =>
                        setTimeout(r, 50)
                    );
                }

                output.innerHTML =

                    renderText +

                    '<span class="live-cursor breathing-cursor">█</span>';

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

                    tokenQueue.push(
                        parsed.token
                    );

                    cinematicTypewriter(
                        output
                    );
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

    stopAllAudio();

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
        async ()=>{

            stopAllAudio();

            const audio =
                new Audio(
                    "/static/archive_voice.mp3"
                );

            audio.playbackRate = 1;

            activeAudio = audio;

            await audio.play();

            addTrace(
                "Archive Voice",
                "Historical archive playback active."
            );

            audio.onended = ()=>{

                activeAudio = null;

                addTrace(
                    "Archive Voice",
                    "Historical playback completed."
                );
            };
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

        injectCursorStyles();
    }
);


/* =========================================
   CURSOR STYLE INJECTION
========================================= */

function injectCursorStyles(){

    const style =
        document.createElement("style");

    style.innerHTML = `

        .breathing-cursor{

            display:inline-block;

            animation:
                heartbeatCursor 1.2s ease-in-out infinite;

            color:#ffffff;

            text-shadow:
                0 0 8px rgba(255,255,255,0.8),
                0 0 16px rgba(255,255,255,0.5);
        }

        @keyframes heartbeatCursor{

            0%{
                opacity:0.35;
                transform:scale(1);
            }

            25%{
                opacity:1;
                transform:scale(1.25);
            }

            40%{
                opacity:0.5;
                transform:scale(0.95);
            }

            60%{
                opacity:1;
                transform:scale(1.18);
            }

            100%{
                opacity:0.35;
                transform:scale(1);
            }
        }

    `;

    document.head.appendChild(
        style
    );
}