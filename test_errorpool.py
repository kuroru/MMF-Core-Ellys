import requests
import datetime

error_event = {
    "timestamp": datetime.datetime.now().isoformat(),
    "error_type": "테스트오류",
    "description": "에러풀 자동화 테스트",
    "user": "마스터"
}

resp = requests.post(
    "http://127.0.0.1:8080/update_errorpool",
    json={
        "error_event": error_event,
        "pool_file": "errors/error_pool.json"
    },
    headers={"X-API-KEY": "SuperSecretKey987654321!@#"}
)
print(resp.json())
