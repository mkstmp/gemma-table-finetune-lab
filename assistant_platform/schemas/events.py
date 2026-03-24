from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel


class ToolTraceEvent(BaseModel):
    tool_name: str
    call_id: str
    ok: bool
    error_code: Optional[str] = None
    metadata: Dict[str, Any] = {}
