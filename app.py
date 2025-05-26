from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/mmf/start', methods=['POST'])
def mmf_start():
    # 자연어 명령이나 시스템 이벤트에서 MMF 시작선언을 트리거할 때 사용
    try:
        proc = subprocess.run(["python", "mmf_bootstrap.py"], capture_output=True, text=True, timeout=300)
        return jsonify({"result": "success", "stdout": proc.stdout, "stderr": proc.stderr}), 200
    except Exception as e:
        return jsonify({"result": "error", "error": str(e)}), 500

@app.route('/mmf/xp_report', methods=['GET'])
def mmf_xp_report():
    try:
        proc = subprocess.run(["python", "xp_info_report.py"], capture_output=True, text=True, timeout=60)
        return jsonify({"result": "success", "stdout": proc.stdout}), 200
    except Exception as e:
        return jsonify({"result": "error", "error": str(e)}), 500

@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    event = request.json
    # 필요시 event의 내용에 따라 정책/XP/보상/알람 등 다양한 자동화 트리거 가능
    print("깃허브 이벤트 수신:", event)
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
