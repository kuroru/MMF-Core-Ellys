## 0. 인프라 및 연동 정보

- **Cloud Run 중계서버**
  - URL: [https://mmf-hook-1042382168153.asia-northeast3.run.app](https://mmf-hook-1042382168153.asia-northeast3.run.app)
  - 설명: ChatGPT, 자동화 시스템에서 /trigger 등 API POST로 자동화 트리거

  - 주요 포트: 8080 (Cloud Run), 5000 (로컬 Flask)
  - API: POST /trigger (devnote_content 포함 가능)
  
  - 인증: Authorization 헤더(토큰, 환경변수), 관리자/담당자 정보 포함 권장


# 센티넬 개발노트

**생성일:** 2025-05-24 20:28

## 1. 전체 개발 현황


## 2. 개발된 기능 요약


## 3. 향후 개발계획
- XP/레벨/보상 고도화
- 알림/연동 자동화, 대시보드 시각화

## 4. 마스터 요구사항
- 모든 메타파일 경로 표기, 평문 우선 표기
- XP/보상/레벨 개별 자동화

## 5. 정책/의사결정 이력
- 알림(훅) 후순위, 실전 피드백 우선
- MMF 선언→개발노트 자동확인

DEVELOP_NOTE.md (2025-05-26 기준)
📅 MMF 개발노트 & 작업 현황 (2025-05-26)
1. 개발/운영 환경
Docker/WSL2 미사용, 윈도우 로컬 파이썬 환경에서 모든 작업 진행

패키지(flask, pandas, tabulate, chardet 등) 직접 pip 설치

2. 폴더/파일 구조
scripts/hud_api_server.py : API 서버(검증/이력/승인 포함)

meta/history.json : 이벤트/검증/관리자 액션 이력 저장(빈 배열로 생성)

frontend/PatchnoteHUD.jsx : 정책/패치노트 검증 HUD, 이력 테이블

docs/patch_notes/ : 패치노트 폴더

3. 주요 작업 내역
MMF API 서버, 이력관리, 검증/복원/승인 기능 로컬 환경에서 완성/테스트

프론트엔드 HUD에서 API 연동, 이력 실시간 표시, 내보내기 기능 설계

Docker/Cloud Run은 환경 복구 후 별도 마이그레이션 예정

VSCode/Pylance 경고는 pip 설치/import로 대부분 해결

4. API/기능 테스트 현황
/api/verify_event?type=patchnote&keyword=시그니처 보상

/api/event_log

관리자 승인/정책 복원 등 모든 엔드포인트 로컬에서 테스트 OK

5. 다음 과제/To-Do
대량 이력 최적화, 필드/승인 UX/내보내기 고도화

Docker/Cloud Run 환경 재설정 후 배포 자동화

운영 보안 점검 및 정책/시크릿 패턴 재정비

⏺️ [자동화 메타]
모델: 엘리스 (GPT-4.1)

세션: MMF 개발노트/진행상황

답번호: 112

일시: 2025-05-26 03:19