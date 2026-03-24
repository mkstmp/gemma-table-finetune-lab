from __future__ import annotations

from typing import Any, Dict, List

from assistant_platform.schemas.common import ConversationTurn


class SearchSynthesisAgent:
    async def synthesize(self, query: str, results: List[Dict[str, Any]], turn: ConversationTurn) -> str:
        if not results:
            return "I couldn't find relevant results."
        top = results[0]
        return f"{top.get('title')}: {top.get('snippet')}"
