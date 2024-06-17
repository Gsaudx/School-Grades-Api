from fastapi import APIRouter, HTTPException
from app.models import Student, StudentCreate
from app.crud import create_student, get_student, get_students_by_subject, calculate_statistics, students_below_average, students_db, remove_students_with_no_grades
from typing import Dict

router = APIRouter()

"""
Each one of the below functions work as an endpoint for the API. They're constructed by adding:

@router.post(endpoint, response_model, summary) ---> Defines the route to the endpoint and basically infos to the docs
def endpoint_function ---> The function ran when the endpoint is accessed
"""

"""
The /students/ endpoint needs to receive a http POST method data in the following format:

{
    "name": str,
    "grades": Dict[str, float]
}

If the data is not in the specified format, an error is returned.

Before adding the new record to the "database" (a JSON file), we check the number of keys in students_db, which represents the number of students registered in the system.
If students_db.keys() == 0, then student_id is set to 1. Otherwise, it is set to the highest existing number + 1, 
representing the auto-increment functionality found in some database systems.

After generating the student ID, we create a Student object containing the generated ID, the given name string, and the grades dictionary.
We also validate the given grades to ensure that none of them are less than 0 or greater than 10, as these are not valid grade values.

If all verifications pass, we run the create_student function, passing the created student object as an argument.
"""
@router.post("/students/", response_model = Student, summary = "Add a student to the database")
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

"""
The /students/{student_id} endpoint expects to receive a student ID to return the corresponding record from the database.
Providing an invalid ID returns a "Student not found" error, along with a 404 HTTP status code.

If a valid ID is provided, the response will be a JSON object in the following format:

{
  "id": int,
  "name": str,
  "grades": Dict[str, float]
}
"""
@router.get("/students/{student_id}", response_model = Student, summary = "Get a student by ID")
def read_student(student_id: int):
    student = get_student(student_id)
    if not student:
        raise HTTPException(
                status_code = 404,
                detail = "Student not found"
            )
    return student

"""
The /grades/{subject} endpoint expects to receive an existing subject from the database to return the corresponding grades.
Providing an invalid subject will return a "There are no students with that subject in the database" error, along with a 404 HTTP status code.

If there are grades for the given subject, the response will be a list containing the student name followed by their grade ordered from the lowest to the higest:

[
    [
        str,
        float
    ]
]
"""
@router.get("/grades/{subject}", summary = "Get all grades for a specific subject")
def subject_grades(subject: str):
    student = get_students_by_subject(subject)
    if not student:
        raise HTTPException(
            status_code = 404,
            detail = "There are no students with that subject in the database"
        )
    return student

"""
The /grades/statistics/{subject} endpoint expects to receive an existing subject from the database to return its average, median, and standard deviation.
Providing an invalid subject will return an error, along with a 404 HTTP status code.
Additionally, if there is only one grade available, the same error and HTTP status code will be returned.

However, if there are at least two grades for the given subject, the response will be a JSON object containing the statistics for that subject:

{
  "average": float,
  "median": float,
  "standard_deviation": float
}
"""
@router.get("/grades/statistics/{subject}", summary = "Get average, median an standard deviation of a specific subject")
def subject_statistics(subject: str):
    statistics = calculate_statistics(subject)

    if not statistics:
        raise HTTPException(
            status_code = 404,
            detail = "There are not enough data for that subject in the database, so no statistics can be calculated."
        )
    return statistics

"""
The /grades/below_average/ endpoint does not expect any arguments.
It retrieves every student with at least one grade below the given threshold. By default, this threshold is set to 6. 
The threshold can be changed by giving an argument to the students_below_average() function 

If there are no grades below the threshold, an error is returned along with a 404 HTTP status code.

However, if there is at least one student with a grade below the threshold, a list of these students is returned:

[
  {
    "id": int,
    "name": str,
    "grades": Dict[str, float]
  }
]
"""
@router.get("/grades/below_average/", summary = "Get every student who have at least one subject below the average (by default 6)")
def below_average():
    students = students_below_average() #Threshold grade is 6 by default

    if not students:
        raise HTTPException(
            status_code = 404,
            detail = "There are no students with grades below 6 in the database"
        )
    return students

"""
The /students/remove/no_grades endpoint does not expect any arguments.
It removes every student that has not grades in the system. 

If every student has at least one grade, an error is returned along with a 404 HTTP status code.

However, if there is at least one student without any grade, he'll be removed and a list with his ID is going to be returned:

[
    int
]
"""
@router.delete("/students/remove/no_grades", summary = "Deletes every student with no grades")
async def remove_students_no_grades():
    removed_students = remove_students_with_no_grades()
    
    if not removed_students:
        raise HTTPException(
            status_code = 404,
            detail = "There are no students without grades. Any student has been removed from the database"
        )

    return removed_students
