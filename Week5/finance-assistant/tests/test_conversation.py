from app.llm.assistant import ask_llm
from app.llm.conversation import Conversation


conversation = Conversation()


response = ask_llm(
    "My name is Amento.",
    conversation
)

print("\nAssistant:")
print(response)


response = ask_llm(
    "What is my name?",
    conversation
)

print("\nAssistant:")
print(response)