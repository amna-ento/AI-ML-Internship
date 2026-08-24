from app.schemas.calculator import CalculateInput, CalculateOutput


def calculate(data: CalculateInput) -> CalculateOutput:
    result = eval(data.expression)

    return CalculateOutput(
        result=float(result)
    )