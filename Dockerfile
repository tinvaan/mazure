FROM python:3.7-slim

RUN apt-get update && apt-get install -y build-essential python3-dev

RUN mkdir -p /mazure
WORKDIR /mazure
COPY . /mazure

RUN pip install -r requirements.txt
ENV PYTHONPATH $(pwd)/mazure:$PYTHONPATH
