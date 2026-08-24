from typing import Any

from pydantic import BaseModel


class ToolResult(BaseModel):
    success: bool
    tool: str
    data: dict[str, Any]
    error: str | None = None


class FinanceResponse(BaseModel):
    answer: str
    tool_used: list[str]
    status: str
    data: dict[str, Any]