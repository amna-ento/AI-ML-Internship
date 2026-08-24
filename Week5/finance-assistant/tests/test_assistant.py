from app.llm.assistant import ask_llm
from app.llm.conversation import Conversation


conversation = Conversation()

result = ask_llm(
    "Convert 100 USD to XYZ",
    conversation
)