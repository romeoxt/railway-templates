from typing import Any

from openai import AsyncOpenAI

from app.config import settings
from app.tools import TOOLS, run_tool


async def run_agent(prompt: str) -> dict[str, Any]:
    client = AsyncOpenAI(api_key=settings.openai_api_key)
    messages: list[dict[str, Any]] = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant with access to tools. "
                "Use tools when they improve accuracy. Keep final answers concise."
            ),
        },
        {"role": "user", "content": prompt},
    ]

    tool_trace: list[dict[str, str]] = []

    for _ in range(settings.max_tool_rounds):
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return {
                "answer": message.content or "",
                "tool_trace": tool_trace,
                "model": settings.openai_model,
            }

        messages.append(message.model_dump())

        for call in message.tool_calls:
            output = run_tool(call.function.name, call.function.arguments)
            tool_trace.append(
                {
                    "tool": call.function.name,
                    "arguments": call.function.arguments,
                    "output": output,
                }
            )
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": output,
                }
            )

    return {
        "answer": "Agent stopped after reaching the maximum number of tool rounds.",
        "tool_trace": tool_trace,
        "model": settings.openai_model,
    }
