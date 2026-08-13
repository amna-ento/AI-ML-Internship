import os
import time

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


MODEL = "openai/gpt-oss-20b"
TEMPERATURE = 0
MAX_RETRIES = 3


api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment.")

client = Groq(api_key=api_key)


def generate_response(prompt: str) -> str:
    """
    Send a prompt to the LLM and return the generated response.
    Retries transient failures up to MAX_RETRIES times.
    """

    for attempt in range(1, MAX_RETRIES + 1):

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=TEMPERATURE
            )

            return response.choices[0].message.content

        except Exception as error:

            if attempt == MAX_RETRIES:
                raise RuntimeError(
                    f"LLM request failed after {MAX_RETRIES} attempts: {error}"
                )

            time.sleep(2)
            
            