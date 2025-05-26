import subprocess

user_input = input("명령을 입력하세요: ")
if "mmf 시작" in user_input:
    print("MMF 시작 선언 감지 → 운영 자동화 시퀀스 실행!")
    subprocess.run(["python", "mmf_bootstrap.py"])
else:
    print("지원하지 않는 명령입니다.")
