from __future__ import annotations

from assistant_platform.dialogue.slot_filling import missing_slot_question
from assistant_platform.schemas.common import ConversationTurn, RoutedAction


class DialogueAgent:
    async def next_prompt(self, routed: RoutedAction, turn: ConversationTurn) -> str:
        if routed.slot_status.missing_slots:
            return missing_slot_question(routed)
        return "Could you clarify your request?"
