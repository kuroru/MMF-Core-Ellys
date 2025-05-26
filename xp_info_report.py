import requests
import json

# 환경설정
GITHUB_USER = "kuroru"
REPO = "MMF-Core-Ellys"
BRANCH = "main"
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1376599739704938516/KmggpDvjMOh4uXNWJPid13orv61h6b6Htnmrms77mZ-8yDIqTKwENSgygkWUW4FaYehJ"

xp_files = [
    ("xp/user_xp_table.json", "사용자 XP"),
    ("xp/gpt_xp_table.json", "지피티 XP"),
    ("xp/sentinel_xp_table.json", "센티넬 XP"),
]

def fetch_github_json(path):
    url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO}/{BRANCH}/{path}"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        print(f"❌ {path} fetch 실패: {r.status_code}")
        return None

def report_xp():
    output = []
    for fname, label in xp_files:
        data = fetch_github_json(fname)
        if not data:
            output.append(f"--- {label} 불러오기 실패 ---")
            continue
        output.append(f"--- {label} ---")
        for key in data:
            for entry in data[key]:
                lines = [f"{k}: {v}" for k, v in entry.items()]
                output.append(" / ".join(lines))
    report = "\n".join(output)
    print(report)
    return report

def send_discord(msg):
    data = {"content": msg}
    r = requests.post(DISCORD_WEBHOOK, json=data)
    if r.status_code in (204, 200):
        print("디스코드 알람 전송 성공")
    else:
        print(f"디스코드 알람 실패: {r.status_code} {r.text}")

if __name__ == "__main__":
    xp_report = report_xp()
    # 디스코드 전송(원하면 아래 주석 해제)
    # send_discord(f"🟢 MMF XP 정보 리포트\n{xp_report}")
    