from __future__ import annotations

from typing import Any, Dict, Optional

from assistant_platform.schemas.common import ToolSpec
from assistant_platform.tools.base import RegisteredTool, model_json_schema


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, RegisteredTool] = {}

    def register(
        self,
        *,
        name: str,
        description: str,
        input_model: type[Any],
        output_model: type[Any],
        risk_level: str = "low",
        idempotent: bool = True,
        confirmation_mode: str = "none",
        timeout_seconds: int = 10,
        max_retries: int = 1,
    ):
        def _decorator(fn):
            spec = ToolSpec(
                name=name,
                description=description,
                risk_level=risk_level,  # type: ignore[arg-type]
                idempotent=idempotent,
                confirmation_mode=confirmation_mode,  # type: ignore[arg-type]
                timeout_seconds=timeout_seconds,
                max_retries=max_retries,
                input_schema=model_json_schema(input_model),
                output_schema=model_json_schema(output_model),
            )
            self._tools[name] = RegisteredTool(
                spec=spec,
                fn=fn,
                input_model=input_model,
                output_model=output_model,
            )
            return fn

        return _decorator

    def get(self, name: str) -> Optional[RegisteredTool]:
        return self._tools.get(name)

    def must_get(self, name: str) -> RegisteredTool:
        tool = self.get(name)
        if tool is None:
            raise KeyError(f"Unknown tool: {name}")
        return tool

    def specs(self) -> Dict[str, ToolSpec]:
        return {k: v.spec for k, v in self._tools.items()}


registry = ToolRegistry()
