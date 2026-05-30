"""Tests for custom exception hierarchy."""
import pytest
from student_management.exceptions import (
    AppError,
    DatabaseError,
    ValidationError,
    NotFoundError,
    DuplicateError,
)


class TestExceptionHierarchy:
    """Test that all custom exceptions inherit from AppError."""

    def test_database_error_is_app_error(self):
        assert issubclass(DatabaseError, AppError)

    def test_validation_error_is_app_error(self):
        assert issubclass(ValidationError, AppError)

    def test_not_found_error_is_app_error(self):
        assert issubclass(NotFoundError, AppError)

    def test_duplicate_error_is_app_error(self):
        assert issubclass(DuplicateError, AppError)

    def test_app_error_is_exception(self):
        assert issubclass(AppError, Exception)


class TestExceptionMessages:
    """Test that exceptions carry messages correctly."""

    def test_database_error_message(self):
        err = DatabaseError("Connection failed")
        assert str(err) == "Connection failed"

    def test_validation_error_message(self):
        err = ValidationError("Invalid email")
        assert str(err) == "Invalid email"

    def test_not_found_error_message(self):
        err = NotFoundError("Student not found")
        assert str(err) == "Student not found"

    def test_duplicate_error_message(self):
        err = DuplicateError("Roll number exists")
        assert str(err) == "Roll number exists"
