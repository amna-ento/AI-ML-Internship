import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

messages = []

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Conversation ended.")
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        stream=True
    )
    print("\r" + " " * 15 + "\r", end="", flush=True)
    assistant_response = ""

    print("Assistant:", end=" ")

    for chunk in response:
        content = chunk.choices[0].delta.content

        if content:
            print(content, end="", flush=True)
            assistant_response += content

    print()

    messages.append({
        "role": "assistant",
        "content": assistant_response
    })    