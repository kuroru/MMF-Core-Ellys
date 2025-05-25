from flask import Flask, request, jsonify
import os
import subprocess
import time
import json

print('### AGENT.PY 실행 경로:', os.path.abspath(__file__))

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY", "SuperSecretKey987654321!@#")

def is_authorized(req):
    if API_KEY:
        return req.headers.get("X-API-KEY") == API_KEY
    return True

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
    return jsonify({"status": "ok"})

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
    return jsonify({"status": "ok"})

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
        subprocess.run(["python", "scripts/generate_mmf_whitepaper.py"])
        os.system(f'git checkout -b {auto_branch}')
        os.system(f'git add {chapter_file} docs/MMF_Ellys_MVF_Whitepaper.md')
        os.system('git commit -m "백서 챕터 자동화 반영" || echo "No changes"')
        os.system(f'git push origin HEAD:{auto_branch}')
    return jsonify({"status": "ok", "branch": auto_branch})

# 4. 에러풀 자동화
@app.route('/update_errorpool', methods=['POST'])
def update_errorpool():
    if not is_authorized(request): return jsonify({"error": "Unauthorized"}), 401
    req = request.get_json()
    error_event = req.get("error_event", {})
    pool_file = req.get("pool_file", "errors/error_pool.json")
    if os.path.exists(pool_file):
        with open(pool_file, "r", encoding="utf-8") as f:
            error_list = json.load(f)
    else:
        error_list = []
    if error_event:
        error_list.insert(0, error_event)
        with open(pool_file, "w", encoding="utf-8") as f:
            json.dump(error_list, f, ensure_ascii=False, indent=2)
        os.system(f'git add {pool_file}')
        os.system(f'git commit -m "에러풀 자동화 업데이트" || echo "No changes"')
        os.system('git push')
    return jsonify({"status": "ok", "event_count": len(error_list)})

# 5. XP/보상 자동화
@app.route('/update_xp', methods=['POST'])
def update_xp():
    print('>>> update_xp called')
    if not is_authorized(request):
        print('>>> update_xp unauthorized')
        return jsonify({"error": "Unauthorized"}), 401
    req = request.get_json()
    print('>>> update_xp request json:', req)
    xp_event = req.get("xp_event", {})
    xp_file = req.get("xp_file", "xp/xp_table.json")
    if os.path.exists(xp_file):
        with open(xp_file, "r", encoding="utf-8") as f:
            xp_list = json.load(f)
    else:
        xp_list = []
    if xp_event:
        xp_list.insert(0, xp_event)
        with open(xp_file, "w", encoding="utf-8") as f:
            json.dump(xp_list, f, ensure_ascii=False, indent=2)
        os.system(f'git add {xp_file}')
        os.system(f'git commit -m "XP/보상 자동화 업데이트" || echo "No changes"')
        os.system('git push')
    print('>>> update_xp returning:', {"status": "ok", "event_count": len(xp_list)})
    return jsonify({"status": "ok", "event_count": len(xp_list)})

@app.route('/update_policy', methods=['POST'])
def update_policy():
    if not is_authorized(request): return jsonify({"error": "Unauthorized"}), 401
    req = request.get_json()
    policy_content = req.get("policy_content", "")
    policy_file = req.get("policy_file", "policies/mmf_policy.json")
    try:
        policy_json = json.loads(policy_content)
        with open(policy_file, "w", encoding="utf-8") as f:
            json.dump(policy_json, f, ensure_ascii=False, indent=2)
        os.system(f'git add {policy_file}')
        os.system(f'git commit -m "정책 파일 자동화 반영" || echo "No changes"')
        os.system('git push')
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    print(app.url_map)
    app.run(host="0.0.0.0", port=8080)

