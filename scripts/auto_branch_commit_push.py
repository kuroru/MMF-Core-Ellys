import subprocess

def auto_git_flow(repo_dir, branch_name, commit_msg, file_to_edit, new_content):
    subprocess.run(['git', 'checkout', 'main'], cwd=repo_dir)
    subprocess.run(['git', 'pull'], cwd=repo_dir)
    subprocess.run(['git', 'checkout', '-b', branch_name], cwd=repo_dir)
    # 파일 수정
    with open(f"{repo_dir}/{file_to_edit}", 'w', encoding='utf-8') as f:
        f.write(new_content)
    subprocess.run(['git', 'add', file_to_edit], cwd=repo_dir)
    subprocess.run(['git', 'commit', '-m', commit_msg], cwd=repo_dir)
    subprocess.run(['git', 'push', '-u', 'origin', branch_name], cwd=repo_dir)

# 사용 예시
if __name__ == "__main__":
    repo_dir = "/경로/MMF-Core-Ellys"
    branch_name = "feature/auto-pr-test"
    commit_msg = "자동화 PR 테스트 커밋"
    file_to_edit = "README.md"
    new_content = "PR 자동화 루프 테스트!"
    auto_git_flow(repo_dir, branch_name, commit_msg, file_to_edit, new_content)
