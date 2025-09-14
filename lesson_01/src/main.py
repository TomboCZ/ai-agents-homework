import json
import random
from typing import Any, Callable, Dict, List, Optional

from dotenv import load_dotenv
from litellm import completion

import prompts as Prompts
from models import GptModels


# Tool schema advertised to the model (OpenAI-compatible)
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "random_number",
            "description": "Generate a random integer in the interval 1..n (inclusive).",
            "parameters": {
                "type": "object",
                "properties": {"n": {"type": "integer", "minimum": 1}},
                "required": ["n"],
            },
        },
    }
]


def random_number(n: int) -> int:
    """Return a random integer between 1 and n (inclusive)."""
    return random.randint(1, int(n))


class ChatBot:
    """Minimal chat agent with optional tool-calling support."""

    def __init__(self, model: GptModels, system_prompt: str):
        self.model = model
        self.history: List[Dict[str, Any]] = [
            {"role": "system", "content": system_prompt}
        ]
        # Map tool name -> callable
        self.tools: Dict[str, Callable[..., Any]] = {
            "random_number": random_number,
        }

    def ask(self, question: str) -> str:
        """Send a user question, handle tool calls, and return assistant text."""
        if question:
            self.history.append({"role": "user", "content": question})

        first = completion(
            model=self.model.value,
            messages=self.history,
            tools=TOOLS_SCHEMA,
        )
        msg = first["choices"][0]["message"]
        tool_calls = msg.get("tool_calls") or []

        # If no tool calls, return the content directly
        if not tool_calls:
            answer = msg.get("content", "") or ""
            self.history.append({"role": "assistant", "content": answer})
            return answer

        # Append assistant tool_calls turn
        self.history.append(
            {
                "role": msg.get("role", "assistant"),
                "content": msg.get("content", ""),
                "tool_calls": tool_calls,
            }
        )

        # Execute tools and append tool results
        for call in tool_calls:
            fn = (call.get("function") or {})
            name = fn.get("name")
            args_raw = fn.get("arguments") or "{}"
            try:
                args = json.loads(args_raw) if isinstance(args_raw, str) else (args_raw or {})
            except Exception:
                args = {}

            result: Any
            if name in self.tools:
                try:
                    result = self.tools[name](**args)
                except TypeError:
                    # Fallback for tools defined with positional args
                    result = self.tools[name](*args.values())
                except Exception as e:
                    result = f"Error: {e}"
            else:
                result = f"Unknown tool: {name}"

            self.history.append(
                {
                    "role": "tool",
                    "name": name,
                    "tool_call_id": call.get("id"),
                    "content": str(result),
                }
            )

        # Follow-up completion to incorporate tool results
        follow = completion(
            model=self.model.value,
            messages=self.history,
            tools=TOOLS_SCHEMA,
        )
        final_msg = follow["choices"][0]["message"]
        answer = final_msg.get("content", "") or ""
        self.history.append({"role": "assistant", "content": answer})
        return answer


if __name__ == "__main__":
    load_dotenv()
    bot = ChatBot(model=GptModels.gemma_3_4b_instruct, system_prompt=Prompts.LESSON_01_CHATBOT)
    prompt = "Roll a dice three times, tell me the numbers and their sum."
    print(prompt)
    print(bot.ask(prompt))
