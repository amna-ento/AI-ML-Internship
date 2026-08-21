from src.retry import retry_api_call


class TemporaryError(Exception):
    pass


attempt_count = 0


def fake_api_call():

    global attempt_count

    attempt_count += 1

    if attempt_count < 3:
        raise TemporaryError("Temporary failure")

    return "Success!"


try:
    result = retry_api_call(
        fake_api_call,
        retryable_exceptions=(TemporaryError,),
        max_attempts=3
    )

    print("Result:", result)

except Exception as e:
    print("Final error:", e)