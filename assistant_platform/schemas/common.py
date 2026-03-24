from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

RiskLevel = Literal["low", "medium", "high"]
ConfirmationMode = Literal["none", "implicit", "explicit"]


class ToolSpec(BaseModel):
    name: str
    description: str
    risk_level: RiskLevel = "low"
    idempotent: bool = True
    confirmation_mode: ConfirmationMode = "none"
    timeout_seconds: int = 10
    max_retries: int = 1
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]


class ToolCall(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    call_id: str


class ToolResult(BaseModel):
    tool_name: str
    call_id: str
    ok: bool
    data: Dict[str, Any] = Field(default_factory=dict)
    error_code: Optional[str] = None
    error_message: Optional[str] = None


class SlotStatus(BaseModel):
    required_slots: List[str] = Field(default_factory=list)
    collected_slots: Dict[str, Any] = Field(default_factory=dict)
    missing_slots: List[str] = Field(default_factory=list)


class RoutedAction(BaseModel):
    skill_name: str
    confidence: float
    requires_tool: bool
    tool_candidates: List[str] = Field(default_factory=list)
    slot_status: SlotStatus
    answer_directly: bool = False


class ConversationTurn(BaseModel):
    session_id: str
    user_text: str
    locale: str = "en-US"
    timezone: str = "America/Los_Angeles"
    context: Dict[str, Any] = Field(default_factory=dict)


class ChatRequest(BaseModel):
    session_id: str
    user_id: str
    text: str
    locale: str = "en-US"
    timezone: str = "America/Los_Angeles"
    context: Dict[str, Any] = Field(default_factory=dict)


class ChatResponse(BaseModel):
    assistant_text: str
    dialogue_state: Dict[str, Any] = Field(default_factory=dict)
    tool_trace: List[Dict[str, Any]] = Field(default_factory=list)
