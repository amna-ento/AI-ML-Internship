from pydantic import BaseModel, Field


class AddExpenseInput(BaseModel):
    amount: float = Field(gt=0)
    category: str = Field(min_length=1)
    description: str = Field(min_length=1)
    date: str
    currency: str = Field(min_length=3, max_length=3)


class AddExpenseOutput(BaseModel):
    success: bool
    expense_id: int
    message: str


class QueryExpensesInput(BaseModel):
    category: str | None = None
    start_date: str | None = None
    end_date: str | None = None


class ExpenseRecord(BaseModel):
    id: int
    amount: float
    category: str
    description: str | None
    date: str
    currency: str


class QueryExpensesOutput(BaseModel):
    expenses: list[ExpenseRecord]
    total: float