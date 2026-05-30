"""Tests for UI module."""
import pytest
from unittest.mock import patch, MagicMock
from student_management.ui import Menu, StudentUI, ExamUI, handle_error
from student_management.models import Student, Exam
from student_management.exceptions import ValidationError, NotFoundError, DuplicateError


class TestMenu:
    """Test Menu display and input."""

    @patch("builtins.input", return_value="1")
    def test_get_choice_valid(self, mock_input):
        choice = Menu.get_choice()
        assert choice == 1

    @patch("builtins.input", side_effect=["abc", "1"])
    def test_get_choice_invalid_then_valid(self, mock_input):
        choice = Menu.get_choice()
        assert choice == 1

    @patch("builtins.input", side_effect=["0", "10", "5"])
    def test_get_choice_out_of_range_then_valid(self, mock_input):
        choice = Menu.get_choice()
        assert choice == 5


class TestStudentUI:
    """Test StudentUI input handling."""

    @patch("builtins.input", side_effect=["1", "John", "James", "Jane", "123 Main St", "1234567890", "john@test.com"])
    def test_add_student_inputs(self, mock_input):
        student = StudentUI.get_student_input()
        assert student.roll_no == 1
        assert student.name == "John"
        assert student.father_name == "James"

    @patch("builtins.input", side_effect=["abc", "1", "John", "James", "Jane", "123 Main St", "1234567890", "john@test.com"])
    def test_add_student_invalid_roll_no(self, mock_input):
        student = StudentUI.get_student_input()
        assert student.roll_no == 1


class TestExamUI:
    """Test ExamUI input handling."""

    @patch("builtins.input", side_effect=["1", "John", "10", "A", "500", "85.5", "A"])
    def test_add_exam_inputs(self, mock_input):
        exam = ExamUI.get_exam_input()
        assert exam.roll_no == 1
        assert exam.name == "John"
        assert exam.class_ == 10
        assert exam.percentage == 85.5


class TestHandleError:
    """Test error display handling."""

    @patch("builtins.print")
    def test_handle_validation_error(self, mock_print):
        handle_error(ValidationError("Invalid input"))
        mock_print.assert_called()
        output = mock_print.call_args[0][0]
        assert "Invalid input" in output

    @patch("builtins.print")
    def test_handle_not_found_error(self, mock_print):
        handle_error(NotFoundError("Not found"))
        mock_print.assert_called()
        output = mock_print.call_args[0][0]
        assert "Not found" in output

    @patch("builtins.print")
    def test_handle_duplicate_error(self, mock_print):
        handle_error(DuplicateError("Already exists"))
        mock_print.assert_called()
        output = mock_print.call_args[0][0]
        assert "Already exists" in output
