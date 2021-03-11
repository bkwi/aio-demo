FROM python:3.8.8-slim

WORKDIR /app

COPY ./requirements-worker.txt /app/requirements-worker.txt
RUN pip install -r requirements-worker.txt

COPY ./worker.py /app/worker.py
