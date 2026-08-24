from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# Path to the GitHub MCP server
SERVER_PATH = (
    "/Users/amento/Desktop/AI-ML-Internship/"
    "Week5/github-mcp-server/server.py"
)


# Call an MCP tool
async def call_mcp_tool(
    tool_name,
    arguments
):

    # Define how to start the MCP server
    server_params = StdioServerParameters(
        command="/Users/amento/Desktop/AI-ML-Internship/"
                "Week5/personal-finance-assistant/.venv/bin/python",
        args=[SERVER_PATH],
    )

    # Start the MCP server
    async with stdio_client(server_params) as (read, write):

        # Create MCP client session
        async with ClientSession(read, write) as session:

            # Initialize MCP connection
            await session.initialize()

            # Call the requested MCP tool
            result = await session.call_tool(
                tool_name,
                arguments
            )

            return result


# Test the MCP client
async def main():

    result = await call_mcp_tool(
        "get_repo_info",
        {
            "owner": "amna-ento",
            "repo": "AI-ML-Internship"
        }
    )

    print("Tool result:")
    print(result)


# Run the test
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())