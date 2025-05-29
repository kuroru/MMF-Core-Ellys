import httpx

url = "https://mmf-roleplay-1042382168153.asia-northeast3.run.app/mmf/trigger"
payload = {
    "command": "mmf_start"
}

try:
    response = httpx.post(url, json=payload)
    print("응답 코드:", response.status_code)
    print("응답 본문 원본:", repr(response.text))
    print("JSON 파싱 결과:", response.json())
except httpx.HTTPStatusError as e:
    print("HTTP 에러 발생:", e.response.status_code, e.response.text)
except Exception as e:
    print("일반 에러 발생:", str(e))
