from flask import Flask, request, Response
import os
import re
import json

PATCH_DIR = 'docs/patch_notes/'

app = Flask(__name__)

def search_patchnotes_for_facts(keywords):
    matches = []
    for fname in os.listdir(PATCH_DIR):
        if fname.endswith(".md"):
            with open(os.path.join(PATCH_DIR, fname), 'r', encoding='utf-8') as f:
                text = f.read()
                for kw in keywords:
                    if kw in text:
                        matches.append({
                            "file": fname,
                            "keyword": kw,
                            "context": "\n".join(re.findall(rf".{{0,30}}{kw}.{{0,30}}", text))
                        })
    return matches

@app.route("/api/verify_event")
def verify_event():
    event_type = request.args.get("type")
    keyword = request.args.get("keyword")
    search_targets = {
        "patchnote": "docs/patch_notes/",
        # 향후 "policy", "xp", "error" 등 확장 가능
    }
    if event_type not in search_targets or not keyword:
        return Response(json.dumps({"status": "error", "message": "type, keyword 필요"}, ensure_ascii=False),
                        content_type="application/json; charset=utf-8"), 400
    if event_type == "patchnote":
        results = search_patchnotes_for_facts([keyword])
        resp = {"status": "ok"}
        if results:
            resp["found"] = True
            resp["matches"] = results
        else:
            resp["found"] = False
            resp["message"] = "공식 패치노트에 기록 없음"
        return Response(json.dumps(resp, ensure_ascii=False),
                        content_type="application/json; charset=utf-8")

@app.route("/api/restore_policy", methods=["POST"])
def restore_policy():
    # 실제 정책 파일 롤백/복원 코드는 여기에
    # 로그 기록 및 관리자 알림도 여기에
    return Response(json.dumps({"status": "ok", "message": "정책 복원/승인 트리거"}), content_type="application/json; charset=utf-8")

@app.route("/api/health")
def health():
    resp = {"status": "ok", "service": "MMF HUD API"}
    return Response(json.dumps(resp, ensure_ascii=False, indent=2),
                    content_type="application/json; charset=utf-8")

if __name__ == "__main__":
    app.run(port=8080, debug=True)
