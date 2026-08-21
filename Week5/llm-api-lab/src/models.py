from pydantic import BaseModel


class JobInformation(BaseModel):
    job_title: str
    experience_years: int
    skills: list[str]
    work_type: str