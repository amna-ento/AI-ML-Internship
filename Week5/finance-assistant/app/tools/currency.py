import requests

from app.schemas.currency import (
    ConvertCurrencyInput,
    ConvertCurrencyOutput
)


def convert_currency(
    data: ConvertCurrencyInput
) -> ConvertCurrencyOutput:

    from_currency = data.from_currency.upper()
    to_currency = data.to_currency.upper()

    url = (
        f"https://api.frankfurter.dev/v2/rate/"
        f"{from_currency}/{to_currency}"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    result = response.json()

    rate = result["rate"]
    converted_amount = data.amount * rate

    return ConvertCurrencyOutput(
        amount=data.amount,
        from_currency=from_currency,
        to_currency=to_currency,
        converted_amount=converted_amount,
        rate=rate
    )