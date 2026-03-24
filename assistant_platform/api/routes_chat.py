from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter

from assistant_platform.agents.orchestrator import OrchestratorAgent
from assistant_platform.schemas.common import ChatRequest, ChatResponse, ConversationTurn

router = APIRouter(prefix="/chat", tags=["chat"])

orchestrator = OrchestratorAgent(skills_dir=Path(__file__).resolve().parents[1] / "skills")


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    turn = ConversationTurn(
        session_id=request.session_id,
        user_text=request.text,
        locale=request.locale,
        timezone=request.timezone,
        context={"user_id": request.user_id, **request.context},
    )
    result = await orchestrator.handle_turn(turn)
    return ChatResponse(**result)
