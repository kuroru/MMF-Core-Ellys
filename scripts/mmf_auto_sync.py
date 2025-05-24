import json, datetime

record = {
    "dt": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
    "status": "success",   # 또는 "fail"
    "diff": ["xp_table"]   # 리스트, 없으면 []
}
file = "handshake/handshake_history.json"
try:
    data = json.load(open(file, encoding="utf-8"))
except:
    data = []
data.insert(0, record)
json.dump(data, open(file, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
