FROM python:3.6
MAINTAINER Unethical Discord <developers@unethical.me>

RUN apt-get update -y

WORKDIR /usr/src/app
RUN pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt && pip install --no-cache-dir .

CMD [ "enigma", "start"]
