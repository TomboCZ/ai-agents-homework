# Lesson 1: AI chatbot based on LiteLLM with external tool support

This example demonstrates a simple chatbot using LiteLLM to call various models, including locally hosted ones (e.g., via LM Studio or Ollama). The chatbot also supports function calling (external tools) using the OpenAI-compatible API.

## Prerequisites
- Install dependencies from `requirements.txt`
- If you want to use locally inferred models, set up a compatible provider (e.g., LM Studio, Ollama, etc.)
- Rename `.env.example` to `.env` and fill in your API keys and URLs
- Note: LM Studio requires an API key (even a dummy one)

## Usage
- Run the chatbot with `python src/main.py`
- Experiment with different models; try asking questions that require external tools (e.g., Wolfram Alpha) if supported by your model

File structure:
- `src/main.py` – minimal `ChatBot` with simple tool-calling
- `models.py` – enum of available models
- `prompts.py` – system prompts and texts
- `.env.example` – example environment file

Example of switching models in code 
(when using local inference, make sure to declare it correctly in `models.py` and set the corresponding `API_BASE` and `API_KEY` in your `.env` file)
```python
from models import GptModels
import prompts as Prompts
from src.main import ChatBot

bot = ChatBot(model=GptModels.gpt_4o_mini, system_prompt=Prompts.LESSON_01_CHATBOT)
print(bot.ask("Hello!"))
```

---

## License
This repository is licensed under the [MIT License](LICENSE)
