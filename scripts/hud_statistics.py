import json
import pandas as pd
from collections import Counter

# 예: XP 이벤트 집계
with open('meta/xp/xp_events_meta.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['timestamp']).dt.date

# 유저별 XP 총합 랭킹
user_xp = df.groupby('user')['value'].sum().sort_values(ascending=False)
print("유저별 XP 랭킹\n", user_xp)

# 일간 XP 변화
daily_xp = df.groupby('date')['value'].sum()
print("일간 XP 변화\n", daily_xp)
