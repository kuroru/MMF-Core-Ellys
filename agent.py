from flask import Flask, request, jsonify
import os
import subprocess
import time

app = Flask(__name__)

# 보안: API KEY 등 인증 필요시 이 변수 활용
API_KEY = os.environ.get("API_KEY", "")

def is_authorized(req):
    # 예시: 요청 헤더에 API 키 확인
    if API_KEY:
        return req.headers.get("X-API-KEY") == API_KEY
    return True  # 키 미사용시 무조건 허용

# 1. DEVELOP_NOTE.md 자동화
@app.route('/trigger', methods=['POST'])
def update_devnote():
    if not is_authorized(request): return jsonify({"error": "Unauthorized"}), 401
    req = request.get_json()
    devnote_content = req.get("devnote_content", "")
    if devnote_content.strip():
        with open("DEVELOP_NOTE.md", "w", encoding="utf-8") as f:
            f.write(devnote_content)
        os.system('git add DEVELOP_NOTE.md')
        os.system('git commit -m "DEVELOP_NOTE.md ChatGPT 자동화 반영" || echo "No changes"')
        os.system('git push')
    return {"status": "ok"}

# 2. 패치노트 자동화
@app.route('/update_patchnote', methods=['POST'])
def update_patchnote():
    if not is_authorized(request): return jsonify({"error": "Unauthorized"}), 401
    req = request.get_json()
    patchnote_content = req.get("patchnote_content", "")
    patchnote_file = req.get("patchnote_file", "docs/patch_notes/v3.5.1.md")
    if patchnote_content.strip():
        os.makedirs(os.path.dirname(patchnote_file), exist_ok=True)
        if os.path.exists(patchnote_file):
            with open(patchnote_file, "r", encoding="utf-8") as f:
                old_content = f.read()
        else:
            old_content = ""
        with open(patchnote_file, "w", encoding="utf-8") as f:
            f.write(patchnote_content + "\n\n" + old_content)
        os.system(f'git add {patchnote_file}')
        os.system(f'git commit -m "패치노트 자동 업데이트" || echo "No changes"')
        os.system('git push')
    return {"status": "ok"}

# 3. 백서(챕터) 자동화
@app.route('/update_whitepaper', methods=['POST'])
def update_whitepaper():
    if not is_authorized(request): return jsonify({"error": "Unauthorized"}), 401
    req = request.get_json()
    whitepaper_content = req.get("whitepaper_content", "")
    chapter_file = req.get("chapter_file", "docs/whitepaper/0_prologue.md")
    auto_branch = f"auto/gpt-{int(time.time())}"
    if whitepaper_content.strip():
        os.makedirs(os.path.dirname(chapter_file), exist_ok=True)
        with open(chapter_file, "w", encoding="utf-8") as f:
            f.write(whitepaper_content)
        # 통합 백서 자동생성
        subprocess.run(["python", "scripts/generate_mmf_whitepaper.py"])
        # 커밋/푸시 (새 브랜치)
        os.system(f'git checkout -b {auto_branch}')
        os.system(f'git add {chapter_file} docs/MMF_Ellys_MVF_Whitepaper.md')
        os.system('git commit -m "백서 챕터 자동화 반영" || echo "No changes"')
        os.system(f'git push origin HEAD:{auto_branch}')
    return {"status": "ok", "branch": auto_branch}

# 4. 필요시 정책/메타로그 등 추가 API도 이 구조로 확장

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
