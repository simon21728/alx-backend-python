FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential

WORKDIR /app
COPY . .
RUN pip install -r messaging_app/requirements.txt
