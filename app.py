import os,json,asyncio
from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse,StreamingResponse,Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from openai import OpenAI

app=FastAPI(title="ATATURK DIGITAL TWIN")

app.mount("/static",StaticFiles(directory="static"),name="static")
templates=Jinja2Templates(directory="templates")

client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ReasonPayload(BaseModel):
    prompt:str=""
    reasoning_mode:str="constitutional"

class TTSPayload(BaseModel):
    text:str=""

@app.get("/",response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.post("/stream")
async def stream(payload:ReasonPayload):

    async def token_stream():

        completion=client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role":"system",
                    "content":"Speak Turkish. Use calm authoritative rhetoric."
                },
                {
                    "role":"user",
                    "content":payload.prompt
                }
            ],
            stream=True
        )

        for chunk in completion:

            try:
                delta=chunk.choices[0].delta.content

                if delta:
                    yield f"data: {json.dumps({'token':delta})}\\n\\n"

            except:
                pass

        yield "data: [DONE]\\n\\n"

    return StreamingResponse(
        token_stream(),
        media_type="text/event-stream"
    )

@app.post("/tts")
async def tts(payload:TTSPayload):

    speech=client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="onyx",
        input=payload.text
    )

    return Response(
        content=speech.content,
        media_type="audio/mpeg"
    )
