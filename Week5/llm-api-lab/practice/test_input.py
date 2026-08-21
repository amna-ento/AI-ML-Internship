from pydantic import ValidationError

from src.input_models import JobDescriptionInput


def validate_input(job_description):

    try:
        data = JobDescriptionInput(
            job_description=job_description
        )

        print("Input is valid.")
        return data

    except ValidationError:
        print("Input validation failed.")
        return None
    
    
    
    
print("\n--- Test 1: Valid Input ---")

validate_input(
    """
    Python Developer needed with 2+ years of experience.
    Must know FastAPI and PostgreSQL.
    Remote position.
    """
)    



print("\n--- Test 2: Empty Input ---")

validate_input("")



def validate_input(job_description):

    try:
        data = JobDescriptionInput(
            job_description=job_description
        )

        print("Input is valid.")
        return data

    except ValidationError as e:

        print("Input validation failed:")

        for error in e.errors():
            print(error["msg"])

        return None
    
    
    
print("\n--- Test 3: Extremely Long Input ---")

long_input = "Python Developer " * 200

validate_input(long_input)    