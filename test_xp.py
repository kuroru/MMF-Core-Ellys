import requests
import datetime

xp_event = {
    "timestamp": datetime.datetime.now().isoformat(),
    "user": "마스터",
    "event_type": "테스트 XP",
    "xp_delta": 50,
    "description": "XP/보상 자동화 테스트"
}

resp = requests.post(
    "http://127.0.0.1:8080/update_xp",
    json={
        "xp_event": xp_event,
        "xp_file": "xp/xp_table.json"
    },
    headers={"X-API-KEY": "SuperSecretKey987654321!@#"}
)
print('응답 본문:', resp.text)
try:
    print(resp.json())
except Exception as e:
    print('JSON decode error:', e)
