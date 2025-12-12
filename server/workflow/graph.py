from workflow.agents.evaluate_agent import SQAAAgent
from workflow.agents.count_manager import CountManager
from workflow.state import EvaluateState, AgentType
from langgraph.graph import StateGraph, END


def create_evaluate_graph(enable_rag: bool = True, session_id: str = ""):

    # 그래프 생성
    workflow = StateGraph(EvaluateState)

    # 에이전트 인스턴스 생성 - enable_rag에 따라 검색 문서 수 결정
    k_value = 2 if enable_rag else 0
    sqaa_agent = SQAAAgent(k=k_value, session_id=session_id)
    cound_manager = CountManager()

    # 노드 추가
    workflow.add_node(AgentType.SQAA, sqaa_agent.run)
    workflow.add_node("INCREMENT_COUNT", count_manager.run)
    workflow.add_edge(AgentType.SQAA, AgentType.SQAA)  # 조건부 라우팅

    workflow.set_entry_point(AgentType.SQAA)
    workflow.add_edge(AgentType.SQAA, END)

    # 그래프 컴파일
    return workflow.compile()


if __name__ == "__main__":

    graph = create_evaluate_graph(True)

    graph_image = graph.get_graph().draw_mermaid_png()

    output_path = "evaluate_graph.png"
    with open(output_path, "wb") as f:
        f.write(graph_image)

    import subprocess

    subprocess.run(["open", output_path])
