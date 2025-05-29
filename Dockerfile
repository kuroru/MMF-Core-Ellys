FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git ca-certificates

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD echo "🔥 THIS IS THE REAL DOCKERFILE" && uvicorn api.main:app --host 0.0.0.0 --port 8080

