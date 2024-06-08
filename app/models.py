from pydantic import BaseModel
from typing import Dict

class Student(BaseModel):
    id: int
    name: str
    grades: Dict[str, float]

    def dict(self, **kwargs):
        return super().dict(**kwargs)
