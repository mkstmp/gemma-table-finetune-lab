from __future__ import annotations

from typing import Any, Dict

from assistant_platform.schemas.common import ConversationTurn


class PersonalMemoryAgent:
    async def propose_memory_write(self, turn: ConversationTurn) -> Dict[str, Any]:
        text = turn.user_text.lower()
        if "remember" not in text:
            return {"action": "noop"}
        payload = turn.user_text.split("remember", 1)[-1].strip()
        return {"action": "store", "key": "user_note", "value": payload}
