from __future__ import annotations

from typing import Dict

from assistant_platform.schemas.dialogue import DialogueState


class InMemoryDialogueStore:
    def __init__(self) -> None:
        self._store: Dict[str, DialogueState] = {}

    def get(self, session_id: str) -> DialogueState:
        if session_id not in self._store:
            self._store[session_id] = DialogueState(session_id=session_id)
        return self._store[session_id]

    def put(self, state: DialogueState) -> None:
        self._store[state.session_id] = state
