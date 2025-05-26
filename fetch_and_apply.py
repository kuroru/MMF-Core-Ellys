import json
import requests
import os
import subprocess
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

CONFIG_FILE = "fetch_targets.json"
SNAPSHOT_DIR = "projects/MMF-001/snapshots"
LOG_DIR = "logs"
GITHUB_USER = "kuroru"
REPO = "MMF-Core-Ellys"
BRANCH = "main"

def log(msg):
    os.makedirs(LOG_DIR, exist_ok=True)
    path = os.path.join(LOG_DIR, f"fetch_{datetime.now().strftime('%Y%m%d')}.log")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} | {msg}\n")
    print(msg)

def send_discord_alert(webhook_url, message):
    data = {"content": message}
    try:
        r = requests.post(webhook_url, json=data)
        if r.status_code != 204 and r.status_code != 200:
            log(f"DISCORD FAIL: {r.status_code} {r.text}")
        else:
            log("DISCORD ALERT SENT")
    except Exception as e:
        log(f"DISCORD ERROR: {e}")

def fetch(github_path, local_path):
    url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO}/{BRANCH}/{github_path}"
    r = requests.get(url)
    if r.status_code == 200:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, "w", encoding="utf-8") as f:
            f.write(r.text)
        log(f"SUCCESS: {github_path} → {local_path}")
        return True
    else:
        log(f"FAIL: {github_path} [{r.status_code}]")
        return False

def snapshot(local_path):
    if os.path.exists(local_path):
        os.makedirs(SNAPSHOT_DIR, exist_ok=True)
        snap_path = os.path.join(SNAPSHOT_DIR, f"{os.path.basename(local_path)}_{datetime.now().strftime('%Y%m%d%H%M%S')}")
        try:
            with open(local_path, "r", encoding="utf-8") as src, open(snap_path, "w", encoding="utf-8") as dst:
                dst.write(src.read())
        except Exception:
            with open(local_path, "rb") as src, open(snap_path, "wb") as dst:
                dst.write(src.read())
        log(f"SNAPSHOT: {snap_path}")


def validate_json(local_path, required_keys=None):
    try:
        with open(local_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        if required_keys:
            for k in required_keys:
                if k not in data:
                    log(f"VALIDATE_FAIL: {local_path} 누락 필드: {k}")
                    return False
        log(f"VALIDATE_OK: {local_path}")
        return True
    except Exception as e:
        log(f"VALIDATE_ERR: {local_path}, {e}")
        return False

def run_reward_script(script_path, local_path):
    if script_path and os.path.exists(script_path):
        try:
            result = subprocess.run(["python", script_path, local_path], capture_output=True, text=True)
            log(f"REWARD_SCRIPT: {script_path} 실행 완료\n{result.stdout}\n{result.stderr}")
        except Exception as e:
            log(f"REWARD_SCRIPT_ERROR: {e}")

def process_target(target):
    if not target.get("enable", True):
        return
    github_path = target["github_path"]
    local_path = target["local_path"]
    required_keys = target.get("required_keys")
    alarm = target.get("alarm")
    discord_webhook = target.get("discord_webhook")
    reward_script = target.get("reward_script")

    # 1. 스냅샷
    snapshot(local_path)
    # 2. fetch
    ok = fetch(github_path, local_path)
    # 3. 검증
    valid = False
    if ok and target.get("type") == "json":
        valid = validate_json(local_path, required_keys)
    else:
        valid = ok

    # 4. 보상
    if valid and reward_script:
        run_reward_script(reward_script, local_path)

    # 5. 알람 (error시만, always로도 확장 가능)
    if (not valid) and alarm in ("always", "error") and discord_webhook:
        msg = f":warning: [{target.get('name', local_path)}] fetch/validate 실패!"
        send_discord_alert(discord_webhook, msg)

def main():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        targets = json.load(f)
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(process_target, [t for t in targets if t.get("enable", True)])

if __name__ == "__main__":
    main()
