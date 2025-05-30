from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
import traceback

app = FastAPI()

# 모든 예외를 JSON으로 반환
class ExceptionInterceptorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except StarletteHTTPException as http_exc:
            return JSONResponse(
                status_code=http_exc.status_code,
                content={"error": "HTTP Exception", "detail": http_exc.detail}
            )
        except Exception as exc:
            tb = traceback.format_exc()
            return JSONResponse(
                status_code=500,
                content={"error": "Global Exception", "traceback": tb}
            )

app.add_middleware(ExceptionInterceptorMiddleware)

# ✅ 정상 응답 확인용
@app.get("/")
async def root():
    return {"status": "OK"}

# 예외 테스트용
@app.get("/ping")
async def ping():
    raise ValueError("강제 오류 발생")
