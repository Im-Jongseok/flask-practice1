# HW1 나를 소개하는 미니 사이트

이름과 학번, 취미를 소개하는 Flask 기반 미니 사이트입니다.

- 이름: 이종석
- 학번: 21011615

## 라우트

| 메서드 | 경로 | 설명 | 템플릿 |
| --- | --- | --- | --- |
| `GET` | `/` | 이름과 학번 표시 | `home.html` |
| `GET` | `/profile` | 취미 목록 표시 | `profile.html` |
| `GET` | `/greet/<name>` | 입력한 이름으로 인사 | `greet.html` |

## 실행 방법

### 1. 저장소 복제

```bash
git clone https://github.com/Im-Jongseok/flask-practice1.git
cd flask-practice1
```

### 2. 가상환경 생성 및 활성화

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows PowerShell에서는 다음 명령을 사용합니다.

```powershell
venv\Scripts\Activate.ps1
```

### 3. 의존성 설치

`requirements.txt`는 저장소 루트에 있으므로 루트 디렉터리에서 설치합니다.

```bash
pip install -r requirements.txt
```

### 4. HW1 실행

```bash
cd HW1
flask --app app run
```

실행 후 브라우저에서 `http://127.0.0.1:5000/`에 접속합니다.

## 실행 화면

### 메인 페이지

![메인 페이지](screenshots/home.png)

### 취미 페이지

![취미 페이지](screenshots/profile.png)

### 인사 페이지

![인사 페이지](screenshots/greet.png)
