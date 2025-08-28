from chatbot import Chatbot
from models import GptModels
from prompts import LESSON_0_CHATBOT

def main():
    bot = Chatbot(model=GptModels.gemma_3_4b_instruct, system_prompt=LESSON_0_CHATBOT)
    print("Type 'exit' to quit.")
    
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            print("Goodbye!")
            break
        try:
            answer = bot.ask(user_input)
            print(f"Bot: {answer}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
            break
    
if __name__ == "__main__":
    main()
