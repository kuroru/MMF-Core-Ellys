import requests

devnote_content = """
# DEVELOP_NOTE.md

## 1. MMF 실전 자동화 엔진 개발 주요 이력 (2025-05-24~25)

- MMF-Core-Ellys 실전 자동화 백엔드 구축 (agent.py)
  - API_KEY 기반 인증, 멀티 엔드포인트 구조 도입
  - 전체 개발 환경, 파일 경로, 프로젝트 구조 정비

- 엔드포인트/기능별 자동화
  - /trigger : DEVELOP_NOTE.md 자동 생성·업데이트 (API+커밋+푸시 완전자동화)
  - /update_patchnote : 패치노트 자동화, docs/patch_notes/v3.x.x.md 자동 관리
  - /update_whitepaper : 백서 챕터 자동화, 분기 생성/통합 백서 PR 연동
  - /update_errorpool : errors/error_pool.json 자동화, 이벤트 기록·관리
  - /update_xp : xp/xp_table.json 기반 XP/보상 이벤트 자동화, 누적 관리

- 테스트 코드 및 실전 점검
  - 각 엔드포인트별 test_*.py(개발노트, 패치노트, 에러풀, XP, 백서 등) 구축
  - 모든 test_*.py에서 정상 응답, 자동화 커밋/푸시 동작 검증 완료
  - test_xp.py의 404/500 에러 및 JSONDecodeError 원인 추적, 함수 위치/구조 정상화로 100% 해결

- 자동화 장애 및 교훈
  - if __name__ == "__main__": 아래에 엔드포인트 함수가 있으면 Flask에서 인식하지 못해 404 발생(중복 금지)
  - 윈도우 환경에서 agent.py 파일 경로, 캐시, 중복 실행 등으로 인한 혼동 빈번 → print(app.url_map) 및 파일 로그로 명확히 관리
  - JSON 파일(에러풀, XP 등)은 반드시 UTF-8, 빈 배열 []로 초기화 필요(인코딩/포맷 오류 방지)
  - 서버 실행-테스트 실행 순서(항상 서버 켜고, 클라이언트 테스트)는 필수

- 깃허브 Actions/워크플로 동기화
  - DEVELOP_NOTE.md, 백서, 패치노트, XP/보상 등 자동 커밋/푸시→GitHub Actions로 PR/빌드/배포 트리거 확인
  - 모든 이력·정책·보상·이벤트는 깃허브 파일 중심 Source of Truth 정책으로 관리

## 2. 주요 자동화 성공/최종 현황

- 모든 엔드포인트(API)에서 정상 JSON 응답 확인 ({"status":"ok"} 등)
- DEVELOP_NOTE.md, docs/patch_notes, errors/error_pool.json, xp/xp_table.json 등 실제 파일에 누적 자동 반영 확인
- test_xp.py, test_devnote.py, test_errorpool.py 등 테스트 코드 일관 정상
- print(app.url_map)로 최종 라우트/엔드포인트 등록상태 검증 성공

## 3. 잔여 개선/운영 항목

- 자동화 엔드포인트 추가(정책, 메타, 보상 상세 등) 및 실시간 대시보드 고도화 예정
- 서버/테스트/워크플로 운영 안정성 추가 검증 및 운영 효율화 계속
- 윈도우 환경 실습/자동화시 경로, 인코딩, 포트 점유 등 체크리스트 강화 필요

---

**자동화 기반 MMF 실전 백엔드, 프론트엔드, 깃허브 워크플로 등
현업에서 필요한 모든 파이프라인/엔드포인트를 구현·연동 완료!
향후 정책/메타/보상/대시보드 등으로 확장 예정.**

## 2025-05-25 정책 자동화 성공 업데이트

- 정책 파일 자동화 엔드포인트(/update_policy) 신규 추가 및 실전 테스트 성공
  - policies/mmf_policy.json을 API 호출로 자동 생성/수정/커밋/푸시 완전 자동화
  - test_policy.py 통한 정상 응답(“{"status": "ok"}”) 및 정책 구조 자동 반영 확인
- 주요 개선/교훈:
  - 모든 엔드포인트는 if __name__ == "__main__": 블록 위에 정의해야 등록됨 (중복 금지)
  - JSON 파일(정책, XP, 에러풀 등)은 반드시 UTF-8/포맷 검증 필수
  - 윈도우 환경 포트 점유/중복 서버 실행 문제로 철저한 단일 프로세스 관리 필요
- 전체 MMF 자동화 구조가 DEVELOP_NOTE, PATCHNOTE, WHITEPAPER, ERRORPOOL, XP, POLICY 등
  - 모든 핵심 업무 파일/이벤트를 자동으로 생성·관리하는 실전 백엔드로 완성됨


(작성: 마스터, 2025-05-25)

"""


resp = requests.post(
    "http://127.0.0.1:8080/trigger",
    json={"devnote_content": devnote_content},
    headers={"X-API-KEY": "SuperSecretKey987654321!@#"}
)
print('응답 본문:', resp.text)
print(resp.json())
