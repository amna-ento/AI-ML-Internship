import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "app.mcp.server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            tools = await session.list_tools()

            print("Available tools:")
            for tool in tools.tools:
                print(f"- {tool.name}")

            print("\nCalling create_task...")

            result = await session.call_tool(
                "create_task",
                {
                    "user_id": 1,
                    "title": "Prepare presentation",
                },
            )

            print("\nTool result:")
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
    
    
    
async def call_mcp_tool(session, tool_name, arguments):
    result = await session.call_tool(
        tool_name,
        arguments
    )

    return result    