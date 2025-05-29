import requests

API_URL = "https://mmf-roleplay-gk2qot5tba-du.a.run.app/mmf/start"
headers = {"x-api-key": "SuperSecretKey987654321!@#"}
data = {
    "event": "mmf_start",
    "user": "master",
    "timestamp": "2025-05-29T14:12:00+09:00"
}

response = requests.post(API_URL, json=data, headers=headers)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
