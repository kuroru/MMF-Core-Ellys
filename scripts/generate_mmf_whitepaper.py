import os

chapters = [
    "0_prologue.md",
    "1_structure.md",
    "2_modules.md",
    "3_automation.md",
    "4_practice.md",
    "5_roadmap.md"
]
base_dir = "docs/whitepaper"
output_file = "docs/MMF_Ellys_MVF_Whitepaper.md"

# ✨ [여기 추가] 챕터 md 파일 없으면 자동 생성
chapter_titles = [
    "# 0장. 프롤로그 & MMF 철학\n",
    "# 1장. MMF Core 전체 구조\n",
    "# 2장. 핵심 모듈/컴포넌트 상세\n",
    "# 3장. 자동화·운영 시나리오\n",
    "# 4장. 실전 운영 사례·Best Practice\n",
    "# 5장. 미래 확장·로드맵\n"
]
os.makedirs(base_dir, exist_ok=True)
for ch, title in zip(chapters, chapter_titles):
    path = os.path.join(base_dir, ch)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(title)
        print(f"{ch} 자동 생성")

# 최종 백서 파일 합치기 (기존 코드)
with open(output_file, "w", encoding="utf-8") as out:
    for ch in chapters:
        path = os.path.join(base_dir, ch)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                out.write(f.read())
                out.write("\n\n---\n\n")
        else:
            out.write(f"# [미작성] {ch}\n\n---\n\n")

print(f"{output_file} 자동 생성 완료.")
