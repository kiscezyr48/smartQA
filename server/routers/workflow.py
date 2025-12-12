from typing import Any
import uuid
import json
import asyncio
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langfuse.callback import CallbackHandler


from workflow.state import AgentType, EvaluateState
from workflow.graph import create_evaluate_graph


# API 경로를 /api/v1로 변경
router = APIRouter(
    prefix="/api/v1/workflow",
    tags=["workflow"],
    responses={404: {"description": "Not found"}},
)


class WorkflowRequest(BaseModel):
    stock_no: str
    max_counts: int = 3
    enable_rag: bool = True


class WorkflowResponse(BaseModel):
    status: str = "success"
    result: Any = None


async def evaluate_generator(evaluate_graph, initial_state, langfuse_handler):
    # 그래프에서 청크 스트리밍
    for chunk in evaluate_graph.stream(
        initial_state,
        config={"callbacks": [langfuse_handler]},
        subgraphs=True,
        stream_mode="updates",
    ):
        if not chunk:
            continue

        node = chunk[0] if len(chunk) > 0 else None
        if not node or node == ():
            continue

        node_name = node[0]
        role = node_name.split(":")[0]
        subgraph = chunk[1]
        subgraph_node = subgraph.get("update_state", None)

        if subgraph_node:
            response        = subgraph_node.get("response", None)
            evaluate_state  = subgraph_node.get("evaluate_state", None)
            messages        = evaluate_state.get("messages", [])
            count           = evaluate_state.get("current_count")
            max_counts      = evaluate_state.get("max_counts")
            docs            = evaluate_state.get("docs", {})
            stock_no        = evaluate_state.get("stock_no")

            state = {
                "role"          : role,
                "response"      : response,
                "stock_no"      : stock_no,
                "messages"      : messages,
                "current_count" : count,
                "max_counts"    : max_counts,
                "docs"          : docs,
            }

            event_data = {"type": "update", "data": state}
            yield f"data: {json.dumps(event_data, ensure_ascii=False)}\n\n"
            print(event_data)

            await asyncio.sleep(0.01)

    # 디베이트 종료 메시지
    yield f"data: {json.dumps({'type': 'end', 'data': {}}, ensure_ascii=False)}\n\n"


# 엔드포인트 경로 수정 (/evaluate/stream -> 유지)
@router.post("/evaluate/stream")
async def stream_evaluate_workflow(request: WorkflowRequest):
    stock_no    = request.stock_no
    max_counts  = request.max_counts
    enable_rag  = request.enable_rag

    session_id      = str(uuid.uuid4())
    evaluate_graph  = create_evaluate_graph(enable_rag, session_id)

    initial_state: EvaluateState = {
        "stock_no"      : stock_no,
        "messages"      : [],
        "current_count" : 1,
        "max_counts"    : max_counts,
        "prev_node"     : "START",  # 이전 노드 START로 설정
        "docs"          : {},       # RAG 결과 저장
    }

    langfuse_handler = CallbackHandler(session_id=session_id)

    # 스트리밍 응답 반환
    return StreamingResponse(
        evaluate_generator(evaluate_graph, initial_state, langfuse_handler),
        media_type="text/event-stream",
    )
