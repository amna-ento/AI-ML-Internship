from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

from groq import (
    RateLimitError,
    APITimeoutError,
    APIConnectionError
)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(
        multiplier=1,
        min=1,
        max=4
    ),
    retry=retry_if_exception_type(
        (
            RateLimitError,
            APITimeoutError,
            APIConnectionError
        )
    )
)
def call_groq(client, **kwargs):

    return client.chat.completions.create(
        **kwargs
    )