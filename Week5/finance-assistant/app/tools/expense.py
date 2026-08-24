from app.schemas.expense import (
    AddExpenseInput,
    AddExpenseOutput,
    QueryExpensesInput,
    QueryExpensesOutput,
    ExpenseRecord
)

from app.database.repository import (
    add_expense as db_add_expense,
    get_expenses,
    get_expenses_by_category,
    get_expenses_by_date_range,
    get_total_expenses
)


def add_expense(data: AddExpenseInput) -> AddExpenseOutput:
    expense_id = db_add_expense(
        data.amount,
        data.category,
        data.description,
        data.date,
        data.currency.upper()
    )

    return AddExpenseOutput(
        success=True,
        expense_id=expense_id,
        message="Expense added successfully."
    )


def query_expenses(
    data: QueryExpensesInput
) -> QueryExpensesOutput:

    if data.category:
        rows = get_expenses_by_category(data.category)

    elif data.start_date and data.end_date:
        rows = get_expenses_by_date_range(
            data.start_date,
            data.end_date
        )

    else:
        rows = get_expenses()

    expenses = [
        ExpenseRecord(
            id=row[0],
            amount=row[1],
            category=row[2],
            description=row[3],
            date=row[4],
            currency=row[5]
        )
        for row in rows
    ]

    total = sum(expense.amount for expense in expenses)

    return QueryExpensesOutput(
        expenses=expenses,
        total=total
    )