"""Seed data for demo purposes."""
from student_management.models import Student, Exam
from student_management.services import StudentService, ExamService


STUDENTS = [
    Student(roll_no=1, name="Aarav Sharma", father_name="Rajesh Sharma", mother_name="Priya Sharma", address="12 MG Road, Delhi", phone_no="9876543210", email="aarav@school.edu"),
    Student(roll_no=2, name="Ananya Patel", father_name="Vikram Patel", mother_name="Meena Patel", address="45 Park Street, Mumbai", phone_no="9876543211", email="ananya@school.edu"),
    Student(roll_no=3, name="Rohan Gupta", father_name="Sunil Gupta", mother_name="Neha Gupta", address="78 Lake View, Bangalore", phone_no="9876543212", email="rohan@school.edu"),
    Student(roll_no=4, name="Isha Singh", father_name="Manoj Singh", mother_name="Kavita Singh", address="90 Hill Road, Chennai", phone_no="9876543213", email="isha@school.edu"),
    Student(roll_no=5, name="Arjun Reddy", father_name="Krishna Reddy", mother_name="Lakshmi Reddy", address="23 Garden City, Hyderabad", phone_no="9876543214", email="arjun@school.edu"),
    Student(roll_no=6, name="Priya Nair", father_name="Raman Nair", mother_name="Sushma Nair", address="56 Beach Road, Kochi", phone_no="9876543215", email="priya@school.edu"),
    Student(roll_no=7, name="Vivek Kumar", father_name="Ashok Kumar", mother_name="Sunita Kumar", address="34 Station Road, Kolkata", phone_no="9876543216", email="vivek@school.edu"),
    Student(roll_no=8, name="Meera Joshi", father_name="Deepak Joshi", mother_name="Asha Joshi", address="67 Civil Lines, Pune", phone_no="9876543217", email="meera@school.edu"),
    Student(roll_no=9, name="Aditya Verma", father_name="Rakesh Verma", mother_name="Pooja Verma", address="89 Cantonment, Lucknow", phone_no="9876543218", email="aditya@school.edu"),
    Student(roll_no=10, name="Sneha Iyer", father_name="Ganesh Iyer", mother_name="Radha Iyer", address="11 Temple Street, Mysore", phone_no="9876543219", email="sneha@school.edu"),
]

EXAMS = [
    Exam(roll_no=1, name="Aarav Sharma", class_=10, section="A", total_marks=480, percentage=96.0, grade="A"),
    Exam(roll_no=2, name="Ananya Patel", class_=10, section="A", total_marks=450, percentage=90.0, grade="A"),
    Exam(roll_no=3, name="Rohan Gupta", class_=10, section="B", total_marks=410, percentage=82.0, grade="A"),
    Exam(roll_no=4, name="Isha Singh", class_=10, section="A", total_marks=380, percentage=76.0, grade="B"),
    Exam(roll_no=5, name="Arjun Reddy", class_=10, section="B", total_marks=350, percentage=70.0, grade="B"),
    Exam(roll_no=6, name="Priya Nair", class_=9, section="A", total_marks=420, percentage=84.0, grade="A"),
    Exam(roll_no=7, name="Vivek Kumar", class_=9, section="A", total_marks=300, percentage=60.0, grade="C"),
    Exam(roll_no=8, name="Meera Joshi", class_=9, section="B", total_marks=460, percentage=92.0, grade="A"),
    Exam(roll_no=9, name="Aditya Verma", class_=9, section="B", total_marks=280, percentage=56.0, grade="D"),
    Exam(roll_no=10, name="Sneha Iyer", class_=9, section="A", total_marks=390, percentage=78.0, grade="B"),
]


def seed_database(student_service: StudentService, exam_service: ExamService) -> int:
    """Seed database with sample data. Returns count of records added.

    Skips records that already exist (by roll_no).
    """
    count = 0
    for student in STUDENTS:
        try:
            student_service.create_student(student)
            count += 1
        except Exception:
            pass  # Already exists, skip

    for exam in EXAMS:
        try:
            exam_service.create_exam(exam)
            count += 1
        except Exception:
            pass  # Already exists, skip

    return count
