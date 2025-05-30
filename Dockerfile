# Dockerfile (테스트용으로 잠시 변경)

FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main_debug:app", "--host", "0.0.0.0", "--port", "8080"]
