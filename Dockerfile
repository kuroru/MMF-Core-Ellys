FROM python:3.11-slim

WORKDIR /app

# 0. 기본 도구 설치 (git + 인증서)
RUN apt-get update && apt-get install -y git ca-certificates

# 1. 의존성 설치
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 2. 소스 코드 복사 (api 포함 전체 복사)
COPY . .

# 3. 포트 노출 (선택적 – GCP는 자동 라우팅)
EXPOSE 8080

# 4. 서버 기동
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]

