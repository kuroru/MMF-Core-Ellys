import json

def log_meta_event(event, file_path, user="master", log_path=".github/meta_logs/meta_history.json"):
    now = datetime.datetime.now().isoformat()
    entry = {
        "timestamp": now,
        "event": event,
        "file": file_path,
        "user": user
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

# 기존 update_meta_block() 호출할 때마다 아래처럼 이벤트 기록
def update_meta_block(file_path, author="master", branch="main", commit="latest", tags=[]):
    ext = os.path.splitext(file_path)[1]
    try:
        with open(file_path, 'rb') as raw_f:
            raw = raw_f.read(4096)
            encoding = chardet.detect(raw)['encoding'] or 'utf-8'
        with open(file_path, 'r+', encoding=encoding, errors='replace') as f:
            content = f.read()
            if ext == '.md':
                content = re.sub(r"---\nmeta:([\s\S]+?)---\n", "", content, count=1)
            elif ext == '.py':
                content = re.sub(r'"""\nmeta:([\s\S]+?)"""\n', "", content, count=1)
            elif ext == '.json':
                content = re.sub(r'\{\s*"meta":\s*\{[^}]*\},?', "", content, count=1)
            f.seek(0)
            f.write(make_meta_block(file_path, author, branch, commit, tags) + content)
            f.truncate()
        # 이벤트 로그 기록 (여기!)
        log_meta_event("update_meta", file_path, author)
    except Exception as e:
        print(f"[SKIP] {file_path} 인코딩 불가({e})")
        log_meta_event("fail_meta_update", file_path, author)
