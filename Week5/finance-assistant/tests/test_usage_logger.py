from app.llm.client import client
from app.utils.usage import log_usage


response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "What is 10 + 20?"
        }
    ]
)


cost = log_usage(
    "openai/gpt-oss-20b",
    response.usage
)


print("Prompt tokens:", response.usage.prompt_tokens)
print("Completion tokens:", response.usage.completion_tokens)
print("Total tokens:", response.usage.total_tokens)
print("Estimated cost:", cost)