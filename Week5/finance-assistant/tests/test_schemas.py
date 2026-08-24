from app.schemas.calculator import CalculateInput
from app.schemas.currency import ConvertCurrencyInput
from app.schemas.expense import AddExpenseInput


# Valid calculator input
calculator = CalculateInput(
    expression="4500 + 500"
)

print("Calculator:", calculator)


# Valid currency input
currency = ConvertCurrencyInput(
    amount=100,
    from_currency="USD",
    to_currency="PKR"
)

print("Currency:", currency)


# Valid expense input
expense = AddExpenseInput(
    amount=4500,
    category="food",
    description="Groceries",
    date="2026-08-21",
    currency="PKR"
)

print("Expense:", expense)


