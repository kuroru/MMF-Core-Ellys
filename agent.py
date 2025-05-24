from flask import Flask, request
import requests

app = Flask(__name__)

GITHUB_TOKEN = 'your_PAT'   # GitHub PAT(권장: 레포 단독 전용, 권한 제한)
WORKFLOW_URL = "https://api.github.com/repos/kuroru/MMF-Core-Ellys/actions/workflows/develop_note.yml/dispatches"

@app.route('/trigger', methods=['POST'])
def trigger_github_workflow():
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }
    data = { "ref": "main" }
    resp = requests.post(WORKFLOW_URL, headers=headers, json=data)
    return {"status": resp.status_code, "response": resp.text}

if __name__ == "__main__":
    app.run(port=5000)
