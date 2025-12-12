간단한 코드 구조 설명 및 실행법 작성

===================
## 코드 실행법
===================
### FastAPI 백엔드 실행(AI Talent Lab 에선 Address already in use)
uvicorn api:app --reload --port 8000

### Streamlit 앱 실행
streamlit run app.py

===================
## 파일별 설명
===================
### main.py
Streamlit 프론트엔드 — 사용자가 STT 텍스트를 입력하면 FastAPI 백엔드(/analyze)에 요청 보냄.

### api.py
FastAPI 백엔드 — STT 분석 전체 파이프라인 실행.

### requirements.txt
설치한 패키지 리스트

### .env
환경 설정(AOAI 변수 및 키)

===================
## app/
===================
### components/

#### history.py
SmartQA Assistant 재평가 이력을 조회, 수정, 삭제하는 API

#### sidebar.py
UI상에서 사이드바를 표시. "재평가", "재평가 이력" 2개의 탭으로 구성

### utils/

#### state_manager.py
세션 스테이트를 관리. 초기화, agent 실행 시 기본 값 설정 등의 역할

===================
## server/
===================
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


### routers/

#### history.py

#### workflow.py

### utils/

#### config.py

### workflow

#### graph.py

#### state.py

### workflow/agents/

#### count_manager.py

#### evaluate_agent.py



