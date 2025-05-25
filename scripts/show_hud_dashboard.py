# 파일: scripts/show_hud_dashboard.py

import json
import os
from tabulate import tabulate

LOG_PATHS = [
    (".github/meta_logs/meta_history.json", "정책"),
    ("meta/xp/xp_events_meta.json", "XP"),
    ("meta/error/error_events_meta.json", "에러"),
    ("meta/reward/reward_events_meta.json", "보상")
]

def load_events(log_path, label, count=10):
    if not os.path.exists(log_path):
        return []
    with open(log_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except Exception:
            return []
    # 최신 N개만 역순 정렬
    events = list(reversed(data[-count:]))
    for e in events:
        e["category"] = label
    return events

def show_hud_dashboard(count=10):
    all_events = []
    for path, label in LOG_PATHS:
        all_events.extend(load_events(path, label, count))
    # 시간순 정렬
    all_events.sort(key=lambda e: e.get("timestamp", ""), reverse=True)
    # 주요 필드만 추출
    table = []
    for e in all_events:
        table.append([
            e.get("timestamp", ""),
            e.get("category", ""),
            e.get("event", ""),
            e.get("user", ""),
            e.get("reason", e.get("message", "")),
            e.get("target_file", e.get("file", "")),
        ])
    print(tabulate(
        table,
        headers=["시간", "종류", "이벤트", "유저", "사유/메시지", "파일"],
        tablefmt="github"
    ))

if __name__ == "__main__":
    show_hud_dashboard()
