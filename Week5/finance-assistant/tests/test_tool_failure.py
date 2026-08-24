from app.llm.tool_executor import execute_tool
from app.tools.registry import TOOLS


# Save the original currency tool
original_tool = TOOLS["convert_currency"]


# Replace it temporarily with a failing tool
def failing_currency_tool(arguments):

    raise ConnectionError(
        "Currency API is unavailable"
    )


TOOLS["convert_currency"] = failing_currency_tool


# Execute the tool
result = execute_tool(
    "convert_currency",
    '{"amount": 100, "from_currency": "USD", "to_currency": "PKR"}'
)

print("Currency tool failure:")
print(result)


# Restore the original tool
TOOLS["convert_currency"] = original_tool