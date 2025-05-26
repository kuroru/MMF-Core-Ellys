import json
import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정 (Windows 기준. Mac/Linux는 폰트명만 변경)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

import glob
import re
import os

def collect_trend_data(meta_path="meta/"):
    # 일자별 명령/인사이트 파일 자동 집계
    cmd_trend = {}
    ins_trend = {}

    cmd_files = sorted(glob.glob(os.path.join(meta_path, "daily_commands_*.json")))
    ins_files = sorted(glob.glob(os.path.join(meta_path, "daily_insights_*.json")))

    for fname in cmd_files:
        date = re.findall(r"(\d{6,})", fname)[-1]
        with open(fname, "r", encoding="utf-8") as f:
            cmds = json.load(f)
        for cmd in cmds:
            cmd_trend.setdefault(cmd, {})[date] = cmd_trend.get(cmd, {}).get(date, 0) + 1

    for fname in ins_files:
        date = re.findall(r"(\d{6,})", fname)[-1]
        with open(fname, "r", encoding="utf-8") as f:
            ins = json.load(f)
        for i in ins:
            ins_trend.setdefault(i, {})[date] = ins_trend.get(i, {}).get(date, 0) + 1

    return cmd_trend, ins_trend

def make_trend_df(trend_dict):
    # 데이터프레임 변환
    df = pd.DataFrame(trend_dict).fillna(0).astype(int)
    df.index.name = 'date'
    return df

def plot_trend(df, title, top_n=3):
    total = df.sum()
    top_items = total.sort_values(ascending=False).head(top_n).index
    df[top_items].plot(figsize=(8,5), marker="o")
    plt.title("Top 3 Command Trends")      # 영문
    plt.xlabel("Date")                     # 영문
    plt.ylabel("Count")                    # 영문
    plt.legend(title="Command")            # 영문
    plt.tight_layout()
    plt.show()


def main():
    cmd_trend, ins_trend = collect_trend_data()
    # 명령 트렌드
    cmd_df = make_trend_df(cmd_trend)
    print("명령 트렌드 데이터프레임:\n", cmd_df.tail())
    plot_trend(cmd_df, "명령어 트렌드 TOP3")
    # 인사이트 트렌드
    ins_df = make_trend_df(ins_trend)
    print("인사이트 트렌드 데이터프레임:\n", ins_df.tail())
    plot_trend(ins_df, "인사이트 트렌드 TOP3")

if __name__ == "__main__":
    main()
