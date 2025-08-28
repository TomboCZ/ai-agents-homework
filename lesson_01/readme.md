# Lesson 1: AI chatbot based on LiteLLM with external tool support

This example demonstrates a simple chatbot using LiteLLM to call various models, including locally hosted ones (e.g., via LM Studio or Ollama). The chatbot also supports function calling (external tools) using the OpenAI-compatible API.

## Prerequisites
- Install dependencies from `requirements.txt`
- If you want to use locally inferred models, set up a compatible provider (e.g., LM Studio, Ollama, etc.)
- Rename `.env.example` to `.env` and fill in your API keys and URLs
- Note: LM Studio requires an API key (even a dummy one)


## Usage
- Run the chatbot with `python main.py`
- Experiment with different models; try asking questions that require external tools (e.g., Wolfram Alpha) if supported by your model

File structure:
- `chatbot.py` – main class
- `models.py` – enum of available models
- `main.py` – CLI runner

Switching model in code (example):
```python
from chatbot import Chatbot
from models import GptModels
bot = Chatbot(system_prompt="Hi", model=GptModels.gpt_4o_mini)
print(bot.ask("Hello!"))
print(bot.ask("Now use local model", model=GptModels.gemma_3_4b_instruct))
```

---

## License
This repository is licensed under the [MIT License](LICENSE)