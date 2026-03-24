from __future__ import annotations

from datetime import datetime, timedelta
from typing import List
from uuid import uuid4

from pydantic import BaseModel

from assistant_platform.tools.registry import registry

TIMERS: dict[str, dict] = {}
REMINDERS: dict[str, dict] = {}
ALARMS: dict[str, dict] = {}


class SetTimerInput(BaseModel):
    duration_seconds: int
    label: str | None = None


class SetTimerOutput(BaseModel):
    timer_id: str
    ends_at_iso: str
    label: str | None = None


class CancelTimerInput(BaseModel):
    timer_id: str


class CancelTimerOutput(BaseModel):
    timer_id: str
    canceled: bool


class SetAlarmInput(BaseModel):
    trigger_at_iso: str
    recurrence_rule: str | None = None
    label: str | None = None


class SetAlarmOutput(BaseModel):
    alarm_id: str
    trigger_at_iso: str
    recurrence_rule: str | None = None


class CreateReminderInput(BaseModel):
    reminder_text: str
    remind_at_iso: str | None = None
    remind_on_arrival_location: str | None = None
    remind_on_departure_location: str | None = None


class CreateReminderOutput(BaseModel):
    reminder_id: str
    reminder_text: str
    remind_at_iso: str | None = None


class ListRemindersInput(BaseModel):
    start_date_iso: str | None = None
    end_date_iso: str | None = None


class ReminderItem(BaseModel):
    reminder_id: str
    reminder_text: str
    remind_at_iso: str | None = None
    status: str


class ListRemindersOutput(BaseModel):
    reminders: List[ReminderItem]


@registry.register(
    name="set_timer",
    description="Create countdown timer",
    input_model=SetTimerInput,
    output_model=SetTimerOutput,
)
async def set_timer(input: SetTimerInput) -> SetTimerOutput:
    timer_id = str(uuid4())
    ends_at = datetime.utcnow() + timedelta(seconds=input.duration_seconds)
    TIMERS[timer_id] = {"ends_at_iso": ends_at.isoformat() + "Z", "label": input.label}
    return SetTimerOutput(timer_id=timer_id, ends_at_iso=TIMERS[timer_id]["ends_at_iso"], label=input.label)


@registry.register(
    name="cancel_timer",
    description="Cancel timer",
    input_model=CancelTimerInput,
    output_model=CancelTimerOutput,
)
async def cancel_timer(input: CancelTimerInput) -> CancelTimerOutput:
    existed = input.timer_id in TIMERS
    if existed:
        TIMERS.pop(input.timer_id)
    return CancelTimerOutput(timer_id=input.timer_id, canceled=existed)


@registry.register(
    name="set_alarm",
    description="Create alarm",
    input_model=SetAlarmInput,
    output_model=SetAlarmOutput,
)
async def set_alarm(input: SetAlarmInput) -> SetAlarmOutput:
    alarm_id = str(uuid4())
    ALARMS[alarm_id] = input.model_dump()
    return SetAlarmOutput(alarm_id=alarm_id, trigger_at_iso=input.trigger_at_iso, recurrence_rule=input.recurrence_rule)


@registry.register(
    name="create_reminder",
    description="Create reminder",
    input_model=CreateReminderInput,
    output_model=CreateReminderOutput,
)
async def create_reminder(input: CreateReminderInput) -> CreateReminderOutput:
    reminder_id = str(uuid4())
    REMINDERS[reminder_id] = {
        "reminder_text": input.reminder_text,
        "remind_at_iso": input.remind_at_iso,
        "status": "active",
    }
    return CreateReminderOutput(reminder_id=reminder_id, reminder_text=input.reminder_text, remind_at_iso=input.remind_at_iso)


@registry.register(
    name="list_reminders",
    description="List reminders",
    input_model=ListRemindersInput,
    output_model=ListRemindersOutput,
)
async def list_reminders(input: ListRemindersInput) -> ListRemindersOutput:
    reminders = [
        ReminderItem(
            reminder_id=rid,
            reminder_text=rec["reminder_text"],
            remind_at_iso=rec.get("remind_at_iso"),
            status=rec["status"],
        )
        for rid, rec in REMINDERS.items()
    ]
    return ListRemindersOutput(reminders=reminders)
