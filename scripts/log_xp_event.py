# 파일: scripts/log_xp_event.py

import os
import json
import datetime

def log_xp_event(event, value, reason, file_path="xp/xp_table.json", user="master", log_path="meta/xp/xp_events_meta.json"):
    now = datetime.datetime.now().isoformat()
    entry = {
        "timestamp": now,
        "event": event,
        "value": value,
        "reason": reason,
        "user": user,
        "target_file": file_path
    }
    # 로그 파일 없으면 생성
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
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
    # 예시: 경험치 +20, 사유: "테스트 작업"
    log_xp_event(event="xp_add", value=20, reason="테스트 작업")
