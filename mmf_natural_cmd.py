import subprocess

def process_natural_command(user_input):
    if "mmf 시작" in user_input:
        print("🤖 MMF 핸드셰이크 실행!")
        result = subprocess.run(["python", "mmf_handshake.py"], capture_output=True, text=True)
        print(result.stdout)
        # 필요시 디스코드 알림, 로그 등도 추가 출력

if __name__ == "__main__":
    user_input = input("명령을 입력하세요: ")
    process_natural_command(user_input)
