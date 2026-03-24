from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from assistant_platform.routing.entity_extractors import EntityExtractor
from assistant_platform.routing.matcher import match_skill
from assistant_platform.routing.skill_loader import load_skills
from assistant_platform.schemas.common import ConversationTurn, RoutedAction, SlotStatus


class RouterAgent:
    def __init__(self, skills_dir: Path) -> None:
        self.skills = load_skills(skills_dir)
        self.extractor = EntityExtractor()

    async def route(self, turn: ConversationTurn) -> RoutedAction:
        entities = self.extractor.extract(turn.user_text)
        skill, confidence = match_skill(turn.user_text, self.skills, entities)

        required = self._required_slots(skill, entities)
        missing = [slot for slot in required if slot not in entities or entities.get(slot) in (None, "")]

        tool_candidates: List[str] = skill.get("tools", {}).get("primary", [])
        answer_directly = bool(skill.get("answer_directly_when")) and not tool_candidates

        return RoutedAction(
            skill_name=skill["name"],
            confidence=confidence,
            requires_tool=not answer_directly,
            tool_candidates=tool_candidates,
            slot_status=SlotStatus(required_slots=required, collected_slots=entities, missing_slots=missing),
            answer_directly=answer_directly,
        )

    def _required_slots(self, skill: Dict[str, Any], entities: Dict[str, Any]) -> List[str]:
        name = skill.get("name")
        if name == "weather":
            return ["location"]
        if name == "utilities" and entities.get("currency_pair"):
            return ["amount", "source_currency", "target_currency"]
        if name == "reminders_timers_alarms" and "remind me" in entities.get("expression", ""):
            return ["reminder_text", "datetime"]
        return skill.get("required_entities", []) or []
