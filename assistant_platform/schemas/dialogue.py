from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class DialogueState(BaseModel):
    session_id: str
    active_skill: Optional[str] = None
    pending_action: Optional[Dict[str, Any]] = None
    slots: Dict[str, Any] = Field(default_factory=dict)
    last_user_text: Optional[str] = None
    last_assistant_text: Optional[str] = None
