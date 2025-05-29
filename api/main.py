# api/main.py
import os, datetime, json, httpx, pathlib
from fastapi import FastAPI, HTTPException, Request

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

app = FastAPI(...)

def handshake() -> list[str]:
    """필수 경로 점검 후 성공 목록 반환"""
    required = [
        "policies/mmf_policy.json",
        "xp/xp_table.json",
        "xp/rewards_catalog.yaml",
        "projects/MMF-001/error_pool.json",
        ".github/meta_logs/xp_events.json",
    ]
    success = []
    for path in required:
        if pathlib.Path(path).is_file():
            success.append(path)
        else:
            raise FileNotFoundError(path)
    return success

def log_and_notify(success_paths: list[str]):
    ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    log_path = f"logs/handshake_{ts}.log"
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"{ts} | [MMF 시작선언 핸드셰이크]\n")
        for p in success_paths:
            f.write(f"SUCCESS: {p}\n")
    # Discord 알림
    if DISCORD_WEBHOOK:
        msg = f"✅ MMF 핸드셰이크 완료\n```\n" + "\n".join(success_paths) + "\n```"
        httpx.post(DISCORD_WEBHOOK, json={"content": msg})

@app.post("/mmf/start")
async def start(payload: dict, request: Request):
    # (API 키 미들웨어로 인증 완료 가정)
    try:
        ok = handshake()
        log_and_notify(ok)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "started"}
