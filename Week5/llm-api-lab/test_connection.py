import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

messages = [
    {
        "role": "system",
        "content": (
            "i am learning ai"
        ),
    },
    {
        "role": "user",
        "content": "What am i learning?",
    },
]


response1 = client.chat.completions.create(
    messages=messages,
    model="llama-3.3-70b-versatile",
)

assistant_message1 = response1.choices[0].message.content


messages.append(
    {
        "role": "assistant",
        "content": assistant_message1,
    }
)



print("Request 1:")
print("User: What am i learning?")
print("Assistant:", assistant_message1)



messages.append(
    {
        "role": "user",
        "content": "What is the scope of my learning?",
    }
)

response2 = client.chat.completions.create(
    messages=messages,
    model="llama-3.3-70b-versatile",
)

assistant_message2 = response2.choices[0].message.content


messages.append(
    {
        "role": "assistant",
        "content": assistant_message2,
    }
)

print("\nRequest 2:")
print("User: What is the scope of my learning?")
print("Assistant:", assistant_message2)