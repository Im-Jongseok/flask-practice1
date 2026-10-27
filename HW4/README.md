# HW4 Todo API 확장 준비

기존 Todo REST API에 설명(`note`)과 완료 여부 필터(`?done=`)를 추가하는 과제입니다.
마감은 **2026년 10월 29일(목) 23:59**이며, HW1 때 제출한 저장소의 `HW4/`에 작성합니다.
기준은 CE-WebSystem-L7-3 교안 79~86쪽(PDF 21~28쪽)입니다.

## 현재 준비 상태

- `todo_app`의 `app.py`, `templates/`, `static/`을 복사했습니다.
- HW4 복사본에서 API 클래스 들여쓰기를 바로잡았습니다.
- 루트 `requirements.txt`에 `Flask-RESTX==1.3.2`를 추가했습니다.
- 임시 복사본에서 화면·문서, 여섯 API 메서드, 기존 CRUD와 404 JSON을 확인했습니다.
- `note`, 필터링, `test_api.py`, 캡처는 아직 작성하지 않았습니다.
- 기존 `todo_app`, HW1~HW3, 데이터베이스는 유지합니다.

## 과제 요구사항

| 항목 | 완료 기준 |
| --- | --- |
| 설명 | `note = db.Column(db.String(500), default="")`, 입출력 모델과 POST·PATCH에 반영. 생략 시 빈 문자열 |
| 목록 | `?done=true`는 완료만, `?done=false`는 미완료만, 조건이 없으면 전체 반환 |
| 문서 | `/api/docs`에 여섯 API 메서드와 `done` 입력칸 표시 |
| 테스트 | `HW4/test_api.py`에 5개 이상, HW4에서 `python -m unittest -v`가 OK |
| 캡처 | `docs.png`, `post.png`, `notfound.png`를 README에 표시 |
| 기록 | HW4 폴더를 변경한 커밋 3개 이상 |
| 제출 | `app.py`, HTML 템플릿, `static/style.css`, 테스트, README, 캡처 포함. `instance/`, 가상환경 제외 |

`note`를 POST에서 받도록 생성자도 `note=""` 인자를 지원해야 합니다.
PATCH에서는 보낸 필드만 변경해 기존 `text`, `note`, `done`을 유지합니다.
PUT은 기존 전체 수정 기능을 유지하며, 추가한 `note`도 처리합니다.

## 실행 방법

저장소 루트에서 의존성을 설치합니다.

```bash
source venv/bin/activate
pip install -r requirements.txt
cd HW4
flask --app app --debug run --port 5003
```

- 화면: http://127.0.0.1:5003/
- API 문서: http://127.0.0.1:5003/api/docs
- 명세: http://127.0.0.1:5003/api/swagger.json

기존 개발 서버와 구분하기 위해 5003 포트를 사용합니다.
교안처럼 기본 5000 포트를 쓰려면 해당 포트를 비우고 `flask --debug run`으로 실행합니다.
`HW4/instance/todos.db`는 실행할 때 자동 생성되며 Git에서 제외됩니다.

## 커밋별 작업 계획

현재 준비 작업은 아직 커밋하지 않았습니다. 각 단계가 동작하는 것을 확인한 뒤 커밋합니다.

| 순서 | 작업 | 검증 |
| --- | --- | --- |
| 1 | 기본 앱 복사, API 메서드 배치 수정, 의존성·준비 문서 | 화면·문서 열림, 기존 CRUD와 404 JSON |
| 2 | `note` 모델·생성자·입출력 모델·POST·PATCH·PUT 구현 | note 저장·조회·수정, 생략 시 `""`, done만 PATCH하면 note 유지 |
| 3 | `?done=` 필터링과 Swagger 매개변수 추가 | true·false·조건 없음의 결과 구분 |
| 4 | 격리된 DB를 사용하는 `test_api.py` 작성 | 5개 이상 OK, 원본 DB 유지 |
| 5 | 실제 Swagger 캡처 3장과 최종 README | GitHub에서 이미지 표시, DB·가상환경 제외, HW4 커밋 3개 이상 |

최종 README는 준비 상태와 계획 대신 추가 기능, 실행 방법, 실제 캡처를 간결하게 정리합니다.

## 구현 시 확인할 점

- 조건이 없을 때는 필터를 적용하지 않습니다. `if done is not None:`을 확인합니다.
- 기존 DB는 복사하지 않았습니다. `note`를 추가한 후 빈 HW4 DB가 필요하면 HW4의 개발 DB만 백업 후 재생성합니다.
- 교안 73쪽 예제는 앱을 import한 뒤 DB 주소를 바꿉니다. Flask-SQLAlchemy 3.1.1에서는 초기화 이후 설정 변경이 기존 엔진에 반영되지 않으므로 그대로 `drop_all()`을 실행하지 않습니다.
- 테스트는 임시 폴더의 앱·DB를 사용하거나 SQLAlchemy 초기화 전에 테스트 DB를 지정합니다. 실제 연결 경로를 확인한 뒤 테이블을 초기화합니다.
- 교안의 최소 테스트 5개는 목록·생성·없는 ID·PATCH·삭제입니다. HW4에서는 note 기본값·보존·수정과 true/false/조건 없음의 필터 결과도 검증합니다.
- 캡처는 ① 전체 메서드가 보이는 문서 ② note가 포함된 201 응답 ③ 없는 ID의 404와 JSON 메시지를 담습니다.
