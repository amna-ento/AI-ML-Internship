import asyncio
import json
import os
import sys

from dotenv import load_dotenv
from groq import Groq
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "openai/gpt-oss-20b"


SYSTEM_PROMPT = """
You are a company assistant.

You can ONLY help with these operations:

1. get_user
   Use when the user asks for their user/account information.

2. get_weather
   Use when the user asks about weather for a specific city.
   If no city is provided, ask which city they mean.

3. create_task
   Use ONLY when the user explicitly asks to create, add, schedule,
   or remember a task.

4. list_tasks
   Use when the user asks to see, show, list, retrieve, or view their tasks.

Important rules:

- Never create a task just because the user mentions an activity.
- Only create a task when the user explicitly asks you to create/remember it.
- For get_user, create_task, and list_tasks, always use the current user_id
  provided by the application.
- Never ask the user for their user_id.
- Never invent tool calls.
- Do not use tools for unrelated requests.

If the request is unrelated to these operations, respond exactly:

"I'm a company assistant, I cannot help you with that."
"""

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_user",
            "description": "Get information about the current user from the database.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "Create a new task for the current user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the task.",
                    }
                },
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city to get weather information for.",
                    }
                },
                "required": ["city"],
            },
        },
    },
]


def ask_llm(message: str):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        tools=TOOL_DEFINITIONS,
        tool_choice="auto",
    )

    return response


def inspect_tool_call(message: str):
    response = ask_llm(message)

    choice = response.choices[0]

    print("Finish reason:", choice.finish_reason)
    print("Message:", choice.message)

    if choice.message.tool_calls:
        for tool_call in choice.message.tool_calls:
            print("Tool:", tool_call.function.name)
            print("Arguments:", tool_call.function.arguments)


async def call_mcp_tool(tool_name: str, arguments: dict):
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "app.mcp.server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                tool_name,
                arguments,
            )

            return result


async def run_assistant(message: str, user_id: int):
    messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": message,
    }
]

    while True:

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto",
        )

        assistant_message = response.choices[0].message

        if not assistant_message.tool_calls:
            return assistant_message.content

        messages.append(assistant_message)

        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            # Add authenticated/current user ID internally.
            if tool_name in {"get_user", "create_task"}:
                arguments["user_id"] = user_id

            result = await call_mcp_tool(
                tool_name,
                arguments,
            )

            # Extract actual MCP text result.
            if result.content:
                tool_result = result.content[0].text
            else:
                tool_result = "Tool returned no result."

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                }
            )


async def run_assistant(message: str, user_id: int):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": message,
        }
    ]

    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto",
        )

        assistant_message = response.choices[0].message

        if not assistant_message.tool_calls:
            return assistant_message.content

        messages.append(assistant_message)

        for tool_call in assistant_message.tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            if tool_name in {"get_user", "create_task", "list_tasks"}:
                arguments["user_id"] = user_id

            result = await call_mcp_tool(
                tool_name,
                arguments,
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result.model_dump()),
                }
            )