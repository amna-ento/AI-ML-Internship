import asyncio

from app.mcp.client import connect_to_github_mcp


async def main():

    tools = await connect_to_github_mcp()

    print("MCP tools:")

    for tool in tools:
        print(f"- {tool.name}")

    # Call GitHub MCP tool
    result = await tools[0].call(
        {
            "owner": "amna-ento",
            "repo": "AI-ML-Internship"
        }
    )

    print("\nTool result:")
    print(result)


asyncio.run(main())