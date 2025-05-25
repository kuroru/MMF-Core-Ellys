"""
meta:
  updated: 2025-05-26T01:40:45
  author: master
  branch: main
  commit: latest
  tags: []
"""
import requests

url = "https://mmf-hook-1042382168153.asia-northeast3.run.app/trigger"
payload = {
    "devnote_content": """
# 센티넬 개발노트

생성일: 2025-05-24 06:33

## 0. 인프라 및 연동 정보
- Cloud Run URL: https://mmf-hook-1042382168153.asia-northeast3.run.app
- 테스트: 이 내용이 제대로 깃허브 DEVELOP_NOTE.md에 반영되는지 실시간 확인
"""
}
response = requests.post(url, json=payload)
print(response.status_code, response.text)
