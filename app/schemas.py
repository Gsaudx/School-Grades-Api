from pydantic import BaseModel
from typing import Dict

class StudentCreate(BaseModel):
    name: str
    grades: Dict[str, float]

class Student(BaseModel):
    id: int
    name: str
    grades: Dict[str, float]

    class Config:
        orm_mode = True