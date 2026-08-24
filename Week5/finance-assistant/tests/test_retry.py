from tenacity import retry, stop_after_attempt, wait_exponential


attempts = 0


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(
        multiplier=1,
        min=1,
        max=4
    )
)
def fake_request():

    global attempts

    attempts += 1

    print(f"Attempt {attempts}")

    if attempts < 3:
        raise Exception("Temporary failure")

    return "Success"


result = fake_request()

print("Result:", result)