from app.schemas.expense import (
    AddExpenseInput,
    QueryExpensesInput
)

from app.tools.expense import (
    add_expense,
    query_expenses
)


# Add food expense
add_expense(
    AddExpenseInput(
        amount=4500,
        category="food",
        description="Groceries",
        date="2026-08-21",
        currency="PKR"
    )
)


# Add transport expense
add_expense(
    AddExpenseInput(
        amount=1200,
        category="transport",
        description="Taxi",
        date="2026-08-20",
        currency="PKR"
    )
)


# Query all expenses
result = query_expenses(
    QueryExpensesInput()
)

print("\nAll expenses:")
print(result)


# Query food expenses
food_result = query_expenses(
    QueryExpensesInput(
        category="food"
    )
)

print("\nFood expenses:")
print(food_result)