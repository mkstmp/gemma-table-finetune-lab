from __future__ import annotations

import asyncio
from typing import Any

from pydantic import ValidationError

from assistant_platform.schemas.common import ToolCall, ToolResult
from assistant_platform.tools.base import ToolExecutionError
from assistant_platform.tools.registry import registry


ERROR_MAP = {
    KeyError: "NOT_FOUND",
    ValidationError: "VALIDATION_ERROR",
    PermissionError: "PERMISSION_DENIED",
    TimeoutError: "UPSTREAM_TIMEOUT",
}


class ToolExecutionAgent:
    async def execute(self, call: ToolCall) -> ToolResult:
        try:
            tool = registry.must_get(call.tool_name)
            parsed_input = tool.input_model(**call.arguments)

            output = await asyncio.wait_for(tool.fn(parsed_input), timeout=tool.spec.timeout_seconds)
            if hasattr(output, "model_dump"):
                data = output.model_dump()
            elif isinstance(output, dict):
                data = output
            else:
                data = {"value": output}
            return ToolResult(tool_name=call.tool_name, call_id=call.call_id, ok=True, data=data)
        except Exception as exc:  # noqa: BLE001
            if isinstance(exc, ToolExecutionError):
                code = exc.code
                message = exc.message
            else:
                code = ERROR_MAP.get(type(exc), "UPSTREAM_UNAVAILABLE")
                message = str(exc)
            return ToolResult(
                tool_name=call.tool_name,
                call_id=call.call_id,
                ok=False,
                error_code=code,
                error_message=message,
            )
