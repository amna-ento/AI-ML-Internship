from pydantic import ValidationError
from src.models import JobInformation


try:
    job = JobInformation(
        job_title="Python Developer",
        experience_years=9,
        skills=["FastAPI", "PostgreSQL"],
        work_type="Remote"
    )

    print("Valid data:")
    print(job)

except ValidationError as e:
    print("Validation failed!")
    print(e)