def handle_error(error):

    error_name = type(error).__name__

    if error_name == "RateLimitError":

        return (
            "I'm temporarily rate limited. "
            "Please try again in a moment."
        )

    if error_name == "APITimeoutError":

        return (
            "The request timed out. "
            "Please try again."
        )

    if error_name == "APIConnectionError":

        return (
            "I couldn't connect to the AI service. "
            "Please check your internet connection and try again."
        )

    return (
        "Something went wrong while processing "
        "your request. Please try again."
    )