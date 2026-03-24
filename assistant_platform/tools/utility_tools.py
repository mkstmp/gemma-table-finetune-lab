from __future__ import annotations

import ast
from datetime import datetime

from pydantic import BaseModel

from assistant_platform.tools.base import ToolExecutionError
from assistant_platform.tools.registry import registry

RATES = {
    ("USD", "INR"): 83.0,
    ("INR", "USD"): 1 / 83.0,
    ("USD", "EUR"): 0.92,
    ("EUR", "USD"): 1.087,
    ("GBP", "USD"): 1.27,
    ("USD", "GBP"): 0.787,
}


class CalculatorInput(BaseModel):
    expression: str


class CalculatorOutput(BaseModel):
    expression: str
    result: str


class UnitConvertInput(BaseModel):
    value: float
    from_unit: str
    to_unit: str


class UnitConvertOutput(BaseModel):
    original_value: float
    original_unit: str
    converted_value: float
    converted_unit: str


class CurrencyConvertInput(BaseModel):
    amount: float
    source_currency: str
    target_currency: str
    date_iso: str | None = None


class CurrencyConvertOutput(BaseModel):
    amount: float
    source_currency: str
    target_currency: str
    converted_amount: float
    exchange_rate: float
    rate_timestamp_iso: str | None = None


def _safe_eval(expr: str) -> float:
    node = ast.parse(expr, mode="eval")
    allowed = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub)
    if not all(isinstance(n, allowed) for n in ast.walk(node)):
        raise ToolExecutionError("VALIDATION_ERROR", "Unsafe expression")
    return float(eval(compile(node, "<expr>", "eval"), {"__builtins__": {}}, {}))


@registry.register(
    name="calculator",
    description="Evaluate safe mathematical expression",
    input_model=CalculatorInput,
    output_model=CalculatorOutput,
)
async def calculator(input: CalculatorInput) -> CalculatorOutput:
    result = _safe_eval(input.expression)
    return CalculatorOutput(expression=input.expression, result=str(result))


@registry.register(
    name="unit_convert",
    description="Convert compatible units",
    input_model=UnitConvertInput,
    output_model=UnitConvertOutput,
)
async def unit_convert(input: UnitConvertInput) -> UnitConvertOutput:
    src = input.from_unit.lower()
    dst = input.to_unit.lower()

    if src in {"mile", "miles"} and dst in {"km", "kilometer", "kilometers"}:
        converted = input.value * 1.60934
    elif src in {"km", "kilometer", "kilometers"} and dst in {"mile", "miles"}:
        converted = input.value / 1.60934
    elif src in {"c", "celsius"} and dst in {"f", "fahrenheit"}:
        converted = (input.value * 9 / 5) + 32
    elif src in {"f", "fahrenheit"} and dst in {"c", "celsius"}:
        converted = (input.value - 32) * 5 / 9
    elif src in {"kg"} and dst in {"lb", "lbs"}:
        converted = input.value * 2.20462
    elif src in {"lb", "lbs"} and dst in {"kg"}:
        converted = input.value / 2.20462
    else:
        raise ToolExecutionError("VALIDATION_ERROR", f"Incompatible or unsupported units: {src} to {dst}")

    return UnitConvertOutput(
        original_value=input.value,
        original_unit=input.from_unit,
        converted_value=round(converted, 6),
        converted_unit=input.to_unit,
    )


@registry.register(
    name="currency_convert",
    description="Convert currencies",
    input_model=CurrencyConvertInput,
    output_model=CurrencyConvertOutput,
)
async def currency_convert(input: CurrencyConvertInput) -> CurrencyConvertOutput:
    src = input.source_currency.upper()
    dst = input.target_currency.upper()
    if src == dst:
        rate = 1.0
    else:
        key = (src, dst)
        if key not in RATES:
            raise ToolExecutionError("NOT_FOUND", f"Unsupported currency pair: {src}->{dst}")
        rate = RATES[key]

    converted = input.amount * rate
    return CurrencyConvertOutput(
        amount=input.amount,
        source_currency=src,
        target_currency=dst,
        converted_amount=round(converted, 6),
        exchange_rate=rate,
        rate_timestamp_iso=datetime.utcnow().isoformat() + "Z",
    )
