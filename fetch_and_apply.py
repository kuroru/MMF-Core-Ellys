import os
import requests
import datetime
import json

# --------- 사용자 설정(필수) ----------
GITHUB_USER = "kuroru"
REPO = "MMF-Core-Ellys"
BRANCH = "main"
FILES_TO_FETCH = [
    ("policies/mmf_policy.json", "./policies/mmf_policy.json"),
    ("xp/xp_table.json", "./xp/xp_table.json"),
]
LOG_DIR = "./logs"
# -------------------------------------

def log_event(event_type, content):
    """센티넬 로그 기록"""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(LOG_DIR, f"{event_type}_{now}.log")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[센티넬] {event_type} 기록됨 → {log_path}")

def fetch_github_file(repo, branch, github_path, local_path):
    """깃허브에서 파일 fetch & 저장"""
    url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{repo}/{branch}/{github_path}"
    try:
        r = requests.get(url)
        if r.status_code != 200:
            log_event("handshake_error", f"Fetch 실패: {url}\n상태코드: {r.status_code}\n내용: {r.text}")
            return False
        # 저장 폴더 자동 생성
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, "w", encoding="utf-8") as f:
            f.write(r.text)
        log_event("handshake_success", f"성공적으로 fetch: {url}\n→ {local_path}")
        return True
    except Exception as e:
        log_event("handshake_error", f"예외 발생: {url}\n{e}")
        return False

def validate_json_schema(local_path, required_keys=None):
    """파일이 json 포맷 + (선택적으로) 필드까지 검증"""
    try:
        with open(local_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if required_keys:
            missing = [k for k in required_keys if k not in data]
            if missing:
                log_event("sentinel_warning", f"{local_path}에 누락 필드: {missing}")
                return False
        log_event("sentinel_report", f"{local_path} json 파싱 및 구조 검증 통과")
        return True
    except Exception as e:
        log_event("sentinel_error", f"{local_path} 파싱 실패\n{e}")
        return False

def main():
    print("MMF 자동 정책/XP 연동 시작 (센티넬 ON)")
    for github_path, local_path in FILES_TO_FETCH:
        print(f"▶ {github_path} fetch 시도...")
        ok = fetch_github_file(REPO, BRANCH, github_path, local_path)
        if ok:
            # 정책/XP 구조 필드 간단 검증 (예시, 필요에 따라 수정)
            if "policy" in github_path:
                validate_json_schema(local_path, required_keys=["policies"])
            if "xp_table" in github_path:
                validate_json_schema(local_path)
        else:
            print(f"[에러] {github_path} fetch 실패 (자세한 내용은 logs 폴더 참조)")

    print("\n모든 fetch/검증/적용 종료! (상세 기록은 logs 폴더 참조)")

if __name__ == "__main__":
    main()
