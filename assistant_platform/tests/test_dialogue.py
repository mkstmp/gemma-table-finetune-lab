import pytest

from assistant_platform.agents.dialogue import DialogueAgent
from assistant_platform.schemas.common import ConversationTurn, RoutedAction, SlotStatus


@pytest.mark.asyncio
async def test_dialogue_missing_slot_prompt() -> None:
    agent = DialogueAgent()
    routed = RoutedAction(
        skill_name="weather",
        confidence=0.9,
        requires_tool=True,
        tool_candidates=["get_weather"],
        slot_status=SlotStatus(required_slots=["location"], collected_slots={}, missing_slots=["location"]),
    )
    prompt = await agent.next_prompt(routed, ConversationTurn(session_id="s1", user_text="How's weather"))
    assert "location" in prompt.lower()
