# PROGRESS (2026-10-06 기준, 규칙은 SPEC.md·.clinerules 참고)

## 끝난 단계
1. SPEC 구현: `app.py`(라우트), `schema.sql`, `templates/index.html`, `static/css/style.css`, `test_app.py`(SPEC 6장 테스트 13개)
2. DB 분리 리팩터링: `db.py` 신설(init_db·get_todos·add_todo·toggle_todo·delete_todo, 모두 첫 인자로 DB 경로를 받음). app.py 라우트는 이 함수만 호출하고 `DATABASE`를 호출 시점에 넘긴다(테스트가 `app.DATABASE`를 바꾸기 때문).

## 스펙과 다른 부분
- 정렬에 `id DESC` 추가: 같은 초에 생긴 항목도 최신순 보장.
- `GET /`는 테이블이 아닌 `<ul>` 목록: 화면 명세(5장)와 기존 테스트가 `<ul>` 기준.
- `db.py`는 SPEC 파일 구성에 없음: 리팩터링 요청으로 추가.
- `init_db()`를 import 시점에 호출: `flask run`에서도 테이블 생성. created_at은 UTC 그대로 표시.

## 남은 일
- [ ] 진행 중이던 작업(요구사항 미확인): app.py `index()`가 `incomplete_todos`/`completed_todos`를 넘기지만 index.html은 아직 `todos`를 써서 목록이 비어 보이고 테스트 2개 실패(test_index_newest_first, test_add_long_title). 사용자에게 의도 확인 후 템플릿 수정 또는 되돌리기.
- [ ] database.db 정리: 테스트 오염 데이터 id 3~20(18건), 원래 항목 '11'(id 1)은 삭제됨. 삭제 여부는 사용자 확인 필요.
- [ ] git 미커밋 상태(폴더 전체 untracked).
