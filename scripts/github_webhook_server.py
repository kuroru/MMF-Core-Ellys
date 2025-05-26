from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def github_webhook():
    event = request.headers.get('X-GitHub-Event')
    payload = request.json
    if event == 'issues' and payload.get('action') == 'opened':
        issue = payload['issue']
        # 대시보드/메타 파일 등에 자동 반영
        print(f"[대시보드] 새 이슈: {issue['title']} by {issue['user']['login']}")
        # 예시: meta/history.json 등 기록 자동 추가
    # 추가 이벤트(머지, PR 등)도 동일하게 분기 가능
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
