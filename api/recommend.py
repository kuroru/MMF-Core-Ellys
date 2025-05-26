import json

def load_json(fname):
    try:
        with open(fname, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def recommend_top_commands(date="240526"):
    data = load_json(f"meta/analysis_commands_{date}.json")
    tops = data.get("top_commands", [])
    rec = [f"추천 명령: {cmd} ({cnt}회)" for cmd, cnt in tops]
    return rec

# 단독 테스트
if __name__ == "__main__":
    print(recommend_top_commands())
