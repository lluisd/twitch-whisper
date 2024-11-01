FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get -y update
RUN apt-get install build-essential ffmpeg git make wget  -y

RUN git clone https://github.com/ggerganov/whisper.cpp.git whisper.cpp
RUN cd whisper.cpp 
RUN make -C ./whisper.cpp

RUN mkdir -p ./tmp
COPY . .

EXPOSE 8000

ENV NAME world

CMD ["fastapi", "run"]