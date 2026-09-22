# Commit Convention

이 저장소의 커밋 메시지는 주차별 작업과 변경 유형을 쉽게 찾을 수 있도록 작성합니다.

## 기본 형식

주차별 실습과 과제는 아래 형식을 사용합니다.

```text
[작업 범위][변경 유형] 작업 내용
```

저장소 문서는 `[docs] 작업 내용` 형식을 사용합니다. 콜론은 사용하지 않고, 작업 내용을 짧게 작성합니다.

## 작업 범위

| 범위 | 용도 |
| --- | --- |
| `week{N}-prac{N}` | 주차별 실습. 첫 번째 `N`은 주차, 두 번째 `N`은 실습 순서입니다. |
| `week{N}-hw{N}` | 주차별 과제. 첫 번째 `N`은 주차, 두 번째 `N`은 과제 순서입니다. |
| `docs` | 저장소 README와 커밋 컨벤션 등 문서 변경 |

## 변경 유형

| 유형 | 용도 |
| --- | --- |
| `feat` | 기능 또는 실습 내용 추가 |
| `chore` | 환경, 의존성, 기본 설정 변경 |
| `fix` | 오류 수정 |
| `docs` | 문서 작성 및 수정 |

## 예시

```text
[week4-prac1][chore] 프로젝트 초기 설정
[week4-prac3][feat] 첫 Flask 서버 실행
[week4-hw1][feat] 메인 소개 페이지 추가
[docs] 주차별 자료와 커밋 안내 정리
```

## 커밋 찾기

작업 범위나 변경 유형을 기준으로 `git log`에서 검색합니다.

```bash
git log --oneline --grep='week4-prac'
git log --oneline --grep='week4-hw'
git log --oneline --grep='\[docs\]'
```
