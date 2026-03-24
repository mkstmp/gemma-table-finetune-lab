from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict

from assistant_platform.schemas.common import ToolSpec

ToolFn = Callable[[Any], Awaitable[Any]]


@dataclass(slots=True)
class RegisteredTool:
    spec: ToolSpec
    fn: ToolFn
    input_model: type[Any]
    output_model: type[Any]


class ToolExecutionError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


class UpstreamTimeoutError(ToolExecutionError):
    def __init__(self, message: str = "Upstream timed out"):
        super().__init__("UPSTREAM_TIMEOUT", message)


class UpstreamUnavailableError(ToolExecutionError):
    def __init__(self, message: str = "Upstream unavailable"):
        super().__init__("UPSTREAM_UNAVAILABLE", message)


def model_json_schema(model: type[Any]) -> Dict[str, Any]:
    if hasattr(model, "model_json_schema"):
        return model.model_json_schema()  # type: ignore[no-any-return]
    return {}
