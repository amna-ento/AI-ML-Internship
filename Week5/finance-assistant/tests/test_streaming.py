from app.llm.client import client


response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "Explain personal finance in 3 short sentences."
        }
    ],
    stream=True
)


print("Assistant: ", end="", flush=True)

for chunk in response:

    content = chunk.choices[0].delta.content

    if content:
        print(content, end="", flush=True)

print()