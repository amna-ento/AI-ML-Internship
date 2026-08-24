from pydantic import BaseModel, Field


class ConvertCurrencyInput(BaseModel):
    amount: float = Field(gt=0)
    from_currency: str = Field(min_length=3, max_length=3)
    to_currency: str = Field(min_length=3, max_length=3)


class ConvertCurrencyOutput(BaseModel):
    amount: float
    from_currency: str
    to_currency: str
    converted_amount: float
    rate: float