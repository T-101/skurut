FROM python:3.13.1-alpine3.21

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

RUN apk add --no-cache nano bash

RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt
