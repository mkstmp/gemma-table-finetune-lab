import pytest

from assistant_platform.agents.tool_executor import ToolExecutionAgent
from assistant_platform.schemas.common import ToolCall

# Register tools
import assistant_platform.tools  # noqa: F401


@pytest.mark.asyncio
async def test_currency_convert() -> None:
    executor = ToolExecutionAgent()
    call = ToolCall(
        tool_name="currency_convert",
        call_id="c1",
        arguments={"amount": 100, "source_currency": "USD", "target_currency": "INR", "date_iso": None},
    )
    result = await executor.execute(call)
    assert result.ok
    assert result.data["converted_amount"] > 0


@pytest.mark.asyncio
async def test_unit_convert_validation_error() -> None:
    executor = ToolExecutionAgent()
    call = ToolCall(tool_name="unit_convert", call_id="c2", arguments={"value": 5, "from_unit": "km", "to_unit": "kg"})
    result = await executor.execute(call)
    assert not result.ok
    assert result.error_code in {"VALIDATION_ERROR", "UPSTREAM_UNAVAILABLE"}


@pytest.mark.asyncio
async def test_timer_set() -> None:
    executor = ToolExecutionAgent()
    call = ToolCall(tool_name="set_timer", call_id="c3", arguments={"duration_seconds": 60, "label": "tea"})
    result = await executor.execute(call)
    assert result.ok
    assert result.data["timer_id"]
