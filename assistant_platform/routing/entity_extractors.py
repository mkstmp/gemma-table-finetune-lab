from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from dateutil import parser

CURRENCIES = {"usd", "inr", "eur", "gbp", "cad", "aud", "jpy"}
UNITS = {
    "km": "length",
    "kilometer": "length",
    "kilometers": "length",
    "mile": "length",
    "miles": "length",
    "c": "temperature",
    "f": "temperature",
    "celsius": "temperature",
    "fahrenheit": "temperature",
    "kg": "mass",
    "lb": "mass",
    "lbs": "mass",
}


class EntityExtractor:
    def extract(self, user_text: str, now: Optional[datetime] = None) -> Dict[str, Any]:
        now = now or datetime.now()
        text = user_text.strip()
        entities: Dict[str, Any] = {}

        entities.update(self.extract_currency_pair(text))
        entities.update(self.extract_unit_pair(text))
        entities.update(self.extract_duration(text))
        entities.update(self.extract_datetime(text, now=now))

        location = self.extract_location(text)
        if location:
            entities["location"] = location

        contact = self.extract_contact_name(text)
        if contact:
            entities["contact_name"] = contact

        expression = self.extract_math_expression(text)
        if expression:
            entities["expression"] = expression

        return entities

    def extract_datetime(self, text: str, now: datetime) -> Dict[str, Any]:
        lower = text.lower()
        if "tomorrow" in lower:
            target = (now + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
            return {"datetime": target.isoformat()}
        if "today" in lower:
            target = now.replace(hour=now.hour, minute=0, second=0, microsecond=0)
            return {"datetime": target.isoformat()}

        match = re.search(r"\b(at\s+)?(\d{1,2}(:\d{2})?\s?(am|pm))\b", lower)
        if match:
            try:
                dt = parser.parse(match.group(2), default=now)
                return {"datetime": dt.isoformat()}
            except Exception:
                return {}
        return {}

    def extract_duration(self, text: str) -> Dict[str, Any]:
        match = re.search(r"(\d+)\s*(seconds?|minutes?|hours?)", text.lower())
        if not match:
            return {}
        amount = int(match.group(1))
        unit = match.group(2)
        multiplier = 1
        if unit.startswith("minute"):
            multiplier = 60
        elif unit.startswith("hour"):
            multiplier = 3600
        return {"duration_seconds": amount * multiplier}

    def extract_currency_pair(self, text: str) -> Dict[str, Any]:
        lower = text.lower()
        m = re.search(r"(\d+(\.\d+)?)\s*([a-z]{3})\s*(to|in)\s*([a-z]{3})", lower)
        if not m:
            return {}
        src = m.group(3)
        dst = m.group(5)
        if src in CURRENCIES and dst in CURRENCIES:
            return {
                "amount": float(m.group(1)),
                "source_currency": src.upper(),
                "target_currency": dst.upper(),
                "currency_pair": f"{src.upper()}_{dst.upper()}",
            }
        return {}

    def extract_unit_pair(self, text: str) -> Dict[str, Any]:
        lower = text.lower()
        m = re.search(r"(\d+(\.\d+)?)\s*([a-z]+)\s*(to|in)\s*([a-z]+)", lower)
        if not m:
            return {}
        from_unit = m.group(3)
        to_unit = m.group(5)
        if from_unit in UNITS and to_unit in UNITS:
            return {
                "value": float(m.group(1)),
                "from_unit": from_unit,
                "to_unit": to_unit,
                "unit_pair": f"{from_unit}_{to_unit}",
            }
        return {}

    def extract_contact_name(self, text: str) -> Optional[str]:
        m = re.search(r"(?:text|call|email)\s+([A-Z][a-zA-Z]+)", text)
        return m.group(1) if m else None

    def extract_location(self, text: str) -> Optional[str]:
        for token in [" in ", " at ", " near "]:
            if token in text.lower():
                idx = text.lower().rfind(token)
                candidate = text[idx + len(token) :].strip(" ?.!")
                if candidate:
                    return candidate
        return None

    def extract_math_expression(self, text: str) -> Optional[str]:
        if re.fullmatch(r"[0-9\s\+\-\*\/\(\)\.]+", text.strip()):
            return text.strip()
        if any(k in text.lower() for k in ["plus", "minus", "times", "divided by"]):
            return (
                text.lower()
                .replace("plus", "+")
                .replace("minus", "-")
                .replace("times", "*")
                .replace("divided by", "/")
            )
        return None
