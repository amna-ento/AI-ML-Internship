from app.utils.errors import handle_error


class RateLimitError(Exception):
    pass


class APITimeoutError(Exception):
    pass


class APIConnectionError(Exception):
    pass


errors = [
    RateLimitError("Rate limit reached"),
    APITimeoutError("Request timed out"),
    APIConnectionError("Connection failed"),
    ValueError("Unknown error")
]


for error in errors:

    print(
        type(error).__name__,
        "→",
        handle_error(error)
    )