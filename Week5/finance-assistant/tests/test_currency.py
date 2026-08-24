from app.schemas.currency import ConvertCurrencyInput
from app.tools.currency import convert_currency


result = convert_currency(
    ConvertCurrencyInput(
        amount=100,
        from_currency="USD",
        to_currency="PKR"
    )
)

print("Currency conversion:")
print(result)