import subprocess

def commit_and_push_handshake_log():
    subprocess.run(["git", "config", "--global", "user.name", "auto-bot"])
    subprocess.run(["git", "config", "--global", "user.email", "auto-bot@example.com"])
    subprocess.run(["git", "add", "logs/handshake_history.json"])
    subprocess.run(["git", "commit", "-m", "chore: update handshake_history.json [auto]"])
    # 인증 방식: https + PAT(환경변수, 시크릿에 저장)
    subprocess.run([
        "git", "push", "https://<GITHUB_USER>:<GH_PAT>@github.com/<USER>/<REPO>.git", "main"
    ])
