import asyncio
import json

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ListToolsResult, CallToolResult

from app.services.user_service import get_user
from app.services.task_service import create_task, list_tasks


# TOOL DEFINITIONS

async def list_tools(context, params):

    return ListToolsResult(
        tools=[
            Tool(
                name="get_user",
                description="Get information about a user from the database.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "The ID of the user."
                        }
                    },
                    "required": ["user_id"]
                }
            ),

            Tool(
                name="create_task",
                description="Create a new task for a user.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "The ID of the user."
                        },
                        "title": {
                            "type": "string",
                            "description": "The task title."
                        }
                    },
                    "required": ["user_id", "title"]
                }
            ),

            Tool(
                name="list_tasks",
                description="Get all tasks belonging to a user.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "The ID of the user."
                        }
                    },
                    "required": ["user_id"]
                }
            ),

            Tool(
                name="get_weather",
                description="Get the current weather for a city.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The city to get weather for."
                        }
                    },
                    "required": ["city"]
                }
            )
        ]
    )


# TOOL EXECUTION

async def call_tool(context, request):

    name = request.name
    arguments = request.arguments or {}

    # GET USER

    if name == "get_user":

        result = get_user(
            arguments["user_id"]
        )

    # CREATE TASK

    elif name == "create_task":

        result = create_task(
            arguments["user_id"],
            arguments["title"]
        )

    # LIST TASKS

    elif name == "list_tasks":

        result = list_tasks(
            arguments["user_id"]
        )

    # GET WEATHER

    elif name == "get_weather":

        city = arguments["city"]

        # Temporary weather response
        result = {
            "city": city,
            "temperature": "30°C",
            "condition": "Sunny"
        }

    # ----------------------------------------------
    # UNKNOWN TOOL
    # ----------------------------------------------

    else:

        raise ValueError(f"Unknown tool: {name}")

    # ----------------------------------------------
    # RETURN MCP RESULT
    # ----------------------------------------------

    return CallToolResult(
        content=[
            TextContent(
                type="text",
                text=json.dumps(result)
            )
        ]
    )


# MCP SERVER

server = Server(
    "company-assistant",
    on_list_tools=list_tools,
    on_call_tool=call_tool,
)


# SERVER START

async def main():

    async with stdio_server() as (read_stream, write_stream):

        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())