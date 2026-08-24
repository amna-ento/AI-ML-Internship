import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from mcp.server.mcpserver import MCPServer

from app.database import initialize_database, get_expenses


mcp = MCPServer("Personal Finance MCP Server")


@mcp.tool()
def get_user_expenses(category: str = "") -> list[dict]:
    """Get personal expenses from the local database, optionally filtered by category."""
    initialize_database()
    return get_expenses(category if category else None)


if __name__ == "__main__":
    mcp.run(transport="stdio")