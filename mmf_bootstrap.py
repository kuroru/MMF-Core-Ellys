import json
import requests
import os
from datetime import datetime

CONFIG_FILE = "fetch_targets.json"
LOG_DIR = "logs"
SNAPSHOT_DIR = "projects/MMF-001/snapshots"
HISTORY_FILE = "logs/handshake_history.json"
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1376599739704938516/KmggpDvjMOh4uXNWJPid13orv61h6b6Htnmrms77mZ-8yDIqTKwENSgygkWUW4FaYehJ"
GITHUB_USER = "kuroru"
REPO = "MMF-Core-Ellys"
BRANCH = "main"

def log(msg, logname="mmf_bootstrap"):
    os.makedirs(LOG_DIR, exist_ok=True)
    nowstr = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = os.path.join(LOG_DIR, f"{logname}_{nowstr}.log")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} | {msg}\n")
    print(msg)

def send_discord_alert(msg):
    data = {"content": msg}
    try:
        r = requests.post(DISCORD_WEBHOOK, json=data)
        if r.status_code in (204, 200):
            log("디스코드 알람 송출 완료")
        else:
            log(f"디스코드 알람 실패: {r.status_code} {r.text}")
    except Exception as e:
        log(f"디스코드 알람 예외: {e}")

def fetch_github(path):
    url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO}/{BRANCH}/{path}"
    r = requests.get(url)
    if r.status_code == 200:
        return True, r.text
    else:
        return False, None

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

def mmf_bootstrap():
    log_summary = ["[MMF 시작선언: 자동화 운영 부트스트랩]"]
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        targets = json.load(f)

    results = []
    for t in targets:
        if not t.get("enable", True):
            continue
        fname = t["github_path"]
        required_keys = t.get("required_keys")
        # 1. fetch
        success, content = fetch_github(fname)
        status = "SUCCESS" if success else "FAIL"
        results.append({
            "filename": fname,
            "status": status,
            "timestamp": datetime.now().isoformat()
        })
        log_summary.append(f"{status}: {fname}")
        # 2. 저장 및 스냅샷
        if success:
            local_path = t["local_path"]
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, "w", encoding="utf-8") as f2:
                f2.write(content)
            snapshot(local_path)
            # 3. 정합성 검증
            if t.get("type") == "json":
                validate_json(local_path, required_keys)
        else:
            log(f"센티넬 경고: {fname} fetch 실패(404 등)")

    # 4. 시스템 현황 리포트
    try:
        with open("xp/user_xp_table.json", "r", encoding="utf-8-sig") as f: user_xp = json.load(f)
        with open("xp/gpt_xp_table.json", "r", encoding="utf-8-sig") as f: gpt_xp = json.load(f)
        with open("xp/sentinel_xp_table.json", "r", encoding="utf-8-sig") as f: sentinel_xp = json.load(f)
        status_lines = ["[XP 현황]"]
        for label, data in [("사용자 XP", user_xp), ("GPT XP", gpt_xp), ("센티넬 XP", sentinel_xp)]:
            for key in data:
                for entry in data[key]:
                    entry_line = " / ".join([f"{k}: {v}" for k, v in entry.items()])
                    status_lines.append(f"{label}: {entry_line}")
        status_report = "\n".join(status_lines)
    except Exception as e:
        status_report = f"[XP 현황 로딩 실패]: {e}"

    # 5. logs/handshake_history.json 이력화
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            hist = json.load(f)
    else:
        hist = []
    hist.append({
        "datetime": datetime.now().isoformat(),
        "results": results,
        "xp_status": status_report
    })
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(hist, f, ensure_ascii=False, indent=2)

    # 6. 디스코드 알람 송출
    final_report = "\n".join(log_summary + ["", status_report])
    send_discord_alert(f"🟢 MMF 시작선언(자동화 운영 부트스트랩)\n{final_report}")
    log(final_report)

if __name__ == "__main__":
    mmf_bootstrap()
