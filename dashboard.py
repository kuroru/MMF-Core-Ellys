import streamlit as st
import pandas as pd
import json

st.set_page_config(layout="wide")
st.title("MMF Command/Insight Trend Dashboard")

date = st.selectbox("분석 일자", ["240524", "240525", "240526"])
with open(f"meta/analysis_commands_{date}.json", "r", encoding="utf-8") as f:
    data = json.load(f)
df = pd.DataFrame.from_dict(data["clusters"], orient="index").T
st.line_chart(df.fillna(0))

st.write("TOP5 추천 명령:")
for cmd, cnt in data["top_commands"]:
    st.write(f"- {cmd} ({cnt}회)")
