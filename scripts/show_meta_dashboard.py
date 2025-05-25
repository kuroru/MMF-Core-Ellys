import json
from tabulate import tabulate

def show_meta_dashboard(log_path=".github/meta_logs/meta_history.json", count=10):
    with open(log_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # 최신 N개만 역순으로 정렬
    recent = list(reversed(data[-count:]))
    # 표 형태 변환
    table = [
        [e.get("event"), e.get("file"), e.get("timestamp"), e.get("user")]
        for e in recent
    ]
    print(tabulate(table, headers=["이벤트", "파일", "시간", "유저"], tablefmt="github"))

if __name__ == "__main__":
    show_meta_dashboard()
