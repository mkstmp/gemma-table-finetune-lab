from __future__ import annotations

from pydantic import BaseModel

from assistant_platform.schemas.common import ConversationTurn, ToolCall

EXPLICIT_TOOLS = {
    "send_sms",
    "send_email",
    "delete_calendar_event",
    "store_memory",
    "update_user_profile",
}
IMPLICIT_TOOLS = {"create_calendar_event", "update_calendar_event", "make_call"}


class PolicyDecision(BaseModel):
    allowed: bool
    requires_confirmation: bool = False
    reason: str | None = None
    confirmation_mode: str = "none"


class PolicyAgent:
    async def evaluate(self, call: ToolCall, turn: ConversationTurn) -> PolicyDecision:
        if call.tool_name in EXPLICIT_TOOLS:
            return PolicyDecision(allowed=True, requires_confirmation=True, confirmation_mode="explicit")
        if call.tool_name in IMPLICIT_TOOLS:
            return PolicyDecision(allowed=True, requires_confirmation=True, confirmation_mode="implicit")

        if call.tool_name == "control_device":
            action = str(call.arguments.get("action", "")).lower()
            if action in {"unlock", "open_garage"}:
                return PolicyDecision(allowed=True, requires_confirmation=True, confirmation_mode="explicit")
            if action in {"set_thermostat"}:
                return PolicyDecision(allowed=True, requires_confirmation=True, confirmation_mode="implicit")

        return PolicyDecision(allowed=True, requires_confirmation=False, confirmation_mode="none")
