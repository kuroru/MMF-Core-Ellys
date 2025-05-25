# Cloud Run(구글 런) 공식 서비스 주소
# 서비스 명: MMF-Hook 중계서버

- Cloud Run URL:
- https://mmf-hook-1042382168153.asia-northeast3.run.app

- 설명:

- ChatGPT, 외부 봇/자동화 시스템에서
- 자동화 트리거(API POST)로 사용

- GitHub Actions 워크플로(dispatch) 트리거 및
- 개발노트(DEVELOP_NOTE.md) 실시간 커밋/푸시 연동

- 주요 포트:

- 8080(Cloud Run 기본),

- 개발용 Flask는 5000(로컬 테스트)

- API 주요 경로:

- POST /trigger (자동화 명령 실행, 본문에 “devnote_content” 포함 가능)

- (Webhook, REST API 등 추가 확장 가능)


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
