import glob, json
from parsers.command_parser import extract_commands
from parsers.insight_parser import extract_insights

def batch_collect():
    files = glob.glob("logs/*.log")
    daily_commands, daily_insights = [], []
    for fname in files:
        with open(fname, "r", encoding="utf-8") as f:
            for line in f:
                cmd = extract_commands(line)
                if cmd: daily_commands.append(cmd)
                insight = extract_insights(line)
                if insight: daily_insights.append(insight)
    with open("meta/daily_commands_240526.json", "w", encoding="utf-8") as f:
        json.dump(daily_commands, f, ensure_ascii=False, indent=2)
    with open("meta/daily_insights_240526.json", "w", encoding="utf-8") as f:
        json.dump(daily_insights, f, ensure_ascii=False, indent=2)

# 단독 실행 예시
if __name__ == "__main__":
    batch_collect()
    print("일일 명령/인사이트 메타 추출 완료")
