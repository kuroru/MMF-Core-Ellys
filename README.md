---
meta:
  updated: 2025-05-26T01:40:45
  author: master
  branch: main
  commit: latest
  tags: []
---
# MMF-Core-Ellys

본 레포는 MMF(메트릭스 메타 프레임워크) 코어 구조 및 자동화/검증/XP 엔진을 구현합니다.
- 모든 공식 정책/오류/XP/핸드셰이크/시그니처보상 정보는 이 레포 기준으로 불러오며, 캔버스/지피티 자료는 보조 참조만 사용합니다.

# MMF-Core-Ellys
최소실행버전(MVF) MMF 프레임워크.  
주요 구조: docs, errors, policies, patch_notes, scripts, sentinel, xp, handshake
예시: 전략설계, 에러로그, XP보상 통합 관리

# MMF-Core-Ellys
완전자동화까지 얼마 안남았다....... (2020-07-28)

# MMF Scalable Base (GitHub-Centric)
MMF-Scalable-Base/
├── logs/
│   └── (user_240526_01.log 등)
├── meta/
│   ├── commands.json
│   ├── insights.json
│   ├── daily_commands_240526.json
│   └── daily_insights_240526.json
├── parsers/
│   ├── command_parser.py
│   └── insight_parser.py
├── schedulers/
│   └── batch_collector.py
├── api/
│   └── recommend.py
├── .github/
│   └── workflows/
│       └── mmf_auto_batch.yml
└── README.md

## 목적
- 모든 사용자 대화 로그, 명령, 인사이트, 정책/리포트/패턴을 깃허브 기반으로 데이터화·자동화·버전 관리
- 미래의 서드파티·플러그인·직군/요금제별 확장 대응

## 폴더 구조
- `/logs/`       : 세션별/일자별 사용자 로그(raw)
- `/meta/`       : 정제된 명령어/인사이트/유저/패턴 데이터셋
- `/parsers/`    : 명령/인사이트 파싱 모듈
- `/schedulers/` : 일일 배치 수집/동기화 스크립트
- `/api/`        : 추천/동기화/외부 연동 API
- `/.github/`    : 워크플로, 자동 배치, 배포, 액션

## 시작 사용법
1. **대화/작업 로그**를 `/logs/`에 저장
2. **파서**가 명령/인사이트 추출 → `/meta/`로 저장
3. **schedulers/batch_collector.py**로 매일 24시 배치 실행
4. **meta/** 데이터 커밋/푸시 (깃허브 Actions 가능)
5. **api/recommend.py** 등에서 실시간 추천/동기화/외부 연동

## 확장 포인트
- 슬랙/웹/서드파티 플러그인 연동
- 요금제별, 직군별, 사용자별 맞춤 추천
- 공식 명령어/인사이트 데이터셋 API 배포

## 라이선스/기여
- 누구나 PR/이슈/플러그인 환영
- MIT License
- kuroru@naver.com