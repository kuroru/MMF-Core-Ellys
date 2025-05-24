import datetime
import json
import os

# === 실전 메타데이터/요구사항 파일 경로 (경로 필요시 수정) ===
meta_history_path = ".github/meta_logs/meta_history.json"
xp_events_path = "meta/xp/xp_events_meta.json"
requirements_path = "meta/requirements.json"  # 예: 요구사항 자동 누적시

def read_last_n(file, n=5):
    if not os.path.exists(file): return []
    with open(file, encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return data[-n:]
            else:
                return [data]
        except Exception:
            return []

# 1. 개발현황: 최근 메타이벤트
dev_status = []
for item in read_last_n(meta_history_path, 5):
    dev_status.append(f"- {item.get('datetime', '')}: {item.get('event', '')} ({item.get('file', '')}) {item.get('desc', '')}")

# 2. 개발된 기능: 최근 XP 이벤트
feature_list = []
for item in read_last_n(xp_events_path, 3):
    feature_list.append(f"- {item.get('datetime', '')}: {item.get('event', '')} [{item.get('대상', '')}] XP: {item.get('누적_xp', '')}")

# 3. 향후 개발계획 (직접 입력 또는 파일 연동)
future_plan = [
    "- XP/레벨/보상 고도화",
    "- 알림/연동 자동화, 대시보드 시각화"
]

# 4. 요구사항(자동 + 직접)
requirements = []
for item in read_last_n(requirements_path, 5):
    requirements.append(f"- {item.get('datetime', '')}: {item.get('요구', '')}")

# 직접입력 요구 병행
requirements += [
    "- 모든 메타파일 경로 표기, 평문 우선 표기",
    "- XP/보상/레벨 개별 자동화"
]

# 5. 정책/결정 이력(샘플)
policy = [
    "- 알림(훅) 후순위, 실전 피드백 우선",
    "- MMF 선언→개발노트 자동확인"
]

with open("DEVELOP_NOTE.md", "w", encoding="utf-8") as f:
    f.write(f"# 센티넬 개발노트\n\n")
    f.write(f"**생성일:** {datetime.datetime.now():%Y-%m-%d %H:%M}\n\n")
    f.write("## 1. 전체 개발 현황\n")
    f.write('\n'.join(dev_status) + "\n\n")
    f.write("## 2. 개발된 기능 요약\n")
    f.write('\n'.join(feature_list) + "\n\n")
    f.write("## 3. 향후 개발계획\n")
    f.write('\n'.join(future_plan) + "\n\n")
    f.write("## 4. 마스터 요구사항\n")
    f.write('\n'.join(requirements) + "\n\n")
    f.write("## 5. 정책/의사결정 이력\n")
    f.write('\n'.join(policy) + "\n")
