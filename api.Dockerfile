FROM python:3.8.8-slim

WORKDIR /app

COPY ./requirements-api.txt /app/requirements-api.txt
RUN pip install -r requirements-api.txt

COPY ./api.py /app/api.py
