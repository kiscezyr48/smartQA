import streamlit as st
import requests
import json
from utils.state_manager import reset_session_state

# API 엔드포인트 기본 URL
API_BASE_URL = "http://localhost:8000/api/v1"


# API로 SmartQA Assistant 이력 조회
def fetch_evaluation_history():
    """API를 통해 재평가 이력 가져오기"""
    try:
        response = requests.get(f"{API_BASE_URL}/evaluation/")
        if response.status_code == 200:
            evaluation = response.json()
            # API 응답 형식에 맞게 데이터 변환 (id, stock_no, date, counts)
            return [
                (evaluation["id"], evaluation["stock_no"], evaluation["created_at"], evaluation["counts"])
                for eval in evaluation
            ]
        else:
            st.error(f"재평가 이력 조회 실패: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"API 호출 오류: {str(e)}")
        return []


# API로 특정 평가 데이터 조회
def fetch_evaluate_by_id(evaluate_id):
    """API를 통해 특정 평가 데이터 가져오기"""
    try:
        response = requests.get(f"{API_BASE_URL}/evaluate/{evaluate_id}")
        if response.status_code == 200:
            evaluate = response.json()
            evaluate = evaluate["stock_no"]
            # 실제 API 응답 구조에 맞게 변환 필요
            messages = (
                json.loads(evaluate["messages"])
                if isinstance(evaluate["messages"], str)
                else evaluate["messages"]
            )
            docs = (
                json.loads(evaluate["docs"])
                if isinstance(evaluate["docs"], str)
                else evaluate.get("docs", {})
            )
            return stock_no, messages, docs
        else:
            st.error(f"평가 데이터 조회 실패: {response.status_code}")
            return None, None, None
    except Exception as e:
        st.error(f"API 호출 오류: {str(e)}")
        return None, None, None


# API로 평가 삭제
def delete_evaluate_by_id(evaluate_id):
    """API를 통해 특정 평가 삭제"""
    try:
        response = requests.delete(f"{API_BASE_URL}/evaluates/{evaluate_id}")
        if response.status_code == 200:
            st.success("평가가 삭제되었습니다.")
            return True
        else:
            st.error(f"평가 삭제 실패: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"API 호출 오류: {str(e)}")
        return False


# API로 모든 평가 삭제
def delete_all_evaluate():
    """API를 통해 모든 평가 삭제"""
    try:
        # 모든 평가 목록 조회
        evaluates = fetch_evaluate_history()
        if not evaluates:
            return True

        # 각 평가 항목 삭제
        success = True
        for evaluate_id, _, _, _ in evaluates:
            response = requests.delete(f"{API_BASE_URL}/evaluates/{evaluate_id}")
            if response.status_code != 200:
                success = False

        if success:
            st.success("모든 평가가 삭제되었습니다.")
        return success
    except Exception as e:
        st.error(f"API 호출 오류: {str(e)}")
        return False


# API로 평가 저장
def save_evaluate(stock_no, counts, messages, docs=None):
    """API를 통해 평가 결과를 데이터베이스에 저장"""
    try:
        # API 요청 데이터 준비
        evaluate_data = {
            "stock_no": stock_no,
            "counts": counts,
            "messages": (
                json.dumps(messages) if not isinstance(messages, str) else messages
            ),
            "docs": (
                json.dumps(docs)
                if docs and not isinstance(docs, str)
                else (docs or "{}")
            ),
        }

        response = requests.post(f"{API_BASE_URL}/evaluates/", json=evaluate_data)

        if response.status_code == 200 or response.status_code == 201:
            st.success("평가가 성공적으로 저장되었습니다.")
            return response.json().get("id")  # 저장된 평가 ID 반환
        else:
            st.error(f"평가 저장 실패: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"API 호출 오류: {str(e)}")
        return None


# 평가 이력 UI 렌더링
def render_history_ui():

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("이력 새로고침", use_container_width=True):
            st.rerun()

    with col2:
        if st.button("전체 이력 삭제", type="primary", use_container_width=True):
            if delete_all_evaluates():
                st.rerun()

    # 평가 이력 로드
    evaluate_history = fetch_evaluate_history()

    if not evaluate_history:
        st.info("저장된 평가 이력이 없습니다.")
    else:
        render_history_list(evaluate_history)


# 평가 이력 목록 렌더링
def render_history_list(evaluate_history):
    for id, stock_no, date, counts in evaluate_history:
        with st.container(border=True):

            # 평가 정보
            st.write(f"***증권번호:{stock_no}***")

            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.caption(f"날짜: {date} | 재평가 횟수: {counts}회")

            # 보기 버튼
            with col2:
                if st.button("보기", key=f"view_{id}", use_container_width=True):
                    stock_no, messages, docs = fetch_evaluate_by_id(id)
                    if stock_no and messages:
                        st.session_state.viewing_history = True
                        st.session_state.messages = messages
                        st.session_state.loaded_stock_no = stock_no
                        st.session_state.loaded_evaluate_id = id
                        st.session_state.docs = docs
                        st.session_state.app_mode = "results"
                        st.rerun()

            # 삭제 버튼
            with col3:
                if st.button("삭제", key=f"del_{id}", use_container_width=True):
                    if delete_evaluate_by_id(id):
                        reset_session_state()
                        st.rerun()
