from typing import Dict
from app.models import Student

students_db: Dict[int, Student] = {}

def create_student(student_id: int, student: Student):
    students_db[student_id] = student
    return student

def get_student(student_id: int):
    return students_db.get(student_id)

def get_students_by_grade(subject: str):
    return sorted(
        [(student.name, student.grades[subject]) for student in students_db.values() if subject in student.grades],
        key=lambda x: x[1]
    )