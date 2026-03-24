from pathlib import Path

import pytest

from assistant_platform.agents.router import RouterAgent
from assistant_platform.schemas.common import ConversationTurn


@pytest.mark.asyncio
async def test_router_currency_convert() -> None:
    router = RouterAgent(skills_dir=Path(__file__).resolve().parents[1] / "skills")
    turn = ConversationTurn(session_id="s1", user_text="167 inr to usd")
    routed = await router.route(turn)
    assert routed.skill_name == "utilities"
    assert "currency_convert" in routed.tool_candidates
    assert not routed.slot_status.missing_slots


@pytest.mark.asyncio
async def test_router_weather() -> None:
    router = RouterAgent(skills_dir=Path(__file__).resolve().parents[1] / "skills")
    turn = ConversationTurn(session_id="s2", user_text="Weather in Sunnyvale tomorrow")
    routed = await router.route(turn)
    assert routed.skill_name == "weather"


@pytest.mark.asyncio
async def test_router_reminder() -> None:
    router = RouterAgent(skills_dir=Path(__file__).resolve().parents[1] / "skills")
    turn = ConversationTurn(session_id="s3", user_text="Set a timer for 10 minutes")
    routed = await router.route(turn)
    assert routed.skill_name == "reminders_timers_alarms"
