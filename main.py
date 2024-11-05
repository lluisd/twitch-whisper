from typing import Union
from fastapi import FastAPI
import os
import subprocess
import signal
import time
from fastapi.middleware.cors import CORSMiddleware

#os.system('git clone https://github.com/ggerganov/whisper.cpp.git')
#os.system('make -C ./whisper.cpp')
#os.system('bash ./whisper.cpp/models/download-ggml-model.sh large-v3-turbo')
#os.system('bash ./whisper.cpp/models/download-ggml-model.sh medium')
#os.system('bash ./whisper.cpp/models/download-ggml-model.sh small')
#os.system('bash ./whisper.cpp/models/download-ggml-model.sh base')

app = FastAPI()
origins = [
    "https://twitch-mz-bot.azurewebsites.net",
    "https://mz.311312.xyz",
    "http://localhost",
    "http://localhost:3800",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

filename = ""
p = None

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/start/{channel}")
def start(channel: str):
    print(f'start recording audio from: {channel}')
    timestr = time.strftime("%Y%m%d-%H%M%S")
    global filename
    global p
    filename = f'whisper-live{timestr}.wav'
    kill_process(p)
    p = subprocess.Popen([f'streamlink https://www.twitch.tv/{channel} best --twitch-disable-ads -O 2>/dev/null | ffmpeg -loglevel quiet -i - -y -probesize 32 -y -ar 16000 -ac 1 -acodec pcm_s16le tmp/{filename}'], stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    return {"filename": filename, "pid": p.pid}

@app.get("/stop")
def stop():
    global p
    kill_process(p)
        
def kill_process(p):
    if p: 
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        print(f'process {p.pid} stopped') 
        p = None 
