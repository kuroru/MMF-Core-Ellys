import os, datetime, json, httpx, pathlib, traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

print("✅ API MAIN LOADED")
assert False, "테스트"

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
app = FastAPI(title="MMF Debug API")

class TriggerCommand(BaseModel):
    command: str

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    tb = traceback.format_exc()
    return JSONResponse(
        status_code=500,
        content={"error": "Global handler", "traceback": tb},
    )

from starlette.exceptions import HTTPException

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "HTTP Exception", "detail": exc.detail},
    )


def handshake() -> list[str]:
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
            raise FileNotFoundError(f"파일 없음: {path}")
    return success

def update_handshake_history(success_paths: list[str]):
    ts = datetime.datetime.utcnow().isoformat()
    entry = {
        "datetime": ts,
        "results": [{"filename": p, "status": "SUCCESS", "timestamp": ts} for p in success_paths]
    }
    history_path = "logs/handshake_history.json"
    os.makedirs("logs", exist_ok=True)
    if os.path.exists(history_path):
        try:
            with open(history_path, "r", encoding="utf-8") as f:
                history = json.load(f)
        except:
            history = []
    else:
        history = []
    history.insert(0, entry)
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    return history_path

def log_and_notify(success_paths: list[str]):
    ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    log_path = f"logs/handshake_{ts}.log"
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"{ts} | [MMF 핸드셰이크]\n")
        for p in success_paths:
            f.write(f"SUCCESS: {p}\n")

    history_json = update_handshake_history(success_paths)

    user = os.getenv("GITHUB_USER", "unknown")
    pat = os.getenv("GH_PAT", "invalid")
    repo = f"https://{user}:{pat}@github.com/{user}/mmf-core-ellys.git"
    try:
        import subprocess
        subprocess.run(["git", "add", log_path], check=True)
        subprocess.run(["git", "add", history_json], check=True)
        subprocess.run(["git", "commit", "-m", f"chore: handshake {ts}"], check=True)
        subprocess.run(["git", "push", repo, "main"], check=True)
    except Exception as e:
        print("git push 오류:", e)

    if DISCORD_WEBHOOK:
        try:
            httpx.post(DISCORD_WEBHOOK, json={"content": "✅ MMF 핸드셰이크 완료"})
        except Exception as e:
            print("디스코드 알림 실패:", e)

@app.post("/mmf/start")
async def start(payload: dict = {}, request: Request = None):
    ok = handshake()
    log_and_notify(ok)
    return {"status": "started"}

@app.post("/mmf/trigger")
async def trigger(command: TriggerCommand):
    if command.command == "mmf_start":
        ok = handshake()
        log_and_notify(ok)
        return {"status": "triggered", "command": command.command}
    else:
        raise ValueError(f"Unknown command: {command.command}")
