import streamlit as st

# 세션 스테이트 초기화
def init_session_state():
    if "app_mode" not in st.session_state:
        reset_session_state()

# 세션 기본값 설정
def reset_session_state():
    st.session_state.app_mode           = False # app mode 여부
    st.session_state.count              = 0     # 재평가 횟수 
    st.session_state.viewing_history    = False # 재평가 이력 보기 여부
    st.session_state.loaded_evaluate_id = None  # evaluation id 로딩 여부
    st.session_state.docs               = {}    # RAG 검색 시 URL 저장

# agent 실행 시 세션 값 설정
def set_evaluate_to_state(stock_no, messages, evaluate_id, docs):
    st.session_state.app_mode            = True
    st.session_state.messages            = messages
    st.session_state.viewing_history     = True
    st.session_state.stock_no            = stock_no
    st.session_state.loaded_cevaluate_id = evaluate_id
    st.session_state.docs                = docs
