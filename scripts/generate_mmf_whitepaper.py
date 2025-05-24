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
