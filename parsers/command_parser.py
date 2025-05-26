import re

def extract_commands(text):
    """
    사용자 입력에서 명령어 패턴을 탐지해서 리턴.
    패턴은 확장 가능. 반환: 명령어(문자열) 또는 None
    """
    patterns = [
        r"(XP|경험치)[\s\S]*?(리포트|보고서|내역).*",
        r"(정책|프로토콜)[\s\S]*?(동기화|업데이트|변경).*",
        r"(패치노트|개발노트|릴리즈).*",
        r"(보상|리워드)[\s\S]*?(내역|기록|정산).*"
    ]
    for pat in patterns:
        if re.search(pat, text, re.IGNORECASE):
            return text.strip()
    return None

# 단독 테스트용
if __name__ == "__main__":
    sample = "XP 내역 리포트로 남겨줘"
    print(extract_commands(sample))  # "XP 내역 리포트로 남겨줘"
