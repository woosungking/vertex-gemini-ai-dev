# Vertex AI와 Gemini로 시작하는 생성형 AI 실전개발

"Vertex AI와 Gemini로 시작하는 생성형 AI 실전개발" 책 실습 프로젝트입니다.

## 프로젝트 구조

```
vertex-gemini-ai-dev/
├── ch01/          # 1장 실습
├── ch02/          # 2장 실습
├── ch03/          # 3장 실습
├── notebooks/     # Jupyter 노트북
├── .env.example   # 환경변수 예시
└── requirements.txt
```

## 환경 설정

### 1. Python 가상환경 생성

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경변수 설정

```bash
cp .env.example .env
# .env 파일에 GCP 프로젝트 ID 및 인증 정보 입력
```

### 4. Google Cloud 인증

```bash
gcloud auth application-default login
```

## 참고

- [Vertex AI 공식 문서](https://cloud.google.com/vertex-ai/docs)
- [Gemini API 문서](https://ai.google.dev/docs)
