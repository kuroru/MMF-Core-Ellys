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
