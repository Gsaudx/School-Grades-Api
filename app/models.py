from pydantic import BaseModel, field_validator
from typing import Dict

class StudentCreate(BaseModel):
    name: str
    grades: Dict[str, float]

class Student(BaseModel):
    id: int
    name: str
    grades: Dict[str, float]

    @field_validator('grades', mode = 'before')
    def round_grades(cls, grades):
        return {subject: round(grade, 1) for subject, grade in grades.items()}

class Statistics(BaseModel):
    average: float
    median: float
    standard_deviation: float
