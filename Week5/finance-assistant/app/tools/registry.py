from app.tools.calculator import calculate
from app.tools.currency import convert_currency
from app.tools.expense import add_expense, query_expenses


TOOLS = {
    "calculate": calculate,
    "convert_currency": convert_currency,
    "add_expense": add_expense,
    "query_expenses": query_expenses,
}