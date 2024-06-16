from pydantic import BaseModel
from typing import Dict

class StudentCreate(BaseModel):
    name: str
    grades: Dict[str, float]