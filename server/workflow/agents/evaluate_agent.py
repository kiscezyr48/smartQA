from workflow.agents.agent import Agent
from workflow.state import AgentType
from typing import Dict, Any


class SQAAAgent(Agent):

    def __init__(self, k: int = 2, session_id: str = None):
        super().__init__(
            system_prompt   = "당신은 STT 데이터와 표준 녹취 스크립트를 비교하여 불완전판매 항목을 검출해내는 SamrtQA 전문가입니다.",
            role            = AgentType.SQAA,
            k               = k,
            session_id      = session_id,
        )

    def _create_prompt(self, state: Dict[str, Any]) -> str:
        if state["current_count"] == 1:
            return self._create_first_count_prompt(state)
        else:
            return self._create_rebuttal_prompt(state)

    def _create_first_count_prompt(self, state: Dict[str, Any]) -> str:
        return f"""
            당신은 STT 데이터와 표준 녹취 스크립트를 비교하여 불완전판매 항목 SmartQA 전문가입니다.
            청약 건인 증권번호 '{state['stock_no']}'를 재평가하겠습니다.
                {state.get("context", "")}
            누락, 과장, 허위, 다보장식 Sales를 탐지해야 합니다.
            검출된 항목에 대해 벌점과 결과(주의, 경고, 중요위반보완 등)를 도출하세요.
            해당 항목이 검출된 이유에 대해 D/L comment를 작성하세요.
            """

    def _create_rebuttal_prompt(self, state: Dict[str, Any]) -> str:

        return f"""
            당신은 STT 데이터와 표준 녹취 스크립트를 비교하여 불완전판매 항목 SmartQA 전문가입니다.
            청약 건인 증권번호 '{state['stock_no']}'를 재평가하겠습니다.
                {state.get("context", "")}
            재평가한 건에 대해 다시 재평가를 진행하세요.
            검출된 항목에 대해 벌점과 결과(주의, 경고, 중요위반보완 등)를 도출하세요.
            해당 항목이 검출된 이유에 대해 D/L comment를 작성하세요.
            QA검수의견을 참고하여 오탐, 미탐 건을 재평가하고 결과와 코멘트를 작성하세요.
            """
