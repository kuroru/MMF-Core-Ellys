from fastapi import FastAPI, Request, HTTPException
import os

# FastAPI 인스턴스 ─ openapi_url 지정으로 /openapi.json 자동 노출
app = FastAPI(
    title="MMF Core Ellys API",
    version="1.0.0",
    openapi_url="/openapi.json"
)

# (선택) API Key 검사 ─ Cloud Run 환경변수 API_KEY 로 주입 예정
API_KEY = os.getenv("API_KEY", "")

@app.middleware("http")
async def verify_key(request: Request, call_next):
    if API_KEY and request.headers.get("x-api-key") != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid key")
    return await call_next(request)

# ① MMF 시작
@app.post("/mmf/start")
async def start_mmf(payload: dict):
    # TODO: mmf-core-ellys 내부 로직 호출
    return {"status": "started"}

# ② 단계별 처리
@app.post("/mmf/step/{n}")
async def step_mmf(n: int, payload: dict):
    # TODO: 단계별 로직
    return {"step": n, "status": "ok"}
