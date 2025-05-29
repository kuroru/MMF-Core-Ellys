"""
meta:
  updated: 2025-05-26T01:40:45
  author: master
  branch: main
  commit: latest
  tags: []
"""
from auto_patchnote import generate_patchnote

if __name__ == "__main__":
    generate_patchnote()
    print("패치노트 자동 생성 완료")
