FROM ubuntu:latest
LABEL authors="volkantasci"

RUN apt update && \
     apt install -y yt-dlp ffmpeg python3 python3-pip \
     python3-setuptools python3-wheel python3-dev python3-venv \
     software-properties-common opus-tools libopus-dev firefox

# Geckodriver'ı indirin ve PATH'e ekleyin
RUN apt install -y wget
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz
RUN tar -xvzf geckodriver-v0.33.0-linux64.tar.gz
RUN mv geckodriver /usr/local/bin/
RUN chmod +x /usr/local/bin/geckodriver

RUN mkdir -p /app/music /app/temp

WORKDIR /app

ADD ./requirements.txt requirements.txt

RUN pip3 install --upgrade pip && \
  pip3 install -r requirements.txt

ADD . .
