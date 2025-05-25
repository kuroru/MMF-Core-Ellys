import requests
resp = requests.post(
    "http://127.0.0.1:8080/update_patchnote",
    json={
        "patchnote_content": "# 패치노트\n\n- 인증 자동화 테스트",
        "patchnote_file": "docs/patch_notes/v3.5.1.md"
    },
    headers={"X-API-KEY": "SuperSecretKey987654321!@#"}
)
print(resp.json())
