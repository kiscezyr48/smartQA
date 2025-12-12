import streamlit as st

from typing import Dict, Any
from components.history import render_history_ui


def render_input_form():
    with st.form("evaluate_form", border=False):
        # 증권번호 입력
        st.text_input(
            label = "증권번호를 입력하세요:",
            value = "1234567",
            key   = "stock_no",
        )

        max_counts = st.slider("재평가 회차", min_value=1, max_value=5, value=1)
        st.session_state.max_counts = max_counts
        st.form_submit_button(
            "재평가 시작",
            on_click=lambda: st.session_state.update({"app_mode": "evaluate"}),
        )
        # RAG 기능 활성화 옵션
        st.checkbox(
            "RAG 활성화",
            value = True,
            help  = "QA검수의견을 참고하여 재평가에 활용합니다.",
            key   = "ui_enable_rag",
        )


def render_sidebar() -> Dict[str, Any]:
    with st.sidebar:

        tab1, tab2 = st.tabs(["재평가", "재평가 이력"])

        with tab1:
            render_input_form()

        with tab2:
            render_history_ui()
