import json

def recommend_for_user(user_id, date="240526"):
    data = json.load(open(f"meta/analysis_usergroup_{date}.json", "r", encoding="utf-8"))
    user_top = data.get("user_top_commands", {}).get(user_id, [])
    job = None
    for u, info in json.load(open("meta/user_profiles.json")).items():
        if u == user_id:
            job = info.get("직군")
    job_top = data.get("job_top_commands", {}).get(job, []) if job else []
    return {
        "사용자 맞춤 TOP 명령": user_top,
        "직군별 인기 명령": job_top
    }

if __name__ == "__main__":
    print(recommend_for_user("testuser"))
