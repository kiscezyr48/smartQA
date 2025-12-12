간단한 코드 구조 설명 및 실행법 작성

## 코드 실행법
### FastAPI 백엔드 실행(AI Talent Lab 에선 Address already in use)
uvicorn api:app --reload --port 8000

### Streamlit 앱 실행
streamlit run main.py

## 파일별 설명
### main.py
Streamlit 프론트엔드 — 사용자가 STT 텍스트를 입력하면 FastAPI 백엔드(/analyze)에 요청 보냄.

### api.py
FastAPI 백엔드 — STT 분석 전체 파이프라인 실행.

### requirements.txt
설치한 패키지 리스트

### .env
환경 설정(AOAI 변수 및 키)

## app/
### components/

#### history.py
SmartQA Assistant 재평가 이력을 조회, 수정, 삭제하는 API

#### sidebar.py
UI상에서 사이드바를 표시. "재평가", "재평가 이력" 2개의 탭으로 구성

### utils/

#### state_manager.py
세션 스테이트를 관리. 초기화, agent 실행 시 기본 값 설정 등의 역할

## server/
### db/

#### database.py
재평가 이력을 테이블에 쌓는 등 CRUD를 하기 위해 SQLite 엔진을 생성하고 DB를 관리하는 역할

#### models.py
재평가 모델의 기본 클래스 작성 

#### schemas.py
DTO 클래스를 정의하고, 기본 생성자 작성

### retrieval/

#### search_service.pyA
AI의 논리력 보강을 위한 RAG 검색 서비스. prompt를 작성하여 agent가 외부 검색을 실행

#### vector_store.py
검색어 개선, 문서를 검색해서 벡터 스토어 생성

### routers/

#### history.py
재평가 이력에 대한 히스토리 조회. 평가 목록 조회, 생성, 조회, 삭제 기능

#### workflow.py
API 경로를 세팅하고, 모델에 요청과 응답을 전달. 스트리밍 서비스에 대한 정의, 엔드포인트 및 응답 반환 등을 세팅

### utils/

#### config.py
.env 파일에서 환경 변수를 로드하고, Azure OpenAI 설정값 등 주요 환경 세팅

### workflow/

#### graph.py
agent 작동 흐름을 그래프로 컴파일하고 png 파일로 떨어뜨리는 역할

#### state.py
LangGraph 상태를 정의

### workflow/agents/

#### count_manager.py
재평가 회차를 나타내는 클래스를 관리

#### evaluate_agent.py
SmartQA Assistant 역할을 수행하는 Agent. 시스템 프롬프트 등으로 구성
