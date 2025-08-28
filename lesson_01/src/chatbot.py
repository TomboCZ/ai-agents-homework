import os
from dotenv import load_dotenv
load_dotenv()
import litellm

from litellm import completion
from models import GptModels

class Chatbot:
    def __init__(self, system_prompt: str, model: GptModels = GptModels.gpt_4o_mini):
        """Initialize Chatbot with system prompt and model."""
        self.system_prompt = system_prompt
        self.model = model.value                
        self.clear()

    def clear(self):
        """
        Clears the conversation history, resetting it to contain only the initial system prompt.
        """
        self.history = [{"role": "system", "content": self.system_prompt}]

    def ask(self, question: str, model: GptModels | None = None) -> str:
        """Ask a question and optionally override the model for this single call.
        Args:
            question: user message
            model: optional different GptModels enum value; if None uses the instance default
        """
        self.history.append({"role": "user", "content": question})
        effective_model = model.value if model else self.model
        completion_args = dict(model=effective_model, messages=self.history)
        
        try:
            response = completion(**completion_args)
            answer = response["choices"][0]["message"]["content"]
            self.history.append({"role": "assistant", "content": answer})
            return answer
        except Exception as e:
            print(f"ERROR: {type(e).__name__}: {str(e)}")
            raise

if __name__ == "__main__":
    bot = Chatbot(
        system_prompt="You are a helpful assistant.",  
        model=GptModels.gemma_3_4b_instruct
    )

    question = "Hello, what model are you?"  
    answer = bot.ask(question)
    print(f"Question: {question}")
    print(f"Answer: {answer}")
    print()

    question = "And now?" 
    answer = bot.ask(model=GptModels.gpt_4o_mini, question=question)
    print(f"Question: {question}")
    print(f"Answer: {answer}")



