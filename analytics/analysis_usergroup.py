# analytics/analysis_usergroup.py

import json
from collections import defaultdict, Counter
import glob
import re
import os

# 예시: user_profiles를 통한 사용자-직군 매핑
def load_user_profiles():
    if os.path.exists("meta/user_profiles.json"):
        with open("meta/user_profiles.json", "r", encoding="utf-8") as f:
            return json.load(f)
    # 샘플
    return {
        "testuser": {"직군": "대학생", "요금제": "basic"},
        "student2": {"직군": "중고등학생", "요금제": "free"},
        "consultantA": {"직군": "컨설턴트", "요금제": "pro"},
        # ...
    }

def parse_log_fname(fname):
    # logs/user_240526_01.log → ("user", "240526", "01")
    base = os.path.basename(fname)
    m = re.match(r"([a-zA-Z0-9]+)_(\d+)_(\d+)\.log", base)
    if m:
        return m.group(1), m.group(2), m.group(3)
    return None, None, None

def run_usergroup_analysis():
    user_profiles = load_user_profiles()
    files = glob.glob("logs/*.log")
    user_cmd_counter = defaultdict(Counter)
    job_cmd_counter = defaultdict(Counter)
    for fname in files:
        user, date, sess = parse_log_fname(fname)
        if not user: continue
        직군 = user_profiles.get(user, {}).get("직군", "미상")
        with open(fname, "r", encoding="utf-8") as f:
            for line in f:
                cmd = line.strip()
                user_cmd_counter[user][cmd] += 1
                job_cmd_counter[직군][cmd] += 1

    # 사용자별/직군별 TOP5 명령어 추출
    user_top = {u: c.most_common(5) for u, c in user_cmd_counter.items()}
    job_top = {j: c.most_common(5) for j, c in job_cmd_counter.items()}

    output = {
        "user_top_commands": user_top,
        "job_top_commands": job_top,
    }
    output_file = "meta/analysis_usergroup_240526.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"사용자/직군별 분석 완료! 결과: {output_file}")

if __name__ == "__main__":
    run_usergroup_analysis()
