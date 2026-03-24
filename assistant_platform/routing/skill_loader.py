from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import yaml

REQUIRED_KEYS = {
    "name",
    "version",
    "description",
    "priority",
    "intent_category",
    "detection",
    "tools",
    "confirmation",
}


class SkillValidationError(ValueError):
    pass


def validate_skill(data: Dict[str, Any], source: str = "unknown") -> None:
    missing = REQUIRED_KEYS - set(data.keys())
    if missing:
        raise SkillValidationError(f"{source}: missing required keys: {sorted(missing)}")
    if "primary" not in data.get("tools", {}):
        raise SkillValidationError(f"{source}: tools.primary is required")
    if "lexical_hints" not in data.get("detection", {}):
        raise SkillValidationError(f"{source}: detection.lexical_hints is required")


def load_skills(skills_dir: Path) -> List[Dict[str, Any]]:
    skills: List[Dict[str, Any]] = []
    for skill_path in sorted(skills_dir.glob("*.yaml")):
        with skill_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        validate_skill(data, source=str(skill_path))
        data["_path"] = str(skill_path)
        skills.append(data)
    return skills
