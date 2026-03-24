from pathlib import Path

from assistant_platform.routing.skill_loader import load_skills


def test_skills_load_and_validate() -> None:
    skills = load_skills(Path(__file__).resolve().parents[1] / "skills")
    assert len(skills) >= 12
    assert any(s["name"] == "utilities" for s in skills)
