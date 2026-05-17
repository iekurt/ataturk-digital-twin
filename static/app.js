/* =========================================
   static/app.js
   FULL LONG CINEMATIC VERSION
   FINAL CLEAN READABLE BUILD
========================================= */

"use strict";


/* =========================================
   GLOBAL AUDIO CONTROL
========================================= */

let activeAudio = null;

let activeAudioContext = null;

let activeNoiseSource = null;

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

        if(activeNoiseSource){

            try{
                activeNoiseSource.stop();
            }catch(e){}

            activeNoiseSource = null;
        }

        if(activeAudioContext){

            activeAudioContext.close();

            activeAudioContext = null;
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
   CLEAN ARCHIVE FILTER
========================================= */

function applyArchiveVoiceEffect(audio){

    try{

        const AudioContextClass =
            window.AudioContext ||
            window.webkitAudioContext;

        const audioCtx =
            new AudioContextClass();

        activeAudioContext =
            audioCtx;

        const source =
            audioCtx.createMediaElementSource(
                audio
            );

        /* =====================================
           MAIN BANDPASS
        ===================================== */

        const bandpass =
            audioCtx.createBiquadFilter();

        bandpass.type =
            "bandpass";

        bandpass.frequency.value =
            1250;

        bandpass.Q.value =
            1.1;

        /* =====================================
           DISTORTION
        ===================================== */

        const distortion =
            audioCtx.createWaveShaper();

        function makeDistortionCurve(amount){

            const k =
                typeof amount === "number"
                    ? amount
                    : 50;

            const n_samples =
                44100;

            const curve =
                new Float32Array(
                    n_samples
                );

            const deg =
                Math.PI / 180;

            for(
                let i = 0;
                i < n_samples;
                ++i
            ){

                const x =
                    i * 2 /
                    n_samples - 1;

                curve[i] =

                    (3 + k) *
                    x *
                    20 *
                    deg /

                    (
                        Math.PI +
                        k *
                        Math.abs(x)
                    );
            }

            return curve;
        }

        distortion.curve =
            makeDistortionCurve(24);

        distortion.oversample =
            "2x";

        /* =====================================
           LOWPASS
        ===================================== */

        const lowpass =
            audioCtx.createBiquadFilter();

        lowpass.type =
            "lowpass";

        lowpass.frequency.value =
            1450;

        /* =====================================
           REMOVE HISS
        ===================================== */

        const highshelf =
            audioCtx.createBiquadFilter();

        highshelf.type =
            "highshelf";

        highshelf.frequency.value =
            2200;

        highshelf.gain.value =
            -18;

        /* =====================================
           RADIO BODY
        ===================================== */

        const peaking =
            audioCtx.createBiquadFilter();

        peaking.type =
            "peaking";

        peaking.frequency.value =
            700;

        peaking.Q.value =
            1;

        peaking.gain.value =
            4;

        /* =====================================
           OUTPUT GAIN
        ===================================== */

        const gain =
            audioCtx.createGain();

        gain.gain.value =
            0.88;

        /* =====================================
           VERY LIGHT NOISE
        ===================================== */

        const noiseGain =
            audioCtx.createGain();

        /* MASSIVELY REDUCED */

        noiseGain.gain.value =
            0.00015;

        const bufferSize =
            2 * audioCtx.sampleRate;

        const noiseBuffer =
            audioCtx.createBuffer(

                1,

                bufferSize,

                audioCtx.sampleRate
            );

        const outputNoise =
            noiseBuffer.getChannelData(0);

        for(
            let i = 0;
            i < bufferSize;
            i++
        ){

            outputNoise[i] =
                (Math.random() * 2 - 1)
                * 0.25;
        }

        const whiteNoise =
            audioCtx.createBufferSource();

        whiteNoise.buffer =
            noiseBuffer;

        whiteNoise.loop = true;

        activeNoiseSource =
            whiteNoise;

        /* =====================================
           CONNECT
        ===================================== */

        source.connect(
            bandpass
        );

        bandpass.connect(
            distortion
        );

        distortion.connect(
            lowpass
        );

        lowpass.connect(
            highshelf
        );

        highshelf.connect(
            peaking
        );

        peaking.connect(
            gain
        );

        gain.connect(
            audioCtx.destination
        );

        /* HISS DISABLED */

        // whiteNoise.connect(
        //     noiseGain
        // );

        // noiseGain.connect(
        //     audioCtx.destination
        // );

        // whiteNoise.start(0);

    }catch(err){

        console.error(err);

        addTrace(
            "Archive Filter",
            "Archive filter fallback mode."
        );
    }
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

        audio.playbackRate = 0.88;

        activeAudio = audio;

        applyArchiveVoiceEffect(
            audio
        );

        await audio.play();

        addTrace(
            "Archive Voice",
            "Constitutional archive playback active."
        );

        audio.onended = ()=>{

            activeAudio = null;

            if(activeNoiseSource){

                try{
                    activeNoiseSource.stop();
                }catch(e){}

                activeNoiseSource = null;
            }

            if(activeAudioContext){

                activeAudioContext.close();

                activeAudioContext = null;
            }

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
   WORD CINEMATIC TYPEWRITER
========================================= */

let renderText = "";

let wordQueue = [];

let typingActive = false;

async function cinematicTypewriter(output){

    if(typingActive) return;

    typingActive = true;

    while(wordQueue.length > 0){

        const nextWord =
            wordQueue.shift();

        /* FIX SPACING */

        if(
            renderText.length > 0 &&
            !renderText.endsWith(" ") &&
            !nextWord.startsWith(" ") &&
            ![".",",",";",":","!","?"].includes(
                nextWord.trim()
            )
        ){

            renderText += " ";
        }

        renderText += nextWord.trim();

        output.innerHTML =

            renderText +

            '<span class="live-cursor breathing-cursor">█</span>';

        /* 2X FASTER */

        let delay = 42;

        if(
            nextWord.includes(".") ||
            nextWord.includes("!") ||
            nextWord.includes("?")
        ){

            delay = 130;
        }

        else if(
            nextWord.includes(",") ||
            nextWord.includes(";") ||
            nextWord.includes(":")
        ){

            delay = 85;
        }

        await new Promise(r =>
            setTimeout(r, delay)
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

    wordQueue = [];

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

                while(wordQueue.length > 0){

                    await new Promise(r =>
                        setTimeout(r, 120)
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

                    const words =
                        parsed.token.match(
                            /\S+\s*/g
                        ) || [];

                    for(
                        const word of words
                    ){

                        wordQueue.push(word);
                    }

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

            audio.playbackRate = 0.94;

            activeAudio = audio;

            applyArchiveVoiceEffect(
                audio
            );

            await audio.play();

            addTrace(
                "Archive Voice",
                "Historical archive playback active."
            );

            audio.onended = ()=>{

                activeAudio = null;

                if(activeNoiseSource){

                    try{
                        activeNoiseSource.stop();
                    }catch(e){}

                    activeNoiseSource = null;
                }

                if(activeAudioContext){

                    activeAudioContext.close();

                    activeAudioContext = null;
                }

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
                opacity:0.25;
                transform:scale(1);
            }

            25%{
                opacity:1;
                transform:scale(1.35);
            }

            40%{
                opacity:0.45;
                transform:scale(0.92);
            }

            60%{
                opacity:1;
                transform:scale(1.22);
            }

            100%{
                opacity:0.25;
                transform:scale(1);
            }
        }

    `;

    document.head.appendChild(
        style
    );
}