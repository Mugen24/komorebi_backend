FROM debian:oldstable-20251208

RUN mkdir -p /opt/komorebi/backend/


ADD game    /opt/komorebi/backend/game
ADD utils   /opt/komorebi/backend/utils
COPY main.py /opt/komorebi/backend/
COPY run.sh  /opt/komorebi/backend/
COPY requirements.txt  /opt/komorebi/backend/

RUN chmod -R 755 /opt/komorebi/backend/


RUN apt update -y 
RUN apt install -y python3 
RUN apt install -y python3-pip
RUN apt install -y python3.11-venv

WORKDIR /opt/komorebi/backend/
RUN python3 -m venv . 
ENV PATH="/opt/komorebi/backend/bin:$PATH"
RUN pip3 install -r requirements.txt


RUN mkdir -p /opt/komorebi/data
RUN mkdir -p /opt/komorebi/config
RUN mkdir -p /opt/komorebi/config/games

ENV PORT=9543
ENV GAME_PATH="/opt/komorebi/config/games"
ENV SERVER_ROOT="/opt/komorebi/data"

# RUN fastapi run main.py --port $PORT
EXPOSE $PORT
ENTRYPOINT ["fastapi", "run", "main.py", "--port", "9543"]


