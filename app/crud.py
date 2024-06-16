from statistics import mean, median, stdev
from typing import Dict
from app.models import Student, Statistics

students_db: Dict[int, Student] = {}

def create_student(student_id: int, student: Student):
    students_db[student_id] = student
    return student

def get_student(student_id: int):
    return students_db.get(student_id)

def get_students_by_subject(subject: str):
    return sorted(
        [(student.name, student.grades[subject]) for student in students_db.values() if subject in student.grades],
        key=lambda x: x[1] #Order by 2nd index (student grade)
    )

def calculate_statistics(subject: str) -> Statistics:
    grades = [student.grades[subject] for student in students_db.values() if subject in student.grades]

    if not grades:
        return
    elif len(grades) == 1:
        return

    average = round(mean(grades), 1)
    median_score = round(median(grades), 1)
    std_dev = round(stdev(grades), 1)

    return Statistics(average = average, median = median_score, standard_deviation = std_dev)

def students_below_average(threshold_grade: float = 6):
    students_below_average = []

    for student in students_db.values():
        low_grade_subjects = {subject: grade for subject, grade in student.grades.items() if grade < threshold_grade}
        if low_grade_subjects:
            student_with_low_grades = Student(id=student.id, name=student.name, grades=low_grade_subjects)
            students_below_average.append(student_with_low_grades)
    return students_below_average
