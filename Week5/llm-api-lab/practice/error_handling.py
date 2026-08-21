import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

try:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": "Hello"
            }
        ]
    )

    print(response.choices[0].message.content)

except Exception as e:
    print("Exception type:", type(e).__name__)
    print("Status code:", e.status_code)
    print("Error message:", str(e))