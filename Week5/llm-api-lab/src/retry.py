import time


def retry_api_call(api_call, retryable_exceptions, max_attempts=3):

    for attempt in range(1, max_attempts + 1):

        try:
            print(f"Attempt {attempt}")
            return api_call()

        except retryable_exceptions as e:

            if attempt == max_attempts:
                print("Maximum attempts reached.")
                raise e

            wait_time = 2 ** (attempt - 1)

            print(f"Temporary failure: {type(e).__name__}")
            print(f"Waiting {wait_time} seconds...")

            time.sleep(wait_time)