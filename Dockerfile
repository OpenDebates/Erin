FROM python:3.6
MAINTAINER Federation of Discord Servers <admin@dicord.cx>

RUN apt-get update -y

WORKDIR /usr/src/app
RUN pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt && pip install --no-cache-dir .

CMD [ "erin", "start"]
