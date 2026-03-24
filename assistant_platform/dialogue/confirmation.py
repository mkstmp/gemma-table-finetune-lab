from __future__ import annotations

from assistant_platform.schemas.common import ToolCall


def explicit_confirmation_prompt(call: ToolCall) -> str:
    return f"Do you want me to proceed with {call.tool_name} using {call.arguments}?"


def implicit_confirmation_text(call: ToolCall) -> str:
    return f"Okay, proceeding with {call.tool_name}."
