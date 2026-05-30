"""Data models for Student and Exam records."""
from dataclasses import dataclass


@dataclass
class Student:
    """Represents a student record."""

    roll_no: int | None = None
    name: str = ""
    father_name: str = ""
    mother_name: str = ""
    address: str = ""
    phone_no: str = ""
    email: str = ""


@dataclass
class Exam:
    """Represents an examination record."""

    id: int | None = None
    roll_no: int = 0
    name: str = ""
    class_: int = 0
    section: str = ""
    total_marks: int = 0
    percentage: float = 0.0
    grade: str = ""
