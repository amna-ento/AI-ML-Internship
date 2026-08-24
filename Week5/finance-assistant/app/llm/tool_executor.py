import json

from app.tools.registry import TOOLS

from app.schemas.calculator import CalculateInput
from app.schemas.currency import ConvertCurrencyInput
from app.schemas.expense import (
    AddExpenseInput,
    QueryExpensesInput
)


INPUT_SCHEMAS = {
    "calculate": CalculateInput,
    "convert_currency": ConvertCurrencyInput,
    "add_expense": AddExpenseInput,
    "query_expenses": QueryExpensesInput,
}


def execute_tool(tool_name, arguments):

    try:

        # Find the requested tool
        tool = TOOLS.get(tool_name)

        if tool is None:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}"
            }

        # Find the Pydantic schema
        schema = INPUT_SCHEMAS.get(tool_name)

        if schema is None:
            return {
                "success": False,
                "error": f"No schema found for {tool_name}"
            }

        # Parse JSON arguments
        try:
            arguments = json.loads(arguments)

        except json.JSONDecodeError:
            return {
                "success": False,
                "error": "Tool received invalid JSON arguments."
            }

        # Validate arguments with Pydantic
        validated_input = schema(**arguments)

        # Execute the tool
        result = tool(validated_input)

        return result

    except Exception as error:

        return {
            "success": False,
            "error": f"Tool execution failed: {str(error)}"
        }
