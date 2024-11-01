from typing import Union
from fastapi import FastAPI
import os
import subprocess
import signal
import time

#os.system('git clone https://github.com/ggerganov/whisper.cpp.git')
#os.system('make -C ./whisper.cpp')
#os.system('bash ./whisper.cpp/models/download-ggml-model.sh large-v3-turbo')
#os.system('bash ./whisper.cpp/models/download-ggml-model.sh medium')
#os.system('bash ./whisper.cpp/models/download-ggml-model.sh small')
os.system('bash ./whisper.cpp/models/download-ggml-model.sh base')

app = FastAPI()
filename = ""

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/start/{channel}")
def start(channel: str):
    print(f'start recording audio from: {channel}')
    timestr = time.strftime("%Y%m%d-%H%M%S")
    global filename
    filename = f'whisper-live{timestr}.wav'
    app.proc = subprocess.Popen([f'streamlink https://www.twitch.tv/{channel} best --twitch-disable-ads -O 2>/dev/null | ffmpeg -loglevel quiet -i - -y -probesize 32 -y -ar 16000 -ac 1 -acodec pcm_s16le /usr/src/app/tmp/{filename}'], stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

@app.get("/stop")
def stop():
    print("stop")
    if filename:
        os.killpg(os.getpgid(app.proc.pid), signal.SIGTERM) 
        os.system(f'/usr/src/app/whisper.cpp/main /usr/src/app/tmp/{filename} -t 4 -l es -m /usr/src/app/whisper.cpp/models/ggml-base.bin  --no-timestamps -otxt')
