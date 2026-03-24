from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel

from assistant_platform.tools.registry import registry


class GetCurrentTimeInput(BaseModel):
    location: str | None = None
    timezone: str | None = None


class GetCurrentTimeOutput(BaseModel):
    timezone: str
    local_time_iso: str
    local_time_human: str
    day_of_week: str


class ConvertTimeInput(BaseModel):
    datetime_iso: str
    from_timezone: str
    to_timezone: str


class ConvertTimeOutput(BaseModel):
    source_datetime_iso: str
    target_datetime_iso: str
    target_human: str


class GetDateInfoInput(BaseModel):
    date_iso: str | None = None
    timezone: str | None = None


class GetDateInfoOutput(BaseModel):
    date_iso: str
    day_of_week: str
    week_of_year: int
    month_name: str
    is_weekend: bool


@registry.register(
    name="get_current_time",
    description="Return current local time for a timezone",
    input_model=GetCurrentTimeInput,
    output_model=GetCurrentTimeOutput,
)
async def get_current_time(input: GetCurrentTimeInput) -> GetCurrentTimeOutput:
    tz_name = input.timezone or "UTC"
    now = datetime.now(ZoneInfo(tz_name))
    return GetCurrentTimeOutput(
        timezone=tz_name,
        local_time_iso=now.isoformat(),
        local_time_human=now.strftime("%I:%M %p"),
        day_of_week=now.strftime("%A"),
    )


@registry.register(
    name="convert_time",
    description="Convert datetime across timezones",
    input_model=ConvertTimeInput,
    output_model=ConvertTimeOutput,
)
async def convert_time(input: ConvertTimeInput) -> ConvertTimeOutput:
    src = datetime.fromisoformat(input.datetime_iso).replace(tzinfo=ZoneInfo(input.from_timezone))
    dst = src.astimezone(ZoneInfo(input.to_timezone))
    return ConvertTimeOutput(
        source_datetime_iso=src.isoformat(),
        target_datetime_iso=dst.isoformat(),
        target_human=dst.strftime("%Y-%m-%d %I:%M %p %Z"),
    )


@registry.register(
    name="get_date_info",
    description="Get date metadata",
    input_model=GetDateInfoInput,
    output_model=GetDateInfoOutput,
)
async def get_date_info(input: GetDateInfoInput) -> GetDateInfoOutput:
    tz_name = input.timezone or "UTC"
    if input.date_iso:
        dt = datetime.fromisoformat(input.date_iso)
    else:
        dt = datetime.now(ZoneInfo(tz_name))
    return GetDateInfoOutput(
        date_iso=dt.date().isoformat(),
        day_of_week=dt.strftime("%A"),
        week_of_year=int(dt.strftime("%V")),
        month_name=dt.strftime("%B"),
        is_weekend=dt.weekday() >= 5,
    )
