import json
from datetime import datetime, timezone
from typing import Any

TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Return the current UTC time in ISO-8601 format.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a basic arithmetic expression with +, -, *, /, and parentheses.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Arithmetic expression, e.g. (12 + 8) * 2",
                    }
                },
                "required": ["expression"],
            },
        },
    },
]


def _safe_eval(expression: str) -> float:
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        raise ValueError("Expression contains unsupported characters")
    return float(eval(expression, {"__builtins__": {}}, {}))


def run_tool(name: str, arguments: str) -> str:
    payload = json.loads(arguments or "{}")

    if name == "get_current_time":
        return datetime.now(timezone.utc).isoformat()

    if name == "calculate":
        result = _safe_eval(payload["expression"])
        return str(result)

    raise ValueError(f"Unknown tool: {name}")
