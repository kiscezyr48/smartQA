import json
import requests
import streamlit as st
from components.history import save_evaluate
from components.sidebar import render_sidebar
from utils.state_manager import init_session_state, reset_session_state

API_BASE_URL = "http://localhost:8000/api/v1"

# 페이지 설정
st.set_page_config(page_title   = "SmartQA Assistant"
                 , page_icon    = "📝"
                 , layout       = "wide"
                 )

class AgentType:
    SQAA = "SQAA_AGENT" # SamrtQA Assistant


def process_event_data(event_data):

    # 이벤트 종료
    if event_data.get("type") == "end":
        return True

    # 새로운 메세지
    if event_data.get("type") == "update":
        # state 추출
        data = event_data.get("data", {})

        role            = data.get("role")
        response        = data["response"]
        stock_no        = data["stock_no"]      # 증권번호
        messages        = data["messages"]      # 메시지내용
        current_count   = data["current_count"] # 현재 평가 회차
        max_counts      = data["max_counts"]    # 최대 재평가 횟수
        docs            = data.get("docs", {})

        # Agent 회차
        # SQAA: 재평가 횟수
        if role == AgentType.SQAA:
            st.subheader(f"{current_count}/{max_counts} 회")

        message = response

        # Agent 각각 아바타 설정
        if role == AgentType.SQAA:
            avatar = "🧑🏻‍💻"

        with st.chat_message(role, avatar=avatar):
            st.markdown(message)

    return False


def process_streaming_response(response):
    for chunk in response.iter_lines():
        if not chunk:
            continue

        # 'data: ' 접두사 제거
        line = chunk.decode("utf-8")

        # line의 형태는 'data: {"type": "update", "data": {}}'
        if not line.startswith("data: "):
            continue

        data_str = line[6:]  # 'data: ' 부분 제거

        try:
            # JSON 데이터 파싱
            event_data = json.loads(data_str)

            # 이벤트 데이터 처리
            is_complete = process_event_data(event_data)

            if is_complete:
                break

        except json.JSONDecodeError as e:
            st.error(f"JSON 파싱 오류: {e}")


def start_evaluate():

    stock_no    = st.session_state.ui_stock_no
    max_counts  = st.session_state.max_counts

    enabled_rag = st.session_state.get("ui_enable_rag", False)

    with st.spinner("재평가가 진행 중입니다... 완료까지 잠시 기다려주세요."):
        # API 요청 데이터
        data = {
            "stock_no"  : stock_no,     # 증권번호
            "max_counts": max_counts,   # 최대 재평가 횟수
            "enable_rag": enabled_rag,  # rag 이용
        }

        try:
            # 스트리밍 API 호출
            response = requests.post(
                f"{API_BASE_URL}/workflow/evaluate/stream",
                json=data,
                stream=True,
                headers={"Content-Type": "application/json"},
            )

            # stream=True로 설정하여 스트리밍 응답 처리
            # iter_lines() 또는 Iter_content()로 청크단위로 Read

            if response.status_code != 200:
                st.error(f"API 오류: {response.status_code} - {response.text}")
                return

            process_streaming_response(response)

        except requests.RequestException as e:
            st.error(f"API 요청 오류: {str(e)}")


# 참고 자료 표시
"""
실제 QA센터에서 평가를 끝내고 송부해주시는 QA검수의견을 참고합니다.
D/L의 오탐, 미탐 건에 대하여 QA 강사님들께서 수기로 평가를 수정한 뒤, 매일 15건씩 선정하여 전달해줍니다.
D/L이 반복적으로 오탐, 미탐을 하는 건은 QA검수의견에 data가 많고, 이를 참고하여 잘못된 평가를 스스로 정정할 수 있습니다.
"""
def render_source_materials():

    with st.expander("참고한 QA검수의견 보기"):
        st.subheader("참고한 QA검수의견")
        for i, doc in enumerate(st.session_state.docs.get(AgentType.SQAA, [])[:3]):
            st.markdown(f"**문서 {i+1}**")
            st.text(doc[:300] + "..." if len(doc) > 300 else doc)
            st.divider()


def display_evaluate_results():

    if st.session_state.viewing_history:
        st.info("📚 재평가 히스토리 확인 중..")
        stcok_no = st.session_state.loaded_stock_no
    else:
        stock_no = st.session_state.ui_stock_no

    # 증권번호 표시
    st.header(f"증권번호: {stock_no}")

    for message in st.session_state.messages:

        role = message["role"]
        if role not in [
            AgentType.SQAA,
        ]:
            continue

        if message["role"] == AgentType.SQAA:
            avatar = "🧑🏻‍💻"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])


    # 참고 자료 표시
    if st.session_state.docs:
        render_source_materials()

    if st.button("다른 재평가 시작"):
        reset_session_state()
        st.session_state.app_mode = "input"
        st.rerun()


def render_ui():

    # 제목 및 소개
    st.title("📝 SmartQA Assistant")
    st.markdown(
        """
        ### 프로젝트 소개
        보험 청약 콜에 대한 STT 데이터와 표준 녹취 스크립트를 비교하여 상품의 완전판매 여부를 평가하는 시스템이 있습니다.
        이 서비스는 보험의 완전판매 여부가 BERT MODEL을 통해 스크리닝 된 이후, 1차 평가가 끝난 청약 콜에 활용합니다.
        D/L이 오탐, 미탐 등 분류를 정확하게 하지 못했을 경우, 해당 증권번호를 입력받아서 상품을 찾아 표준 녹취 스크립트와 비교합니다.
        D/L은 batch로 대용량 청약 콜 STT데이터를 처리하지만, 이 서비스는 증권번호 하나에 대해서만 재분류 역할을 합니다.
        """
    )

    render_sidebar()

    current_mode = st.session_state.app_mode

    if current_mode == "evaluate":
        start_evaluate()
    elif current_mode == "results":
        display_evaluate_results()


if __name__ == "__main__":
    # 세션 상태 초기화
    init_session_state()

    render_ui()
