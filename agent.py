from flask import Flask, request
import os

app = Flask(__name__)

# 1. DEVELOP_NOTE.md 자동화
@app.route('/trigger', methods=['POST'])
def update_devnote():
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

if __name__ == "__main__":
    app.run(port=8080)
