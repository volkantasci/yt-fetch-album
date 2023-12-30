FROM ubuntu:latest
LABEL authors="volkantasci"

RUN sudo add-apt-repository ppa:tomtomtom/yt-dlp -y && \
sudo apt update && \
sudo apt install yt-dlp -y && \
sudo apt install ffmpeg -y && \
sudo apt install python3 -y && \
sudo apt install python3-pip -y && \
sudo apt install python3-setuptools -y && \
sudo apt install python3-wheel -y && \
sudo apt install python3-dev -y && \
sudo apt install python3-venv -y && \
sudo apt-get install -y software-properties-common && \
sudo apt-get install -y opus-tools && \
sudo apt-get install -y libopus-dev &&

RUN mkdir /app

WORKDIR /app

ADD ./requirements.txt requirements.txt

RUN sudo pip3 install --upgrade pip && \
sudo pip3 install -r requirements.txt


ENTRYPOINT ["top", "-b"]