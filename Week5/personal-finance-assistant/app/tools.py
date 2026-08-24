import ast
import operator
import requests

from app.database import get_expenses as query_expenses
from app.models import ToolResult


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg
}


def safe_calculate(expression: str):
    node = ast.parse(expression, mode="eval").body

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](safe_calculate(ast.unparse(node.operand)))

    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        left = safe_calculate(ast.unparse(node.left))
        right = safe_calculate(ast.unparse(node.right))
        return OPERATORS[type(node.op)](left, right)

    raise ValueError("Only basic arithmetic expressions are supported")


def calculator(expression: str) -> ToolResult:
    try:
        result = safe_calculate(expression)

        return ToolResult(
            success=True,
            tool="calculator",
            data={
                "expression": expression,
                "result": result
            }
        )

    except Exception as error:
        return ToolResult(
            success=False,
            tool="calculator",
            data={},
            error=str(error)
        )


def currency_converter(
    amount: float,
    from_currency: str,
    to_currency: str
) -> ToolResult:
    try:
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        if from_currency == to_currency:
            return ToolResult(
                success=True,
                tool="currency_converter",
                data={
                    "amount": amount,
                    "from_currency": from_currency,
                    "to_currency": to_currency,
                    "rate": 1,
                    "converted_amount": amount
                }
            )

        response = requests.get(
            f"https://api.frankfurter.dev/v2/rate/{from_currency}/{to_currency}",
            timeout=10
        )

        response.raise_for_status()
        result = response.json()

        rate = result["rate"]
        converted_amount = amount * rate

        return ToolResult(
            success=True,
            tool="currency_converter",
            data={
                "amount": amount,
                "from_currency": from_currency,
                "to_currency": to_currency,
                "converted_amount": round(converted_amount, 2),
                "rate": rate
            }
        )

    except requests.Timeout:
        return ToolResult(
            success=False,
            tool="currency_converter",
            data={},
            error="Currency API request timed out"
        )

    except requests.RequestException as error:
        return ToolResult(
            success=False,
            tool="currency_converter",
            data={},
            error=f"Currency API request failed: {error}"
        )

    except Exception as error:
        return ToolResult(
            success=False,
            tool="currency_converter",
            data={},
            error=str(error)
        )


def get_expenses(category: str | None = None) -> ToolResult:
    try:
        expenses = query_expenses(category)

        return ToolResult(
            success=True,
            tool="get_expenses",
            data={
                "expenses": expenses,
                "count": len(expenses)
            }
        )

    except Exception as error:
        return ToolResult(
            success=False,
            tool="get_expenses",
            data={},
            error=str(error)
        )