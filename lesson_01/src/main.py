import json
import random
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from litellm import completion
import prompts as Prompts
from models import GptModels

# Global variables
history: List[Dict[str, Any]] = []

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "random_number",
            "description": "Generate a random integer in the interval 1..n (inclusive).",
            "parameters": {"type": "object", "properties": {"n": {"type": "integer"}}},
            "required": ["n"]
        }
    }
]

def random_number(n: int) -> int:
    """Returns a random integer between 1 and n (inclusive)."""
    return random.randint(1, int(n))

def init(model: GptModels, system_prompt: str) -> None:
    """Initializes the chatbot with a model and a system prompt."""
    global history
    history = [{"role": "system", "content": system_prompt}]

def run_question(question: str, model: Optional[GptModels] = None) -> str:
    """Processes a user question, handles tool calls, and returns the assistant's answer."""
    model_to_use = model or GptModels.gpt_4o_mini
    if question:
        history.append({"role": "user", "content": question})
    
    resp = completion(model=model_to_use.value, messages=history, tools=TOOLS)
    msg = resp["choices"][0]["message"]
    
    # Treat message and tool call entries as objects (getattr); accept only tools variant
    tool_calls = getattr(msg, "tool_calls", []) or []
    if not tool_calls:
        answer = getattr(msg, "content", "") or ""
        history.append({"role": "assistant", "content": answer})
        return answer
    
    # Normalize calls (expect objects with .function)
    tool_calls_list = []
    for tc in tool_calls:
        func = getattr(tc, "function", None)
        if not func or not getattr(func, "name", None):
            raise RuntimeError("invalid tool call")
        tool_calls_list.append({
            "id": getattr(tc, "id", "") or "",
            "name": getattr(func, "name"),
            "arguments": getattr(func, "arguments", "{}")
        })
    
    # Extract arguments for assistant message
    assistant_role = getattr(msg, "role", "assistant")
    assistant_content = getattr(msg, "content", "")
    assistant_tool_calls = tool_calls
    history.append({
        "role": assistant_role,
        "content": assistant_content,
        "tool_calls": assistant_tool_calls
    })
    
    # Execute each call and append outputs
    for call in tool_calls_list:
        name = call["name"]
        raw_args = call["arguments"] or "{}"
        try:
            args = json.loads(raw_args) if isinstance(raw_args, str) else (raw_args or {})
        except Exception:
            args = {}
        if name == "random_number":
            try:
                result = random_number(int(args.get("n", 1)))
            except Exception:
                result = "Error: invalid n"
        else:
            result = f"Unknown tool: {name}"
        history.append({
            "role": "tool",
            "name": name,
            "tool_call_id": call["id"] or None,
            "content": str(result)
        })
    
    # Single follow-up completion
    resp2 = completion(model=model_to_use.value, messages=history, tools=TOOLS)
    msg2 = resp2["choices"][0]["message"]
    answer = getattr(msg2, "content", "") or ""
    history.append({"role": "assistant", "content": answer})
    return answer

if __name__ == "__main__":
    load_dotenv()
    init(model=GptModels.gemma_3_4b_instruct, system_prompt=Prompts.LESSON_01_CHATBOT)
    
    question = "Roll a dice three times, tell me the numbers and their sum."
    print(question)
    
    answer = run_question(question)
    print(answer)
    
