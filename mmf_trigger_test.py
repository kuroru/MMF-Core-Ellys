# mmf_trigger_test.py
import httpx

url = "https://mmf-roleplay-1042382168153.asia-northeast3.run.app/mmf/trigger"
payload = {
    "command": "mmf_start"
}

try:
    response = httpx.post(url, json=payload)
    print("응답 코드:", response.status_code)
    print("응답 내용:", response.text)
except Exception as e:
    print("요청 실패:", e)
