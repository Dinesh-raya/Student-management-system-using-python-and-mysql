"""Tests for repository layer."""
import pytest
from unittest.mock import MagicMock, patch
from student_management.repositories import StudentRepository, ExamRepository
from student_management.models import Student, Exam
from student_management.exceptions import DatabaseError, NotFoundError, DuplicateError


class TestStudentRepository:
    """Test StudentRepository CRUD operations."""

    @pytest.fixture
    def mock_db(self):
        db = MagicMock()
        return db

    @pytest.fixture
    def repo(self, mock_db):
        return StudentRepository(mock_db)

    @pytest.fixture
    def sample_student(self):
        return Student(
            roll_no=1,
            name="John",
            father_name="James",
            mother_name="Jane",
            address="123 Main St",
            phone_no="1234567890",
            email="john@example.com",
        )

    def test_create_student(self, repo, mock_db, sample_student):
        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_db.cursor.return_value.__exit__ = MagicMock(return_value=False)

        # No existing student
        mock_cursor.fetchone.return_value = None

        repo.create(sample_student)
        assert mock_cursor.execute.call_count == 2
        call_args = mock_cursor.execute.call_args_list[1]
        assert "INSERT INTO student" in call_args[0][0]

    def test_create_duplicate_raises(self, repo, mock_db, sample_student):
        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_db.cursor.return_value.__exit__ = MagicMock(return_value=False)

        # Student already exists
        mock_cursor.fetchone.return_value = (1,)

        with pytest.raises(DuplicateError, match="already exists"):
            repo.create(sample_student)

    def test_get_by_roll_no(self, repo, mock_db):
        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_db.cursor.return_value.__exit__ = MagicMock(return_value=False)

        mock_cursor.fetchone.return_value = (
            1, "John", "James", "Jane", "123 Main St", "1234567890", "john@example.com"
        )

        student = repo.get_by_roll_no(1)
        assert student.roll_no == 1
        assert student.name == "John"

    def test_get_by_roll_no_not_found(self, repo, mock_db):
        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_db.cursor.return_value.__exit__ = MagicMock(return_value=False)

        mock_cursor.fetchone.return_value = None

        with pytest.raises(NotFoundError, match="not found"):
            repo.get_by_roll_no(999)

    def test_get_all(self, repo, mock_db):
        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_db.cursor.return_value.__exit__ = MagicMock(return_value=False)

        mock_cursor.fetchall.return_value = [
            (1, "John", "James", "Jane", "123 Main St", "1234567890", "john@example.com"),
            (2, "Jane", "Bob", "Alice", "456 Oak Ave", "0987654321", "jane@example.com"),
        ]

        students = repo.get_all()
        assert len(students) == 2
        assert students[0].name == "John"
        assert students[1].name == "Jane"

    def test_get_all_empty(self, repo, mock_db):
        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_db.cursor.return_value.__exit__ = MagicMock(return_value=False)

        mock_cursor.fetchall.return_value = []

        students = repo.get_all()
        assert len(students) == 0

    def test_update_student(self, repo, mock_db, sample_student):
        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_db.cursor.return_value.__exit__ = MagicMock(return_value=False)

        # Student exists
        mock_cursor.fetchone.return_value = (1,)

        repo.update(sample_student)
        assert mock_cursor.execute.call_count == 2
        call_args = mock_cursor.execute.call_args_list[1]
        assert "UPDATE student" in call_args[0][0]

    def test_update_not_found(self, repo, mock_db, sample_student):
        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_db.cursor.return_value.__exit__ = MagicMock(return_value=False)

        mock_cursor.fetchone.return_value = None

        with pytest.raises(NotFoundError, match="not found"):
            repo.update(sample_student)

    def test_delete_student(self, repo, mock_db):
        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_db.cursor.return_value.__exit__ = MagicMock(return_value=False)

        mock_cursor.fetchone.return_value = (1,)

        repo.delete(1)
        assert mock_cursor.execute.call_count == 2
        call_args = mock_cursor.execute.call_args_list[1]
        assert "DELETE FROM student" in call_args[0][0]

    def test_delete_not_found(self, repo, mock_db):
        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_db.cursor.return_value.__exit__ = MagicMock(return_value=False)

        mock_cursor.fetchone.return_value = None

        with pytest.raises(NotFoundError, match="not found"):
            repo.delete(999)


