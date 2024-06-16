from fastapi import APIRouter, HTTPException
from app.models import Student
from app.crud import create_student, get_student, get_students_by_subject, calculate_statistics, students_below_average, students_db
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

    for subject, grade in student.grades.items():
        if grade < 0 or grade > 10:
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
def subject_grades(subject: str):
    student = get_students_by_subject(subject)
    if not student:
        raise HTTPException(
            status_code = 404,
            detail = "There are no students with that subject in the database"
        )
    return student

@router.get("/grades/statistics/{subject}")
def subject_statistics(subject: str):
    average = calculate_statistics(subject)

    if not average:
        raise HTTPException(
            status_code = 404,
            detail = "There are no data for that subject in the database"
        )
    return average

@router.get("/grades/below_average/")
def below_average():
    students = students_below_average() #Threshold grade is 6 by default

    if not students:
        raise HTTPException(
            status_code = 404,
            detail = "There are no students with grades below 6 in the database"
        )
    return students
