from __future__ import annotations

from difflib import SequenceMatcher
from typing import Any, Dict


def semantic_similarity_bonus(user_text: str, skill: Dict[str, Any]) -> float:
    text = user_text.lower()
    best = 0.0
    samples = [skill.get("description", "")]
    samples.extend(skill.get("detection", {}).get("semantic_examples", []))
    for sample in samples:
        ratio = SequenceMatcher(None, text, str(sample).lower()).ratio()
        if ratio > best:
            best = ratio
    return best * 2.0
