from __future__ import annotations

from assistant_platform.schemas.common import RoutedAction


def missing_slot_question(routed: RoutedAction) -> str:
    if not routed.slot_status.missing_slots:
        return "Can you clarify what you'd like me to do?"
    slot = routed.slot_status.missing_slots[0]
    prompts = {
        "location": "Which location should I use?",
        "datetime": "When should I schedule it?",
        "duration_seconds": "How long should the timer be?",
        "reminder_text": "What should I remind you about?",
        "source_currency": "What is the source currency?",
        "target_currency": "What is the target currency?",
    }
    return prompts.get(slot, f"Could you provide {slot.replace('_', ' ')}?")
