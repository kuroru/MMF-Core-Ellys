import httpx

url = "https://mmf-roleplay-debug-1042382168153.asia-northeast3.run.app/ping"

response = httpx.get(url)

print("응답 코드:", response.status_code)
print("응답 내용:", response.text)
