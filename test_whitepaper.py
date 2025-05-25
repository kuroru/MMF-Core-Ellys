import requests
resp = requests.post(
    "http://127.0.0.1:8080/update_whitepaper",
    json={
        "whitepaper_content": "# 0장 프롤로그\n\n- Ellys Core 백서 자동화 테스트",
        "chapter_file": "docs/whitepaper/0_prologue.md"
    },
    headers={"X-API-KEY": "SuperSecretKey987654321!@#"}
)
print(resp.json())
