from pydantic import BaseModel, validator
from typing import Dict

class Student(BaseModel):
    id: int
    name: str
    grades: Dict[str, float]

    @validator('grades', pre=True)
    def round_grades(cls, grades):
        return {subject: round(grade, 1) for subject, grade in grades.items()}

    def dict(self, **kwargs):
        return super().dict(**kwargs)
