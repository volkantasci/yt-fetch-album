FROM ubuntu:latest
LABEL authors="volkantasci"

RUN apt update && \
     apt install yt-dlp -y && \
     apt install ffmpeg -y && \
     apt install python3 -y && \
     apt install python3-pip -y && \
     apt install python3-setuptools -y && \
     apt install python3-wheel -y && \
     apt install python3-dev -y && \
     apt install python3-venv -y && \
     apt-get install -y software-properties-common && \
     apt-get install -y opus-tools && \
     apt-get install -y libopus-dev && \
        apt-get install -y firefox && \
        apt-get install -y firefox-headless

RUN mkdir /app
RUN mkdir /app/music
RUN mkdir /app/temp

WORKDIR /app

ADD ./requirements.txt requirements.txt

RUN pip3 install --upgrade pip && \
  pip3 install -r requirements.txt

ADD . .