# SPEC.md

## 1. 개요
Python Flask와 SQLite를 활용하여 만드는 심플한 할 일 관리(Todo) 웹 애플리케이션입니다. 사용자는 할 일을 등록하고, 목록을 확인하며, 완료 상태를 변경하거나 삭제할 수 있습니다.

## 2. 기술
- **Language**: Python 3.x
- **Framework**: Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3 (Pure CSS, no frameworks)

## 3. 파일 구성
```text
todo_app/
├── app.py              # Flask 애플리케이션 메인 로직 및 라우트
├── database.db         # SQLite 데이터베이스 파일
├── schema.sql          # 데이터베이스 초기 생성 스크립트
├── static/
│   └── css/
│       └── style.css   # 앱 디자인을 위한 스타일시트
└── templates/
    └── index.html      # 할 일 목록 및 입력 폼을 담은 메인 페이지
```

## 4. 동작 규칙

| 라우트 | 메서드 | 입력 | 결과 |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | 없음 | 전체 할 일 목록 페이지 렌더링 |
| `/add` | `POST` | `title` (non-empty string) | 새로운 할 일 DB 저장 후 `/`로 리다이렉트 |
| `/add` | `POST` | `title` (empty or whitespace) | 400 Bad Request 반환 |
| `/toggle/<int:todo_id>` | `POST` | `todo_id` (int) | 해당 ID의 `is_completed` 상태 반전 후 `/`로 리다이렉트 |
| `/toggle/<int:todo_id>` | `POST` | `todo_id` (non-existent) | 404 Not Found 반환 |
| `/delete/<int:todo_id>` | `POST` | `todo_id` (int) | 해당 ID의 데이터 삭제 후 `/`로 리다이렉트 |
| `/delete/<int:todo_id>` | `POST` | `todo_id` (non-existent) | 404 Not Found 반환 |

## 5. 화면
- **메인 페이지 (`index.html`)**:
  - 상단: 할 일을 입력할 수 있는 텍스트 입력창과 '추가' 버튼
  - 중앙: 할 일 목록 (생성 시각 내림차순 정렬)
    - 각 항목 좌측: 완료 여부에 따른 체크박스 또는 텍스트 스타일 변화
    - 각 항목 내용: 제목 및 생성 시각
    - 각 항목 우측: '삭제' 버튼
- **디자인**: 외부 프레임워크 없이 `style.css`를 통해 깔끔하고 가독성 있는 레이아웃 구현

## 6. 테스트

| 요청 | 기대하는 결과 |
| :--- | :--- |
| `GET /` | 200 OK, 할 일 목록 테이블이 포함된 HTML 응답 |
| `POST /add` (제목: "공부하기") | 302 Redirect, DB에 "공부하기"가 저장됨 |
| `POST /add` (제목: "") | 400 Bad Request, 빈 문자열은 허용 안 함 |
| `POST /add` (제목: "   ") | 400 Bad Request, 공백만 있는 문자열은 허용 안 함 |
| `POST /add` (매우 긴 제목) | 200 OK, 데이터가 정상적으로 저장됨 |
| `POST /toggle/1` (ID 1번 존재) | 302 Redirect, ID 1번 항목의 완료 여부가 바뀜 |
| `POST /toggle/999` (존재하지 않는 ID) | 404 Not Found |
| `POST /toggle/abc` (잘못된 타입) | 404 Not Found |
| `POST /delete/1` (ID 1번 존재) | 302 Redirect, ID 1번 항목이 삭제됨 |
| `POST /delete/999` (존재하지 않는 ID) | 404 Not Found |
| `POST /delete/abc` (잘못된 타입) | 404 Not Found |
| `GET /non-existent-route` | 404 Not Found |

## 7. 완료 전 점검
- [ ] SQLite 데이터베이스가 정상적으로 생성되고 초기화되는가?
- [ ] 할 일을 추가했을 때 최신순으로 목록 상단에 나타나는가?
- [ ] 완료 표시를 클릭했을 때 시각적으로 변화(취소선 등)가 나타나는가?
- [ ] 삭제 버튼을 눌렀을 때 데이터가 DB와 화면에서 모두 제거되는가?
- [ ] CSS가 외부 라이브러리 없이 의도한 대로 적용되었는가?

## 8. 하지 않는 것
- 사용자 로그인 및 회원가입 기능
- 기존 할 일 내용 수정(Update) 기능
- Bootstrap, Tailwind CSS 등 외부 CSS 프레임워크 사용
- React, Vue 등 자바스크립트 프레임워크 사용
```