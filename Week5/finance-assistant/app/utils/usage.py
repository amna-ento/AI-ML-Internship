from datetime import datetime
import os


# Model pricing per 1 million tokens
# Keep this separate so pricing can be updated easily.
MODEL_PRICING = {
    "openai/gpt-oss-20b": {
        "input": 0.075,
        "output": 0.30
    }
}


def calculate_cost(
    model,
    prompt_tokens,
    completion_tokens
):

    pricing = MODEL_PRICING.get(model)

    if not pricing:
        return 0.0

    input_cost = (
        prompt_tokens / 1_000_000
    ) * pricing["input"]

    output_cost = (
        completion_tokens / 1_000_000
    ) * pricing["output"]

    return input_cost + output_cost


def log_usage(
    model,
    usage
):

    prompt_tokens = usage.prompt_tokens
    completion_tokens = usage.completion_tokens
    total_tokens = usage.total_tokens

    cost = calculate_cost(
        model,
        prompt_tokens,
        completion_tokens
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    os.makedirs("logs", exist_ok=True)

    with open(
        "logs/usage.log",
        "a"
    ) as file:

        file.write(
            f"{timestamp} | "
            f"model={model} | "
            f"prompt_tokens={prompt_tokens} | "
            f"completion_tokens={completion_tokens} | "
            f"total_tokens={total_tokens} | "
            f"estimated_cost=${cost:.8f}\n"
        )

    return cost