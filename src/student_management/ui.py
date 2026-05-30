"""User interface — all print/input calls live here."""
from prettytable import PrettyTable
from student_management.models import Student, Exam
from student_management.exceptions import AppError, ValidationError, NotFoundError, DuplicateError


def handle_error(error: AppError) -> None:
    """Display user-friendly error messages."""
    if isinstance(error, ValidationError):
        print(f"Validation Error: {error}")
    elif isinstance(error, NotFoundError):
        print(f"Not Found: {error}")
    elif isinstance(error, DuplicateError):
        print(f"Duplicate: {error}")
    else:
        print(f"Error: {error}")


class Menu:
    """Main menu display and input."""

    @staticmethod
    def display() -> None:
        """Display the main menu."""
        print("\n" + "=" * 60)
        print("       STUDENT MANAGEMENT SYSTEM")
        print("=" * 60)
        print("  1. Add Student")
        print("  2. Display All Students")
        print("  3. Update Student")
        print("  4. Delete Student")
        print("  5. Add Exam Record")
        print("  6. Display All Exam Records")
        print("  7. Update Exam Record")
        print("  8. Delete Exam Record")
        print("  9. Exit")
        print("=" * 60)

    @staticmethod
    def get_choice() -> int:
        """Get validated menu choice (1-9)."""
        while True:
            try:
                choice = int(input("Enter your choice (1-9): "))
                if 1 <= choice <= 9:
                    return choice
                print("Please enter a number between 1 and 9.")
            except ValueError:
                print("Invalid input. Please enter a number.")


class StudentUI:
    """Student-related UI operations."""

    @staticmethod
    def get_student_input() -> Student:
        """Get student details from user input."""
        while True:
            try:
                roll_no = int(input("Enter Roll No: "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        name = input("Enter Name: ")
        father_name = input("Enter Father's Name: ")
        mother_name = input("Enter Mother's Name: ")
        address = input("Enter Address: ")
        phone_no = input("Enter Phone No: ")
        email = input("Enter Email: ")

        return Student(
            roll_no=roll_no, name=name, father_name=father_name,
            mother_name=mother_name, address=address, phone_no=phone_no, email=email,
        )

    @staticmethod
    def get_roll_no_input() -> int:
        """Get roll number from user input."""
        while True:
            try:
                return int(input("Enter Roll No: "))
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    @staticmethod
    def display_students(students: list[Student]) -> None:
        """Display students in a formatted table."""
        if not students:
            print("No student records found.")
            return
        table = PrettyTable()
        table.field_names = ["Roll No", "Name", "Father's Name", "Mother's Name", "Address", "Phone No", "Email"]
        for s in students:
            table.add_row([s.roll_no, s.name, s.father_name, s.mother_name, s.address, s.phone_no, s.email])
        print(table)


class ExamUI:
    """Exam-related UI operations."""

    @staticmethod
    def get_exam_input() -> Exam:
        """Get exam details from user input."""
        while True:
            try:
                roll_no = int(input("Enter Roll No: "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        name = input("Enter Name: ")

        while True:
            try:
                class_ = int(input("Enter Class: "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        section = input("Enter Section: ")

        while True:
            try:
                total_marks = int(input("Enter Total Marks: "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        while True:
            try:
                percentage = float(input("Enter Percentage: "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        grade = input("Enter Grade (A/B/C/D/F): ")

        return Exam(roll_no=roll_no, name=name, class_=class_, section=section,
                    total_marks=total_marks, percentage=percentage, grade=grade)

    @staticmethod
    def get_roll_no_input() -> int:
        """Get roll number from user input."""
        while True:
            try:
                return int(input("Enter Roll No: "))
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    @staticmethod
    def display_exams(exams: list[Exam]) -> None:
        """Display exams in a formatted table."""
        if not exams:
            print("No examination records found.")
            return
        table = PrettyTable()
        table.field_names = ["Roll No", "Name", "Class", "Section", "Total Marks", "Percentage", "Grade"]
        for e in exams:
            table.add_row([e.roll_no, e.name, e.class_, e.section, e.total_marks, e.percentage, e.grade])
        print(table)