class TestExamRepository:
    """Test ExamRepository CRUD operations."""

    @pytest.fixture
    def mock_db(self):
        db = MagicMock()
        return db

    @pytest.fixture
    def repo(self, mock_db):
        return ExamRepository(mock_db)

    @pytest.fixture
    def sample_exam(self):
        return Exam(
            roll_no=1,
            name="John",
            class_=10,
            section="A",
            total_marks=500,
            percentage=85.5,
            grade="A",
        )

    def test_create_exam(self, repo, mock_db, sample_exam):
        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_db.cursor.return_value.__exit__ = MagicMock(return_value=False)

        # Student exists, no existing exam
        mock_cursor.fetchone.side_effect = [(1,), None]

        repo.create(sample_exam)
        assert mock_cursor.execute.call_count == 3  # Check student + check exam + insert

    def test_create_exam_student_not_found(self, repo, mock_db, sample_exam):
        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_db.cursor.return_value.__exit__ = MagicMock(return_value=False)

        # Student doesn't exist
        mock_cursor.fetchone.return_value = None

        with pytest.raises(NotFoundError, match="Student.*not found"):
            repo.create(sample_exam)

    def test_create_exam_duplicate(self, repo, mock_db, sample_exam):
        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_db.cursor.return_value.__exit__ = MagicMock(return_value=False)

        # Student exists, exam already exists
        mock_cursor.fetchone.side_effect = [(1,), (1,)]

        with pytest.raises(DuplicateError, match="already exists"):
            repo.create(sample_exam)

    def test_get_by_roll_no(self, repo, mock_db):
        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_db.cursor.return_value.__exit__ = MagicMock(return_value=False)

        mock_cursor.fetchone.return_value = (
            1, 1, "John", 10, "A", 500, 85.5, "A"
        )

        exam = repo.get_by_roll_no(1)
        assert exam.roll_no == 1
        assert exam.name == "John"
        assert exam.percentage == 85.5

    def test_get_by_roll_no_not_found(self, repo, mock_db):
        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_db.cursor.return_value.__exit__ = MagicMock(return_value=False)

        mock_cursor.fetchone.return_value = None

        with pytest.raises(NotFoundError, match="not found"):
            repo.get_by_roll_no(999)

    def test_get_all(self, repo, mock_db):
        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_db.cursor.return_value.__exit__ = MagicMock(return_value=False)

        mock_cursor.fetchall.return_value = [
            (1, 1, "John", 10, "A", 500, 85.5, "A"),
            (2, 2, "Jane", 11, "B", 450, 75.0, "B"),
        ]

        exams = repo.get_all()
        assert len(exams) == 2

    def test_update_exam(self, repo, mock_db, sample_exam):
        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_db.cursor.return_value.__exit__ = MagicMock(return_value=False)

        mock_cursor.fetchone.return_value = (1,)

        repo.update(sample_exam)
        assert mock_cursor.execute.call_count == 2
        call_args = mock_cursor.execute.call_args_list[1]
        assert "UPDATE exam" in call_args[0][0]

    def test_update_not_found(self, repo, mock_db, sample_exam):
        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_db.cursor.return_value.__exit__ = MagicMock(return_value=False)

        mock_cursor.fetchone.return_value = None

        with pytest.raises(NotFoundError, match="not found"):
            repo.update(sample_exam)

    def test_delete_exam(self, repo, mock_db):
        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_db.cursor.return_value.__exit__ = MagicMock(return_value=False)

        mock_cursor.fetchone.return_value = (1,)

        repo.delete(1)
        assert mock_cursor.execute.call_count == 2

    def test_delete_not_found(self, repo, mock_db):
        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_db.cursor.return_value.__exit__ = MagicMock(return_value=False)

        mock_cursor.fetchone.return_value = None

        with pytest.raises(NotFoundError, match="not found"):
            repo.delete(999)
