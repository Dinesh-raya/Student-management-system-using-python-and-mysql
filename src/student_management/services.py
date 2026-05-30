"""Service layer — business logic and validation."""
import re
from student_management.models import Student, Exam
from student_management.repositories import StudentRepository, ExamRepository
from student_management.exceptions import ValidationError


class StudentService:
    """Business logic for student operations."""

    def __init__(self, repo: StudentRepository) -> None:
        self.repo = repo

    def _validate_student(self, student: Student) -> None:
        """Validate student data. Raises ValidationError on failure."""
        if not student.name.strip():
            raise ValidationError("Name is required")
        if not student.father_name.strip():
            raise ValidationError("Father's name is required")
        if not student.mother_name.strip():
            raise ValidationError("Mother's name is required")
        if student.phone_no and not re.match(r"^\d{10,15}$", student.phone_no):
            raise ValidationError("Phone number must be 10-15 digits")
        if student.email and not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", student.email):
            raise ValidationError("Invalid email format")

    def create_student(self, student: Student) -> Student:
        """Create a new student after validation."""
        self._validate_student(student)
        self.repo.create(student)
        return student

    def get_student(self, roll_no: int) -> Student:
        """Get a student by roll number."""
        return self.repo.get_by_roll_no(roll_no)

    def list_students(self) -> list[Student]:
        """Get all students."""
        return self.repo.get_all()

    def update_student(self, student: Student) -> Student:
        """Update an existing student after validation."""
        self._validate_student(student)
        self.repo.update(student)
        return student

    def delete_student(self, roll_no: int) -> None:
        """Delete a student by roll number."""
        self.repo.delete(roll_no)


class ExamService:
    """Business logic for exam operations."""

    def __init__(self, repo: ExamRepository) -> None:
        self.repo = repo
