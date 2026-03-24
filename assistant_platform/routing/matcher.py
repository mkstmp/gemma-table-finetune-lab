from __future__ import annotations

from typing import Any, Dict, List, Tuple

from assistant_platform.routing.semantic_ranker import semantic_similarity_bonus


def _entity_bonus(skill: Dict[str, Any], extracted: Dict[str, Any]) -> float:
    score = 0.0
    hints = skill.get("detection", {}).get("entity_hints", {})
    if "currency_pair" in hints and extracted.get("currency_pair"):
        score += 3.0
    if "location" in hints and extracted.get("location"):
        score += 1.5
    if "datetime" in hints and extracted.get("datetime"):
        score += 1.0
    if "duration" in hints and extracted.get("duration_seconds"):
        score += 1.0
    return score


def match_skill(user_text: str, skills: List[Dict[str, Any]], extracted_entities: Dict[str, Any]) -> Tuple[Dict[str, Any], float]:
    candidates: List[Tuple[float, Dict[str, Any]]] = []
    lower_text = user_text.lower()

    for skill in skills:
        score = 0.0
        hints = skill.get("detection", {}).get("lexical_hints", [])
        for hint in hints:
            if str(hint).lower() in lower_text:
                score += 1.0

        score += _entity_bonus(skill, extracted_entities)
        score += semantic_similarity_bonus(user_text, skill)

        priority = str(skill.get("priority", "medium")).lower()
        if priority == "high":
            score += 0.25
        elif priority == "low":
            score -= 0.1

        candidates.append((score, skill))

    candidates.sort(key=lambda x: x[0], reverse=True)
    best_score, best_skill = candidates[0]
    confidence = 0.5
    if len(candidates) > 1:
        gap = best_score - candidates[1][0]
        confidence = max(0.05, min(0.99, 0.5 + gap / 4.0))
    return best_skill, confidence
