"""Entry point for Student Management System."""
import sys
from student_management.config import get_config
from student_management.db import Database
from student_management.repositories import StudentRepository, ExamRepository
from student_management.services import StudentService, ExamService
from student_management.ui import Menu, StudentUI, ExamUI, handle_error
from student_management.exceptions import AppError


def main() -> None:
    """Run the Student Management System."""
    config = get_config()

    db = Database(config)
    try:
        db.initialize()
    except AppError as e:
        print(f"Failed to connect to database: {e}")
        sys.exit(1)

    student_repo = StudentRepository(db)
    exam_repo = ExamRepository(db)
    student_service = StudentService(student_repo)
    exam_service = ExamService(exam_repo)

    print("Connected to database successfully!")

    while True:
        Menu.display()
        choice = Menu.get_choice()

        try:
            if choice == 1:
                student = StudentUI.get_student_input()
                student_service.create_student(student)
                print("Student added successfully!")

            elif choice == 2:
                students = student_service.list_students()
                StudentUI.display_students(students)

            elif choice == 3:
                roll_no = StudentUI.get_roll_no_input()
                student = student_service.get_student(roll_no)
                print(f"Current details: {student.name}, {student.father_name}, {student.mother_name}")
                updated = StudentUI.get_student_input()
                updated.roll_no = roll_no
                student_service.update_student(updated)
                print("Student updated successfully!")

            elif choice == 4:
                roll_no = StudentUI.get_roll_no_input()
                student_service.delete_student(roll_no)
                print("Student deleted successfully!")

            elif choice == 5:
                exam = ExamUI.get_exam_input()
                exam_service.create_exam(exam)
                print("Exam record added successfully!")

            elif choice == 6:
                exams = exam_service.list_exams()
                ExamUI.display_exams(exams)

            elif choice == 7:
                roll_no = ExamUI.get_roll_no_input()
                exam = exam_service.get_exam(roll_no)
                print(f"Current details: {exam.name}, Class {exam.class_}, Section {exam.section}")
                updated = ExamUI.get_exam_input()
                updated.roll_no = roll_no
                exam_service.update_exam(updated)
                print("Exam record updated successfully!")

            elif choice == 8:
                roll_no = ExamUI.get_roll_no_input()
                exam_service.delete_exam(roll_no)
                print("Exam record deleted successfully!")

            elif choice == 9:
                print("Thank you for using Student Management System!")
                sys.exit(0)

        except AppError as e:
            handle_error(e)


if __name__ == "__main__":
    main()
