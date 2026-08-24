from app.llm.client import client
from app.llm.tool_definitions import TOOL_DEFINITIONS


response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "What's 4500 + 1200?"
        }
    ],
    tools=TOOL_DEFINITIONS,
    tool_choice="auto"
)


message = response.choices[0].message

print("Content:")
print(message.content)

print("\nTool calls:")
print(message.tool_calls)