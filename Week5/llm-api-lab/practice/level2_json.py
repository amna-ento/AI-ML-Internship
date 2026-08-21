import os
import json

from dotenv import load_dotenv
from groq import Groq
from pydantic import ValidationError

from src.models import JobInformation


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

job_description = """
Python Developer needed with 2+ years of experience.
Must know FastAPI and PostgreSQL.
Remote position.
"""

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",

    response_format={
        "type": "json_object"
    },

    messages=[
        {
            "role": "system",
            "content": """
Extract job information from the job description.

Return a JSON object with:
job_title
experience_years
skills
work_type
"""
        },
        {
            "role": "user",
            "content": job_description
        }
    ]
)

llm_response = response.choices[0].message.content

print("LLM response:")
print(llm_response)

try:
    data = json.loads(llm_response)

    job = JobInformation(**data)

    print("\nValid JobInformation:")
    print(job)

except json.JSONDecodeError:
    print("\nInvalid JSON.")

except ValidationError as e:
    print("\nPydantic validation failed:")
    print(e)