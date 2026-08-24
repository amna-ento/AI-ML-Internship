from app.llm.client import client


response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "What is 2 + 2?"
        }
    ]
)


print("Response:")
print(response.choices[0].message.content)

print("\nUsage:")
print(response.usage)

print("\nPrompt tokens:")
print(response.usage.prompt_tokens)

print("\nCompletion tokens:")
print(response.usage.completion_tokens)

print("\nTotal tokens:")
print(response.usage.total_tokens)