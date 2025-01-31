FROM python:3.13.1-alpine3.21

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk add --no-cache nano bash

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
