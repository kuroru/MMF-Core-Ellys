import os, datetime, json, httpx, pathlib, traceback
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
app = FastAPI(title="MMF Debug API")

class TriggerCommand(BaseModel):
    command: str

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
            raise FileNotFoundError(f"🔍 파일 없음: {path}")
    return success

def update_handshake_history(success_paths: list[str]):
    ts = datetime.datetime.utcnow().isoformat()
    entry = {
        "datetime": ts,
        "results": [{"filename": p, "status": "SUCCESS", "timestamp": ts} for p in success_paths]
    }
    history_path = "logs/handshake_history.json"
    if os.path.exists(history_path):
        try:
            with open(history_path, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception as e:
            print("⚠️ JSON 파싱 실패:", e)
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
    os.makedirs("logs", exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"{ts} | [MMF 시작선언 핸드셰이크]\n")
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
        subprocess.run(["git", "commit", "-m", f"chore: handshake {ts} [auto]"], check=True)
        subprocess.run(["git", "push", repo, "main"], check=True)
    except Exception as e:
        print("⚠️ git push error:", e)

    if DISCORD_WEBHOOK:
        msg = f"✅ MMF 핸드셰이크 완료\n```\n" + "\n".join(success_paths) + "\n```"
        try:
            httpx.post(DISCORD_WEBHOOK, json={"content": msg})
        except Exception as e:
            print("⚠️ discord notify error:", e)

@app.post("/mmf/start")
async def start(payload: dict = {}, request: Request = None):
    try:
        ok = handshake()
        log_and_notify(ok)
        return {"status": "started"}
    except Exception as e:
        tb = traceback.format_exc()
        print("🔥 내부 오류 발생:\n", tb)
        raise HTTPException(status_code=500, detail=tb)

@app.post("/mmf/trigger")
async def trigger(command: TriggerCommand):
    try:
        if command.command == "mmf_start":
            ok = handshake()
            log_and_notify(ok)
            return {"status": "triggered", "command": command.command}
        else:
            raise ValueError(f"Unknown command: {command.command}")
    except Exception as e:
        tb = traceback.format_exc()
        print("🔥 트리거 오류:\n", tb)
        raise HTTPException(status_code=500, detail=tb)
