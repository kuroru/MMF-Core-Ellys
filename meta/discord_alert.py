import requests

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1376562880387743875/2bW-X0wwrXOPIca60dvmBz10BGKzsBn3D1LfmD_4eJjgcG7fe3ygtOOY3X-1pBgK6fFT"

def send_discord_alert(message):
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("디스코드 알림 전송 성공")
    else:
        print(f"실패: {response.status_code}, {response.text}")

def alert_trend(date="240526"):
    import json
    with open(f"meta/analysis_commands_{date}.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    top = data.get("top_commands", [("없음", 0)])[0][0]
    send_discord_alert(f"오늘의 추천 명령어: {top}")

# pip install requests 필요
if __name__ == "__main__":
    alert_trend("240526")
