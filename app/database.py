import json
from typing import Dict
from app.models import Student

FILE_PATH = "students.json"

def load_data() -> Dict[int, Student]:
    try:
        with open(FILE_PATH, "r") as file:
            data = json.load(file)
            return {int(student_id): Student(**student_obj) for student_id, student_obj in data.items()}
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_data(data: Dict[int, Student]):
    with open(FILE_PATH, "w") as file:
        json.dump({student_id: student_obj.dict() for student_id, student_obj in data.items()}, file, indent = 4)
