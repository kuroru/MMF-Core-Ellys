import re

def extract_insights(text):
    """
    사용자 입력에서 인사이트/아이디어/전략적 지시를 탐지.
    """
    patterns = [
        r"벤치마킹 할.*", r".*시장.*(많아|작아|포화|버짓).*",
        r".*아이디어.*", r".*접목해보자", r".*해보자",
        r".*방식.*제안", r".*전략.*추천", r".*위험.*분석"
    ]
    for pat in patterns:
        if re.search(pat, text, re.IGNORECASE):
            return text.strip()
    return None

# 단독 테스트용
if __name__ == "__main__":
    sample = "시장 버짓이 너무 많아, 아이디어를 다르게 내야할 것 같아"
    print(extract_insights(sample))
