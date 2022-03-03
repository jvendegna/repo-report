FROM python:3.9-slim-buster

WORKDIR /app

RUN addgroup --system app && adduser --system --group app

USER app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./ .

