# analytics/analysis_commands.py

import json
import re
from collections import Counter, defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import nltk
import Levenshtein
import os

nltk.download('punkt', quiet=True)

# 데이터 로드
def load_json(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

# 한글/영문 기초 토큰화
def preprocess(text):
    text = re.sub(r"[^가-힣A-Za-z0-9 ]", " ", text)
    return " ".join(nltk.word_tokenize(text))

def run_command_analysis(date="240526"):
    input_file = f"meta/daily_commands_{date}.json"
    commands = load_json(input_file)
    if not commands:
        print("명령어 데이터가 없습니다.")
        return

    commands_prep = [preprocess(cmd) for cmd in commands]

    # TF-IDF 벡터화 및 군집화
    vectorizer = TfidfVectorizer()
    X_cmd = vectorizer.fit_transform(commands_prep)
    num_clusters = min(5, len(commands_prep))
    if num_clusters > 1:
        kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X_cmd)
    else:
        clusters = [0] * len(commands_prep)

    # 클러스터별 그룹핑
    cmd_clustered = defaultdict(list)
    for idx, cl in enumerate(clusters):
        cmd_clustered[f"cluster_{cl}"].append(commands[idx])

    # 빈도 분석
    cmd_counts = Counter([cmd for cl in cmd_clustered.values() for cmd in cl])
    top_cmds = cmd_counts.most_common(5)

    # 유사명령 통합(Levenshtein Distance)
    synonyms_dict = defaultdict(list)
    for i, c1 in enumerate(commands):
        for j, c2 in enumerate(commands):
            if i != j:
                dist = Levenshtein.ratio(c1, c2)
                if dist > 0.7:
                    synonyms_dict[c1].append(c2)

    # 결과 저장
    output_file = f"meta/analysis_commands_{date}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({
            "clusters": cmd_clustered,
            "top_commands": top_cmds,
            "synonyms": synonyms_dict
        }, f, ensure_ascii=False, indent=2)

    print(f"명령어 분석 완료! (군집 수: {num_clusters}, TOP5: {top_cmds})")
    print(f"결과 파일: {output_file}")

# 단독 실행
if __name__ == "__main__":
    run_command_analysis()
