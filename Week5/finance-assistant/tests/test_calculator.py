from app.schemas.calculator import CalculateInput
from app.tools.calculator import calculate


result = calculate(
    CalculateInput(
        expression="1000 / 4"
    )
)

print("Result:", result)