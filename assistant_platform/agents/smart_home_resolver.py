from __future__ import annotations

from typing import Any, Dict, List


class SmartHomeResolutionAgent:
    async def resolve(self, user_text: str, device_candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not device_candidates:
            return {"status": "not_found"}
        if len(device_candidates) == 1:
            return {"status": "resolved", "device": device_candidates[0], "action_text": user_text}
        return {"status": "ambiguous", "candidates": device_candidates}
