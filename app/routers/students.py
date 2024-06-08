from fastapi import APIRouter, HTTPException
from app.models import Student
from app.crud import create_student, get_student, get_students_by_subject, students_db
from app.schemas import StudentCreate, Student as StudentSchema

router = APIRouter()

@router.post("/students/", response_model = StudentSchema)
def add_student(student: StudentCreate):
    student_id = max(students_db.keys()) + 1 if students_db else 1
    new_student = Student(
        id = student_id,
        name = student.name,
        grades = student.grades
    )

    for materia, nota in student.grades.items():
        if nota < 0 or nota > 10:
            raise HTTPException(
                status_code = 422,
                detail = "Grades must range from 0 to 10"
            )

    create_student(student_id, new_student)
    return new_student

@router.get("/students/{student_id}", response_model = StudentSchema)
def read_student(student_id: int):
    student = get_student(student_id)
    if not student:
        raise HTTPException(
                status_code = 404,
                detail = "Student not found"
            )
    return student

@router.get("/grades/{subject}")
def read_grades(subject: str):
    student = get_students_by_subject(subject)
    if not student:
        raise HTTPException(
            status_code = 404,
            detail = "There are no students with that subject in the database"
        )
    return student
