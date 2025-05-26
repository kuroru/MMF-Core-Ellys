import json
import requests
import os
from datetime import datetime

# 환경설정
CONFIG_FILE = "fetch_targets.json"
LOG_DIR = "logs"
HISTORY_FILE = "logs/handshake_history.json"
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1376599739704938516/KmggpDvjMOh4uXNWJPid13orv61h6b6Htnmrms77mZ-8yDIqTKwENSgygkWUW4FaYehJ"
GITHUB_USER = "kuroru"
REPO = "MMF-Core-Ellys"
BRANCH = "main"

def log(msg, logname="handshake"):
    os.makedirs(LOG_DIR, exist_ok=True)
    nowstr = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = os.path.join(LOG_DIR, f"{logname}_{nowstr}.log")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} | {msg}\n")
    print(msg)

def send_discord_alert(msg):
    data = {"content": msg}
    r = requests.post(DISCORD_WEBHOOK, json=data)
    if r.status_code in (204, 200):
        log("디스코드 핸드셰이크 알람 전송 완료")
    else:
        log(f"디스코드 알람 실패: {r.status_code} {r.text}")

def fetch_github(path):
    url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO}/{BRANCH}/{path}"
    r = requests.get(url)
    if r.status_code == 200:
        return True, r.text
    else:
        return False, None

def handshake():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        targets = json.load(f)
    results = []
    log_summary = ["[MMF 시작선언 핸드셰이크]"]
    for t in targets:
        if not t.get("enable", True):
            continue
        fname = t["github_path"]
        success, _ = fetch_github(fname)
        status = "SUCCESS" if success else "FAIL"
        log_summary.append(f"{status}: {fname}")
        results.append({
            "filename": fname,
            "status": status,
            "timestamp": datetime.now().isoformat()
        })
    # 로그 저장
    summary_str = "\n".join(log_summary)
    log(summary_str)
    # handshake 이력 json에 추가
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            hist = json.load(f)
    else:
        hist = []
    hist.append({
        "datetime": datetime.now().isoformat(),
        "results": results
    })
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(hist, f, ensure_ascii=False, indent=2)
    # 디스코드 알람 발송
    send_discord_alert(f"🤝 MMF 시작선언 핸드셰이크 결과\n{summary_str}")

if __name__ == "__main__":
    handshake()
