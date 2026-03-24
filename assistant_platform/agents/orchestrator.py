from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any, Dict

from assistant_platform.agents.dialogue import DialogueAgent
from assistant_platform.agents.policy import PolicyAgent
from assistant_platform.agents.router import RouterAgent
from assistant_platform.agents.tool_executor import ToolExecutionAgent
from assistant_platform.dialogue.confirmation import explicit_confirmation_prompt, implicit_confirmation_text
from assistant_platform.dialogue.state_store import InMemoryDialogueStore
from assistant_platform.schemas.common import ConversationTurn, ToolCall


class OrchestratorAgent:
    def __init__(self, skills_dir: Path) -> None:
        self.router = RouterAgent(skills_dir=skills_dir)
        self.dialogue = DialogueAgent()
        self.executor = ToolExecutionAgent()
        self.policy = PolicyAgent()
        self.state = InMemoryDialogueStore()

    async def handle_turn(self, turn: ConversationTurn) -> Dict[str, Any]:
        dialogue_state = self.state.get(turn.session_id)
        routed = await self.router.route(turn)

        dialogue_state.active_skill = routed.skill_name
        dialogue_state.last_user_text = turn.user_text

        if routed.answer_directly:
            text = "Here is the answer based on your request."
            dialogue_state.last_assistant_text = text
            self.state.put(dialogue_state)
            return {"assistant_text": text, "dialogue_state": dialogue_state.model_dump(), "tool_trace": []}

        if routed.slot_status.missing_slots:
            prompt = await self.dialogue.next_prompt(routed, turn)
            dialogue_state.last_assistant_text = prompt
            self.state.put(dialogue_state)
            return {"assistant_text": prompt, "dialogue_state": dialogue_state.model_dump(), "tool_trace": []}

        tool_name = self._pick_tool(routed.skill_name, routed.slot_status.collected_slots)
        call = ToolCall(tool_name=tool_name, arguments=self._build_tool_args(tool_name, turn, routed.slot_status.collected_slots), call_id=str(uuid.uuid4()))

        policy = await self.policy.evaluate(call, turn)
        if not policy.allowed:
            text = policy.reason or "I can't perform that action."
            return {"assistant_text": text, "dialogue_state": dialogue_state.model_dump(), "tool_trace": []}

        if policy.requires_confirmation:
            if policy.confirmation_mode == "explicit":
                text = explicit_confirmation_prompt(call)
            else:
                text = implicit_confirmation_text(call)
                result = await self.executor.execute(call)
                return {
                    "assistant_text": text,
                    "dialogue_state": dialogue_state.model_dump(),
                    "tool_trace": [result.model_dump()],
                }
            return {"assistant_text": text, "dialogue_state": dialogue_state.model_dump(), "tool_trace": []}

        result = await self.executor.execute(call)
        if result.ok:
            text = self._render_success(tool_name, result.data)
        else:
            text = f"I couldn't complete that ({result.error_code})."

        dialogue_state.last_assistant_text = text
        self.state.put(dialogue_state)
        return {
            "assistant_text": text,
            "dialogue_state": dialogue_state.model_dump(),
            "tool_trace": [result.model_dump()],
        }

    def _pick_tool(self, skill_name: str, entities: Dict[str, Any]) -> str:
        if skill_name == "weather":
            if "aqi" in entities.get("expression", ""):
                return "get_air_quality"
            return "get_weather"
        if skill_name == "time_date":
            if entities.get("datetime") and entities.get("target_timezone"):
                return "convert_time"
            if entities.get("datetime"):
                return "get_date_info"
            return "get_current_time"
        if skill_name == "utilities":
            if entities.get("currency_pair"):
                return "currency_convert"
            if entities.get("unit_pair"):
                return "unit_convert"
            return "calculator"
        if skill_name == "reminders_timers_alarms":
            if entities.get("duration_seconds"):
                return "set_timer"
            return "create_reminder"
        return "calculator"

    def _build_tool_args(self, tool_name: str, turn: ConversationTurn, entities: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name == "get_weather":
            return {
                "location": entities.get("location") or turn.context.get("default_location"),
                "start_date_iso": None,
                "end_date_iso": None,
                "units": turn.context.get("units", "metric"),
            }
        if tool_name == "get_air_quality":
            return {"location": entities.get("location") or turn.context.get("default_location")}
        if tool_name == "get_current_time":
            return {"location": entities.get("location"), "timezone": turn.timezone}
        if tool_name == "get_date_info":
            return {"date_iso": entities.get("datetime"), "timezone": turn.timezone}
        if tool_name == "convert_time":
            return {
                "datetime_iso": entities.get("datetime"),
                "from_timezone": entities.get("from_timezone", turn.timezone),
                "to_timezone": entities.get("target_timezone", "UTC"),
            }
        if tool_name == "currency_convert":
            return {
                "amount": entities["amount"],
                "source_currency": entities["source_currency"],
                "target_currency": entities["target_currency"],
                "date_iso": None,
            }
        if tool_name == "unit_convert":
            return {
                "value": entities["value"],
                "from_unit": entities["from_unit"],
                "to_unit": entities["to_unit"],
            }
        if tool_name == "set_timer":
            return {"duration_seconds": entities["duration_seconds"], "label": None}
        if tool_name == "create_reminder":
            return {
                "reminder_text": turn.user_text,
                "remind_at_iso": entities.get("datetime"),
                "remind_on_arrival_location": None,
                "remind_on_departure_location": None,
            }
        return {"expression": turn.user_text}

    def _render_success(self, tool_name: str, data: Dict[str, Any]) -> str:
        if tool_name == "get_weather":
            return data.get("summary", "Weather fetched.")
        if tool_name == "get_current_time":
            return f"It is {data.get('local_time_human')} ({data.get('timezone')})."
        if tool_name == "currency_convert":
            return (
                f"{data.get('amount')} {data.get('source_currency')} = "
                f"{data.get('converted_amount')} {data.get('target_currency')}"
            )
        if tool_name == "unit_convert":
            return f"{data.get('original_value')} {data.get('original_unit')} = {data.get('converted_value')} {data.get('converted_unit')}"
        if tool_name == "set_timer":
            return f"Timer set. Ends at {data.get('ends_at_iso')}."
        if tool_name == "create_reminder":
            return f"Reminder created: {data.get('reminder_text')}"
        if tool_name == "calculator":
            return f"{data.get('expression')} = {data.get('result')}"
        return "Done."
