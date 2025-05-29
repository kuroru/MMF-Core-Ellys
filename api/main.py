import os, datetime, json, httpx, pathlib
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
app = FastAPI(title="MMF API Server")

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
            raise FileNotFoundError(path)
    return success

def update_handshake_history(success_paths: list[str]):
    ts = datetime.datetime.utcnow().isoformat()
    entry = {
        "datetime": ts,
        "results": [{"filename": p, "status": "SUCCESS", "timestamp": ts} for p in success_paths]
    }
    history_path = "logs/handshake_history.json"
    if os.path.exists(history_path):
        with open(history_path, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except Exception:
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
        f.write(f"{ts} | [MMF 시작선언 핸드셰이크]\n")
        for p in success_paths:
            f.write(f"SUCCESS: {p}\n")

    history_json = update_handshake_history(success_paths)

    user = os.getenv("GITHUB_USER")
    pat = os.getenv("GH_PAT")
    repo = f"https://{user}:{pat}@github.com/{user}/mmf-core-ellys.git"
    try:
        import subprocess
        subprocess.run(["git", "add", log_path], check=True)
        subprocess.run(["git", "add", history_json], check=True)
        subprocess.run(["git", "commit", "-m", f"chore: handshake {ts} [auto]"], check=True)
        subprocess.run(["git", "push", repo, "main"], check=True)
    except Exception as e:
        print("git push error:", e)

    if DISCORD_WEBHOOK:
        msg = f"✅ MMF 핸드셰이크 완료\n```\n" + "\n".join(success_paths) + "\n```"
        try:
            httpx.post(DISCORD_WEBHOOK, json={"content": msg})
        except Exception as e:
            print("discord notify error:", e)

@app.post("/mmf/start")
async def start(payload: dict, request: Request):
    try:
        ok = handshake()
        log_and_notify(ok)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "started"}

@app.post("/mmf/trigger")
async def trigger(command: TriggerCommand):
    if command.command == "mmf_start":
        try:
            ok = handshake()
            log_and_notify(ok)
            return {"status": "triggered", "command": command.command}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail=f"Unknown command: {command.command}")
