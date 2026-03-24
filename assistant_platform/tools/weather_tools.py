from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel

from assistant_platform.tools.registry import registry


class GetWeatherInput(BaseModel):
    location: str
    start_date_iso: str | None = None
    end_date_iso: str | None = None
    units: str = "metric"


class WeatherPeriod(BaseModel):
    timestamp_iso: str
    condition: str
    temperature: float
    precipitation_probability: float | None = None
    wind_speed: float | None = None


class GetWeatherOutput(BaseModel):
    location_resolved: str
    timezone: str
    periods: List[WeatherPeriod]
    summary: str


class GetAirQualityInput(BaseModel):
    location: str


class GetAirQualityOutput(BaseModel):
    location_resolved: str
    aqi: int
    category: str
    primary_pollutant: str | None = None


@registry.register(
    name="get_weather",
    description="Get current weather or forecast",
    input_model=GetWeatherInput,
    output_model=GetWeatherOutput,
)
async def get_weather(input: GetWeatherInput) -> GetWeatherOutput:
    now = datetime.utcnow().isoformat() + "Z"
    temp = 22.0 if input.units == "metric" else 71.6
    period = WeatherPeriod(
        timestamp_iso=now,
        condition="Partly cloudy",
        temperature=temp,
        precipitation_probability=0.1,
        wind_speed=8.0,
    )
    summary = f"{input.location}: {period.condition}, {period.temperature}{'C' if input.units == 'metric' else 'F'}."
    return GetWeatherOutput(
        location_resolved=input.location,
        timezone="UTC",
        periods=[period],
        summary=summary,
    )


@registry.register(
    name="get_air_quality",
    description="Get AQI",
    input_model=GetAirQualityInput,
    output_model=GetAirQualityOutput,
)
async def get_air_quality(input: GetAirQualityInput) -> GetAirQualityOutput:
    return GetAirQualityOutput(
        location_resolved=input.location,
        aqi=58,
        category="Moderate",
        primary_pollutant="PM2.5",
    )
