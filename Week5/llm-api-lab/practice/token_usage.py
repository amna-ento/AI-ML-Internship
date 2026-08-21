import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "Explain what machine learning is in 3 sentences."
        }
    ]
)

print("Response:")
print(response.choices[0].message.content)

print("\nUsage:")
print(response.usage)

print("\nUsage:")

print("Prompt tokens:", response.usage.prompt_tokens)
print("Completion tokens:", response.usage.completion_tokens)
print("Total tokens:", response.usage.total_tokens)

input_cost = (response.usage.prompt_tokens / 1_000_000) * 0.075
output_cost = (response.usage.completion_tokens / 1_000_000) * 0.30

total_cost = input_cost + output_cost

print("\nCost:")

input_tokens = response.usage.prompt_tokens
output_tokens = response.usage.completion_tokens
total_tokens = response.usage.total_tokens

input_cost = (input_tokens / 1_000_000) * 0.075
output_cost = (output_tokens / 1_000_000) * 0.30
total_cost = input_cost + output_cost

print("\n--- Usage Summary ---")
print(f"Input tokens: {input_tokens}")
print(f"Output tokens: {output_tokens}")
print(f"Total tokens: {total_tokens}")

print("\n--- Cost Summary ---")
print(f"Input cost: ${input_cost:.8f}")
print(f"Output cost: ${output_cost:.8f}")
print(f"Total cost: ${total_cost:.8f}")