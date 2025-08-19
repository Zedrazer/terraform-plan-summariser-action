FROM python:3.13.7-slim-bookworm

WORKDIR /
COPY src src

COPY requirements.txt requirements.txt

COPY entrypoint.sh /entrypoint.sh

RUN apt-get update -y && \
  apt-get upgrade -y && \
  apt-get -y install git && \
  rm -rf /var/lib/apt/lists/* && \
  pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/entrypoint.sh"]
