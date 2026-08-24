from app.database.repository import (
    add_expense,
    get_expenses,
    get_expenses_by_category,
    get_expenses_by_date_range,
    get_total_expenses
)


# Add sample expenses
add_expense(
    1200,
    "transport",
    "Taxi",
    "2026-08-20",
    "PKR"
)

add_expense(
    2500,
    "food",
    "Restaurant",
    "2026-08-19",
    "PKR"
)


# Get all expenses
print("\nAll expenses:")
print(get_expenses())


# Get food expenses
print("\nFood expenses:")
print(get_expenses_by_category("food"))


# Get expenses within a date range
print("\nExpenses from August 19 to August 21:")
print(
    get_expenses_by_date_range(
        "2026-08-19",
        "2026-08-21"
    )
)


# Get total food spending
print("\nTotal food spending:")
print(
    get_total_expenses(category="food")
)


# Get total spending in date range
print("\nTotal spending from August 19 to August 21:")
print(
    get_total_expenses(
        start_date="2026-08-19",
        end_date="2026-08-21"
    )
)