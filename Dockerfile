FROM python:3.11-slim
WORKDIR /app

# 1. 의존성
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. 소스
COPY . .

# 3. 포트 노출(옵션)
EXPOSE 8080

# 4. 기동
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
