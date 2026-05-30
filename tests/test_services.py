"""Tests for service layer."""
import pytest
from unittest.mock import MagicMock
from student_management.services import StudentService, ExamService
from student_management.models import Student, Exam
from student_management.exceptions import ValidationError


class TestStudentService:
    """Test StudentService business logic."""

    @pytest.fixture
    def mock_repo(self):
        return MagicMock()

    @pytest.fixture
    def service(self, mock_repo):
        return StudentService(mock_repo)

    def test_create_valid_student(self, service, mock_repo):
        student = Student(
            roll_no=1, name="John", father_name="James", mother_name="Jane",
            address="123 Main St", phone_no="1234567890", email="john@example.com",
        )
        result = service.create_student(student)
        mock_repo.create.assert_called_once_with(student)
        assert result == student

    def test_create_student_empty_name_raises(self, service):
        student = Student(roll_no=1, name="", father_name="James", mother_name="Jane")
        with pytest.raises(ValidationError, match="Name is required"):
            service.create_student(student)

    def test_create_student_empty_father_name_raises(self, service):
        student = Student(roll_no=1, name="John", father_name="", mother_name="Jane")
        with pytest.raises(ValidationError, match="Father's name is required"):
            service.create_student(student)

    def test_create_student_empty_mother_name_raises(self, service):
        student = Student(roll_no=1, name="John", father_name="James", mother_name="")
        with pytest.raises(ValidationError, match="Mother's name is required"):
            service.create_student(student)

    def test_create_student_empty_phone_raises(self, service):
        student = Student(
            roll_no=1, name="John", father_name="James", mother_name="Jane", phone_no=""
        )
        with pytest.raises(ValidationError, match="Phone number is required"):
            service.create_student(student)

    def test_create_student_invalid_phone_raises(self, service):
        student = Student(
            roll_no=1, name="John", father_name="James", mother_name="Jane", phone_no="123"
        )
        with pytest.raises(ValidationError, match="Phone number must be 10-15 digits"):
            service.create_student(student)

    def test_create_student_invalid_email_raises(self, service):
        student = Student(
            roll_no=1, name="John", father_name="James", mother_name="Jane",
            phone_no="1234567890", email="not-an-email"
        )
        with pytest.raises(ValidationError, match="Invalid email format"):
            service.create_student(student)

    def test_create_student_no_email_ok(self, service, mock_repo):
        student = Student(
            roll_no=1, name="John", father_name="James", mother_name="Jane",
            phone_no="1234567890", email=""
        )
        service.create_student(student)
        mock_repo.create.assert_called_once()

    def test_get_student(self, service, mock_repo):
        expected = Student(roll_no=1, name="John")
        mock_repo.get_by_roll_no.return_value = expected
        result = service.get_student(1)
        assert result == expected

    def test_list_students(self, service, mock_repo):
        mock_repo.get_all.return_value = [Student(roll_no=1), Student(roll_no=2)]
        result = service.list_students()
        assert len(result) == 2

    def test_update_valid_student(self, service, mock_repo):
        student = Student(
            roll_no=1, name="John", father_name="James", mother_name="Jane",
            address="123 Main St", phone_no="1234567890", email="john@example.com",
        )
        result = service.update_student(student)
        mock_repo.update.assert_called_once_with(student)
        assert result == student

    def test_update_student_empty_name_raises(self, service):
        student = Student(roll_no=1, name="", father_name="James", mother_name="Jane")
        with pytest.raises(ValidationError, match="Name is required"):
            service.update_student(student)

    def test_delete_student(self, service, mock_repo):
        service.delete_student(1)
        mock_repo.delete.assert_called_once_with(1)


class TestExamService:
    """Test ExamService business logic."""

    @pytest.fixture
    def mock_repo(self):
        return MagicMock()

    @pytest.fixture
    def service(self, mock_repo):
        return ExamService(mock_repo)

    def test_create_valid_exam(self, service, mock_repo):
        exam = Exam(
            roll_no=1, name="John", class_=10, section="A",
            total_marks=500, percentage=85.5, grade="A"
        )
        service.create_exam(exam)
        mock_repo.create.assert_called_once_with(exam)

    def test_create_exam_invalid_class_raises(self, service):
        exam = Exam(roll_no=1, name="John", class_=0, section="A",
                    total_marks=500, percentage=85.5, grade="A")
        with pytest.raises(ValidationError, match="Class must be a positive integer"):
            service.create_exam(exam)

    def test_create_exam_empty_section_raises(self, service):
        exam = Exam(roll_no=1, name="John", class_=10, section="",
                    total_marks=500, percentage=85.5, grade="A")
        with pytest.raises(ValidationError, match="Section is required"):
            service.create_exam(exam)

    def test_create_exam_negative_marks_raises(self, service):
        exam = Exam(roll_no=1, name="John", class_=10, section="A",
                    total_marks=-1, percentage=85.5, grade="A")
        with pytest.raises(ValidationError, match="Total marks must be positive"):
            service.create_exam(exam)

    def test_create_exam_invalid_percentage_raises(self, service):
        exam = Exam(roll_no=1, name="John", class_=10, section="A",
                    total_marks=500, percentage=101, grade="A")
        with pytest.raises(ValidationError, match="Percentage must be between 0 and 100"):
            service.create_exam(exam)

    def test_create_exam_invalid_grade_raises(self, service):
        exam = Exam(roll_no=1, name="John", class_=10, section="A",
                    total_marks=500, percentage=85.5, grade="Z")
        with pytest.raises(ValidationError, match="Grade must be one of"):
            service.create_exam(exam)

    def test_get_exam(self, service, mock_repo):
        expected = Exam(roll_no=1, name="John")
        mock_repo.get_by_roll_no.return_value = expected
        result = service.get_exam(1)
        assert result == expected

    def test_list_exams(self, service, mock_repo):
        mock_repo.get_all.return_value = [Exam(id=1), Exam(id=2)]
        result = service.list_exams()
        assert len(result) == 2

    def test_update_valid_exam(self, service, mock_repo):
        exam = Exam(
            roll_no=1, name="John", class_=10, section="A",
            total_marks=500, percentage=85.5, grade="A"
        )
        result = service.update_exam(exam)
        mock_repo.update.assert_called_once_with(exam)
        assert result == exam

    def test_update_exam_invalid_grade_raises(self, service):
        exam = Exam(roll_no=1, name="John", class_=10, section="A",
                    total_marks=500, percentage=85.5, grade="Z")
        with pytest.raises(ValidationError, match="Grade must be one of"):
            service.update_exam(exam)

    def test_delete_exam(self, service, mock_repo):
        service.delete_exam(1)
        mock_repo.delete.assert_called_once_with(1)
