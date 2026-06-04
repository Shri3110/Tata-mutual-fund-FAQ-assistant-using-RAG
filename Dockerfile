FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential curl

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED=1

CMD sh -c "uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}"
