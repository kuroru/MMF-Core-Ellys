# 파일: scripts/log_policy_event.py

import os
import json
import datetime
import hashlib

def hash_file(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def log_policy_event(event, file_path, user="master", log_path=".github/meta_logs/meta_history.json"):
    now = datetime.datetime.now().isoformat()
    entry = {
        "timestamp": now,
        "event": event,
        "file": file_path,
        "user": user,
        "file_hash": hash_file(file_path)
    }
    # 파일 없으면 생성
    if not os.path.exists(log_path):
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    # 기록 추가
    with open(log_path, 'r+', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except Exception:
            data = []
        data.append(entry)
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.truncate()

if __name__ == "__main__":
    policy_file = "policies/mmf_policy.json"
    user = "master"
    log_policy_event("policy_update", policy_file, user)
