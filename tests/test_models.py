"""Tests for data models."""
import pytest
from dataclasses import fields
from student_management.models import Student, Exam


class TestStudent:
    """Test Student dataclass."""

    def test_create_empty_student(self):
        student = Student()
        assert student.roll_no is None
        assert student.name == ""
        assert student.father_name == ""
        assert student.mother_name == ""
        assert student.address == ""
        assert student.phone_no == ""
        assert student.email == ""

    def test_create_student_with_values(self):
        student = Student(
            roll_no=1,
            name="John",
            father_name="James",
            mother_name="Jane",
            address="123 Main St",
            phone_no="1234567890",
            email="john@example.com",
        )
        assert student.roll_no == 1
        assert student.name == "John"
        assert student.father_name == "James"
        assert student.mother_name == "Jane"
        assert student.address == "123 Main St"
        assert student.phone_no == "1234567890"
        assert student.email == "john@example.com"

    def test_student_fields_count(self):
        assert len(fields(Student)) == 7


class TestExam:
    """Test Exam dataclass."""

    def test_create_empty_exam(self):
        exam = Exam()
        assert exam.id is None
        assert exam.roll_no == 0
        assert exam.name == ""
        assert exam.class_ == 0
        assert exam.section == ""
        assert exam.total_marks == 0
        assert exam.percentage == 0.0
        assert exam.grade == ""

    def test_create_exam_with_values(self):
        exam = Exam(
            id=1,
            roll_no=1,
            name="John",
            class_=10,
            section="A",
            total_marks=500,
            percentage=85.5,
            grade="A",
        )
        assert exam.id == 1
        assert exam.roll_no == 1
        assert exam.name == "John"
        assert exam.class_ == 10
        assert exam.section == "A"
        assert exam.total_marks == 500
        assert exam.percentage == 85.5
        assert exam.grade == "A"

    def test_exam_fields_count(self):
        assert len(fields(Exam)) == 8

    def test_exam_class_underscore_field(self):
        """Verify class_ is used instead of 'class' (reserved word)."""
        exam = Exam(class_=10)
        assert exam.class_ == 10
