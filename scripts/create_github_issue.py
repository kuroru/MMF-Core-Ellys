import subprocess

def create_github_issue(repo, title, body):
    cmd = [
        "gh", "issue", "create",
        "--repo", repo,
        "--title", title,
        "--body", body
    ]
    # gh CLI 인증 필요(1회 gh auth login 후 사용)
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("에러:", result.stderr)

# 사용 예시
if __name__ == "__main__":
    repo = "kuroru/MMF-Core-Ellys"
    title = "테스트 자동화 이슈"
    body = "자연어 명령→구글런→깃허브 자동화 실전 루프 테스트"
    create_github_issue(repo, title, body)
