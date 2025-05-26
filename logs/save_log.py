import datetime

def save_log(user_id, session_id, message):
    date = datetime.date.today().strftime("%y%m%d")
    fname = f"logs/{user_id}_{date}_{session_id}.log"
    with open(fname, "a", encoding="utf-8") as f:
        f.write(message.strip() + "\n")

# 단독 테스트
if __name__ == "__main__":
    save_log("testuser", "001", "XP 내역 리포트로 남겨줘")
    save_log("testuser", "001", "시장 버짓이 너무 많아, 아이디어를 다르게 내야할 것 같아")
