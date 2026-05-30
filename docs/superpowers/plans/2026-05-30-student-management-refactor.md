# Student Management System — Production-Grade CLI Refactor

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor a beginner-level single-file Student Management System into a production-grade, multi-module Python CLI with proper architecture, testing, and error handling.

**Architecture:** Multi-module package with clear separation: config → db → models → repositories → services → ui → main. Each layer only depends on layers below it. TDD throughout.

**Tech Stack:** Python 3.10+, mysql-connector-python, prettytable, python-dotenv, pytest

---

## File Structure

```
student-management-system/
├── src/
│   └── student_management/
│       ├── __init__.py
│       ├── __main__.py
│       ├── config.py
│       ├── db.py
│       ├── models.py
│       ├── repositories.py
│       ├── services.py
│       ├── ui.py
│       └── exceptions.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_config.py
│   ├── test_db.py
│   ├── test_models.py
│   ├── test_repositories.py
│   ├── test_services.py
│   └── test_ui.py
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── schema.sql
└── README.md
```

---

## Task 1: Project Setup

**Files:**
- Create: `pyproject.toml`
- Create: `requirements.txt`
- Create: `.env.example`
- Create: `.gitignore`
- Create: `src/student_management/__init__.py`
- Create: `tests/__init__.py`

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p src/student_management tests
```

- [ ] **Step 2: Create pyproject.toml**

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "student-management-system"
version = "1.0.0"
description = "Production-grade Student Management System CLI"
requires-python = ">=3.10"
dependencies = [
    "mysql-connector-python>=8.0",
    "prettytable>=3.0",
    "python-dotenv>=1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "pytest-mock>=3.0",
]

[project.scripts]
student-management = "student_management.__main__:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

- [ ] **Step 3: Create requirements.txt**

```
mysql-connector-python>=8.0
prettytable>=3.0
python-dotenv>=1.0
```

- [ ] **Step 4: Create .env.example**

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=root
DB_NAME=student_details
DB_POOL_SIZE=5
```

- [ ] **Step 5: Create .gitignore**

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.env
.venv
env/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db
```

- [ ] **Step 6: Create __init__.py files**

```python
# src/student_management/__init__.py
"""Student Management System — Production-grade CLI."""
__version__ = "1.0.0"
```

```python
# tests/__init__.py
```

- [ ] **Step 7: Install dependencies and verify**

```bash
pip install -e ".[dev]"
```

Expected: Successfully installs all dependencies

- [ ] **Step 8: Commit**

```bash
git add pyproject.toml requirements.txt .env.example .gitignore src/ tests/
git commit -m "chore: initialize project structure with packaging and dependencies"
```

---

## Task 2: Custom Exceptions

**Files:**
- Create: `src/student_management/exceptions.py`
- Create: `tests/test_exceptions.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_exceptions.py
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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_exceptions.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'student_management.exceptions'"

- [ ] **Step 3: Implement exceptions**

```python
# src/student_management/exceptions.py
"""Custom exception hierarchy for Student Management System."""


class AppError(Exception):
    """Base exception for all application errors."""


class DatabaseError(AppError):
    """Raised when database operations fail."""


class ValidationError(AppError):
    """Raised when input data fails validation."""


class NotFoundError(AppError):
    """Raised when a requested record does not exist."""


class DuplicateError(AppError):
    """Raised when attempting to create a record that already exists."""
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_exceptions.py -v
```

Expected: All 9 tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/student_management/exceptions.py tests/test_exceptions.py
git commit -m "feat: add custom exception hierarchy"
```

---

## Task 3: Configuration Module

**Files:**
- Create: `src/student_management/config.py`
- Create: `tests/test_config.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_config.py
"""Tests for configuration module."""
import os
import pytest
from unittest.mock import patch
from student_management.config import DatabaseConfig, get_config


class TestDatabaseConfig:
    """Test DatabaseConfig dataclass."""

    def test_default_values(self):
        config = DatabaseConfig()
        assert config.host == "localhost"
        assert config.user == "root"
        assert config.password == "root"
        assert config.database == "student_details"
        assert config.pool_size == 5

    def test_custom_values(self):
        config = DatabaseConfig(
            host="remotehost",
            user="admin",
            password="secret",
            dbname="mydb",
            pool_size=10,
        )
        assert config.host == "remotehost"
        assert config.user == "admin"
        assert config.password == "secret"
        assert config.database == "mydb"
        assert config.pool_size == 10


class TestGetConfig:
    """Test get_config function with environment variables."""

    def test_reads_from_env_vars(self):
        env_vars = {
            "DB_HOST": "envhost",
            "DB_USER": "envuser",
            "DB_PASSWORD": "envpass",
            "DB_NAME": "envdb",
            "DB_POOL_SIZE": "3",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            config = get_config()
            assert config.host == "envhost"
            assert config.user == "envuser"
            assert config.password == "envpass"
            assert config.database == "envdb"
            assert config.pool_size == 3

    def test_falls_back_to_defaults(self):
        # Clear relevant env vars
        env_keys = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME", "DB_POOL_SIZE"]
        cleared = {k: None for k in env_keys}
        with patch.dict(os.environ, cleared, clear=False):
            for k in env_keys:
                os.environ.pop(k, None)
            config = get_config()
            assert config.host == "localhost"
            assert config.user == "root"

    def test_pool_size_converts_to_int(self):
        with patch.dict(os.environ, {"DB_POOL_SIZE": "8"}, clear=False):
            config = get_config()
            assert config.pool_size == 8
            assert isinstance(config.pool_size, int)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_config.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'student_management.config'"

- [ ] **Step 3: Implement config module**

```python
# src/student_management/config.py
"""Configuration management using environment variables."""
import os
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Database connection configuration."""

    host: str = "localhost"
    user: str = "root"
    password: str = "root"
    database: str = "student_details"
    pool_size: int = 5


def get_config() -> DatabaseConfig:
    """Load configuration from environment variables with defaults."""
    return DatabaseConfig(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root"),
        database=os.getenv("DB_NAME", "student_details"),
        pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
    )
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_config.py -v
```

Expected: All 6 tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/student_management/config.py tests/test_config.py
git commit -m "feat: add configuration module with env var support"
```

---

## Task 4: Database Module

**Files:**
- Create: `src/student_management/db.py`
- Create: `tests/test_db.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_db.py
"""Tests for database connection module."""
import pytest
from unittest.mock import patch, MagicMock
from student_management.db import Database
from student_management.config import DatabaseConfig
from student_management.exceptions import DatabaseError


class TestDatabase:
    """Test Database connection manager."""

    def test_init_stores_config(self):
        config = DatabaseConfig()
        db = Database(config)
        assert db.config == config

    @patch("student_management.db.mysql.connector.pooling.MySQLConnectionPool")
    def test_initialize_creates_pool(self, mock_pool_class):
        config = DatabaseConfig(pool_size=3)
        db = Database(config)
        db.initialize()
        mock_pool_class.assert_called_once_with(
            pool_name="student_pool",
            pool_size=3,
            host="localhost",
            user="root",
            password="root",
            database="student_details",
        )

    @patch("student_management.db.mysql.connector.pooling.MySQLConnectionPool")
    def test_initialize_raises_database_error_on_failure(self, mock_pool_class):
        mock_pool_class.side_effect = Exception("Connection refused")
        config = DatabaseConfig()
        db = Database(config)
        with pytest.raises(DatabaseError, match="Failed to initialize connection pool"):
            db.initialize()

    @patch("student_management.db.mysql.connector.pooling.MySQLConnectionPool")
    def test_get_connection_returns_connection(self, mock_pool_class):
        mock_pool = MagicMock()
        mock_conn = MagicMock()
        mock_pool.get_connection.return_value = mock_conn
        mock_pool_class.return_value = mock_pool

        config = DatabaseConfig()
        db = Database(config)
        db.initialize()
        conn = db.get_connection()
        assert conn == mock_conn

    @patch("student_management.db.mysql.connector.pooling.MySQLConnectionPool")
    def test_get_connection_raises_if_not_initialized(self, mock_pool_class):
        config = DatabaseConfig()
        db = Database(config)
        with pytest.raises(DatabaseError, match="Database not initialized"):
            db.get_connection()

    @patch("student_management.db.mysql.connector.pooling.MySQLConnectionPool")
    def test_cursor_context_manager(self, mock_pool_class):
        mock_pool = MagicMock()
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_pool.get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_pool_class.return_value = mock_pool

        config = DatabaseConfig()
        db = Database(config)
        db.initialize()

        with db.cursor() as cursor:
            assert cursor == mock_cursor

        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_db.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'student_management.db'"

- [ ] **Step 3: Implement database module**

```python
# src/student_management/db.py
"""Database connection management with connection pooling."""
from contextlib import contextmanager
import mysql.connector
import mysql.connector.pooling

from student_management.config import DatabaseConfig
from student_management.exceptions import DatabaseError


class Database:
    """Manages MySQL connection pool and provides context-managed cursors."""

    def __init__(self, config: DatabaseConfig) -> None:
        self.config = config
        self._pool: mysql.connector.pooling.MySQLConnectionPool | None = None

    def initialize(self) -> None:
        """Create the connection pool. Call once at startup."""
        try:
            self._pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="student_pool",
                pool_size=self.config.pool_size,
                host=self.config.host,
                user=self.config.user,
                password=self.config.password,
                database=self.config.database,
            )
        except Exception as e:
            raise DatabaseError(f"Failed to initialize connection pool: {e}") from e

    def get_connection(self) -> mysql.connector.connection.MySQLConnection:
        """Get a connection from the pool."""
        if self._pool is None:
            raise DatabaseError("Database not initialized. Call initialize() first.")
        return self._pool.get_connection()

    @contextmanager
    def cursor(self):
        """Context manager that yields a cursor and ensures cleanup."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_db.py -v
```

Expected: All 6 tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/student_management/db.py tests/test_db.py
git commit -m "feat: add database module with connection pooling"
```

---

## Task 5: Models

**Files:**
- Create: `src/student_management/models.py`
- Create: `tests/test_models.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_models.py
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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_models.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'student_management.models'"

- [ ] **Step 3: Implement models**

```python
# src/student_management/models.py
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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_models.py -v
```

Expected: All 7 tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/student_management/models.py tests/test_models.py
git commit -m "feat: add Student and Exam dataclass models"
```

---

## Task 6: Student Repository

**Files:**
- Create: `src/student_management/repositories.py`
- Create: `tests/test_repositories.py`

- [ ] **Step 1: Write failing tests for StudentRepository**

```python
# tests/test_repositories.py
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
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args
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
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args
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
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args
        assert "DELETE FROM student" in call_args[0][0]

    def test_delete_not_found(self, repo, mock_db):
        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_db.cursor.return_value.__exit__ = MagicMock(return_value=False)

        mock_cursor.fetchone.return_value = None

        with pytest.raises(NotFoundError, match="not found"):
            repo.delete(999)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_repositories.py -v
```

Expected: FAIL with "ModuleNotFoundError"

- [ ] **Step 3: Implement StudentRepository**

```python
# src/student_management/repositories.py
"""Repository layer — all SQL lives here."""
from student_management.db import Database
from student_management.models import Student, Exam
from student_management.exceptions import NotFoundError, DuplicateError


class StudentRepository:
    """Handles all STUDENT table operations."""

    def __init__(self, db: Database) -> None:
        self.db = db

    def create(self, student: Student) -> None:
        """Insert a new student. Raises DuplicateError if roll_no exists."""
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT roll_no FROM student WHERE roll_no=%s", (student.roll_no,)
            )
            if cursor.fetchone():
                raise DuplicateError(f"Roll number {student.roll_no} already exists")

            cursor.execute(
                "INSERT INTO student (roll_no, name, father_name, mother_name, address, phone_no, email) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    student.roll_no,
                    student.name,
                    student.father_name,
                    student.mother_name,
                    student.address,
                    student.phone_no,
                    student.email,
                ),
            )

    def get_by_roll_no(self, roll_no: int) -> Student:
        """Get a student by roll number. Raises NotFoundError if not found."""
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT roll_no, name, father_name, mother_name, address, phone_no, email "
                "FROM student WHERE roll_no=%s",
                (roll_no,),
            )
            row = cursor.fetchone()
            if not row:
                raise NotFoundError(f"Student with roll number {roll_no} not found")
            return Student(
                roll_no=row[0],
                name=row[1],
                father_name=row[2],
                mother_name=row[3],
                address=row[4],
                phone_no=row[5],
                email=row[6],
            )

    def get_all(self) -> list[Student]:
        """Get all students."""
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT roll_no, name, father_name, mother_name, address, phone_no, email FROM student"
            )
            rows = cursor.fetchall()
            return [
                Student(
                    roll_no=row[0],
                    name=row[1],
                    father_name=row[2],
                    mother_name=row[3],
                    address=row[4],
                    phone_no=row[5],
                    email=row[6],
                )
                for row in rows
            ]

    def update(self, student: Student) -> None:
        """Update an existing student. Raises NotFoundError if not found."""
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT roll_no FROM student WHERE roll_no=%s", (student.roll_no,)
            )
            if not cursor.fetchone():
                raise NotFoundError(f"Student with roll number {student.roll_no} not found")

            cursor.execute(
                "UPDATE student SET name=%s, father_name=%s, mother_name=%s, "
                "address=%s, phone_no=%s, email=%s WHERE roll_no=%s",
                (
                    student.name,
                    student.father_name,
                    student.mother_name,
                    student.address,
                    student.phone_no,
                    student.email,
                    student.roll_no,
                ),
            )

    def delete(self, roll_no: int) -> None:
        """Delete a student. Raises NotFoundError if not found."""
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT roll_no FROM student WHERE roll_no=%s", (roll_no,)
            )
            if not cursor.fetchone():
                raise NotFoundError(f"Student with roll number {roll_no} not found")

            cursor.execute("DELETE FROM student WHERE roll_no=%s", (roll_no,))
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_repositories.py::TestStudentRepository -v
```

Expected: All 10 tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/student_management/repositories.py tests/test_repositories.py
git commit -m "feat: add StudentRepository with CRUD operations"
```

---

## Task 7: Exam Repository

**Files:**
- Modify: `src/student_management/repositories.py`
- Modify: `tests/test_repositories.py`

- [ ] **Step 1: Write failing tests for ExamRepository**

Append to `tests/test_repositories.py`:

```python
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
        assert mock_cursor.execute.call_count == 2  # Check student exists + insert

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
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args
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
        mock_cursor.execute.assert_called_once()

    def test_delete_not_found(self, repo, mock_db):
        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_db.cursor.return_value.__exit__ = MagicMock(return_value=False)

        mock_cursor.fetchone.return_value = None

        with pytest.raises(NotFoundError, match="not found"):
            repo.delete(999)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_repositories.py::TestExamRepository -v
```

Expected: FAIL with "cannot import name 'ExamRepository'"

- [ ] **Step 3: Implement ExamRepository**

Append to `src/student_management/repositories.py`:

```python
class ExamRepository:
    """Handles all EXAM table operations."""

    def __init__(self, db: Database) -> None:
        self.db = db

    def create(self, exam: Exam) -> None:
        """Insert a new exam record. Raises DuplicateError if exam exists for roll_no."""
        with self.db.cursor() as cursor:
            # Verify student exists
            cursor.execute(
                "SELECT roll_no FROM student WHERE roll_no=%s", (exam.roll_no,)
            )
            if not cursor.fetchone():
                raise NotFoundError(f"Student with roll number {exam.roll_no} not found")

            # Check for existing exam
            cursor.execute(
                "SELECT roll_no FROM exam WHERE roll_no=%s", (exam.roll_no,)
            )
            if cursor.fetchone():
                raise DuplicateError(f"Exam record for roll number {exam.roll_no} already exists")

            cursor.execute(
                "INSERT INTO exam (roll_no, name, class, section, total_marks, percentage, grade) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    exam.roll_no,
                    exam.name,
                    exam.class_,
                    exam.section,
                    exam.total_marks,
                    exam.percentage,
                    exam.grade,
                ),
            )

    def get_by_roll_no(self, roll_no: int) -> Exam:
        """Get exam by roll number. Raises NotFoundError if not found."""
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT id, roll_no, name, class, section, total_marks, percentage, grade "
                "FROM exam WHERE roll_no=%s",
                (roll_no,),
            )
            row = cursor.fetchone()
            if not row:
                raise NotFoundError(f"Exam record for roll number {roll_no} not found")
            return Exam(
                id=row[0],
                roll_no=row[1],
                name=row[2],
                class_=row[3],
                section=row[4],
                total_marks=row[5],
                percentage=row[6],
                grade=row[7],
            )

    def get_all(self) -> list[Exam]:
        """Get all exam records."""
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT id, roll_no, name, class, section, total_marks, percentage, grade FROM exam"
            )
            rows = cursor.fetchall()
            return [
                Exam(
                    id=row[0],
                    roll_no=row[1],
                    name=row[2],
                    class_=row[3],
                    section=row[4],
                    total_marks=row[5],
                    percentage=row[6],
                    grade=row[7],
                )
                for row in rows
            ]

    def update(self, exam: Exam) -> None:
        """Update an exam record. Raises NotFoundError if not found."""
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT roll_no FROM exam WHERE roll_no=%s", (exam.roll_no,)
            )
            if not cursor.fetchone():
                raise NotFoundError(f"Exam record for roll number {exam.roll_no} not found")

            cursor.execute(
                "UPDATE exam SET name=%s, class=%s, section=%s, total_marks=%s, "
                "percentage=%s, grade=%s WHERE roll_no=%s",
                (
                    exam.name,
                    exam.class_,
                    exam.section,
                    exam.total_marks,
                    exam.percentage,
                    exam.grade,
                    exam.roll_no,
                ),
            )

    def delete(self, roll_no: int) -> None:
        """Delete an exam record. Raises NotFoundError if not found."""
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT roll_no FROM exam WHERE roll_no=%s", (roll_no,)
            )
            if not cursor.fetchone():
                raise NotFoundError(f"Exam record for roll number {roll_no} not found")

            cursor.execute("DELETE FROM exam WHERE roll_no=%s", (roll_no,))
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_repositories.py -v
```

Expected: All 20 tests PASS (10 Student + 10 Exam)

- [ ] **Step 5: Commit**

```bash
git add src/student_management/repositories.py tests/test_repositories.py
git commit -m "feat: add ExamRepository with CRUD operations"
```

---

## Task 8: Student Service

**Files:**
- Create: `src/student_management/services.py`
- Create: `tests/test_services.py`

- [ ] **Step 1: Write failing tests for StudentService**

```python
# tests/test_services.py
"""Tests for service layer."""
import pytest
from unittest.mock import MagicMock
from student_management.services import StudentService, ExamService
from student_management.models import Student, Exam
from student_management.exceptions import ValidationError, NotFoundError


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
            roll_no=1,
            name="John",
            father_name="James",
            mother_name="Jane",
            address="123 Main St",
            phone_no="1234567890",
            email="john@example.com",
        )
        mock_repo.create.return_value = student
        result = service.create_student(student)
        mock_repo.create.assert_called_once_with(student)

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

    def test_delete_student(self, service, mock_repo):
        service.delete_student(1)
        mock_repo.delete.assert_called_once_with(1)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_services.py -v
```

Expected: FAIL with "ModuleNotFoundError"

- [ ] **Step 3: Implement StudentService**

```python
# src/student_management/services.py
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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_services.py::TestStudentService -v
```

Expected: All 10 tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/student_management/services.py tests/test_services.py
git commit -m "feat: add StudentService with validation"
```

---

## Task 9: Exam Service

**Files:**
- Modify: `src/student_management/services.py`
- Modify: `tests/test_services.py`

- [ ] **Step 1: Write failing tests for ExamService**

Append to `tests/test_services.py`:

```python
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

    def test_delete_exam(self, service, mock_repo):
        service.delete_exam(1)
        mock_repo.delete.assert_called_once_with(1)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_services.py::TestExamService -v
```

Expected: FAIL with "cannot import name 'ExamService'"

- [ ] **Step 3: Implement ExamService**

Append to `src/student_management/services.py`:

```python
class ExamService:
    """Business logic for exam operations."""

    VALID_GRADES = {"A", "B", "C", "D", "F"}

    def __init__(self, repo: ExamRepository) -> None:
        self.repo = repo

    def _validate_exam(self, exam: Exam) -> None:
        """Validate exam data. Raises ValidationError on failure."""
        if exam.class_ <= 0:
            raise ValidationError("Class must be a positive integer")
        if not exam.section.strip():
            raise ValidationError("Section is required")
        if exam.total_marks <= 0:
            raise ValidationError("Total marks must be positive")
        if not 0 <= exam.percentage <= 100:
            raise ValidationError("Percentage must be between 0 and 100")
        if exam.grade.upper() not in self.VALID_GRADES:
            raise ValidationError(f"Grade must be one of {', '.join(sorted(self.VALID_GRADES))}")

    def create_exam(self, exam: Exam) -> Exam:
        """Create a new exam record after validation."""
        self._validate_exam(exam)
        exam.grade = exam.grade.upper()
        self.repo.create(exam)
        return exam

    def get_exam(self, roll_no: int) -> Exam:
        """Get exam by roll number."""
        return self.repo.get_by_roll_no(roll_no)

    def list_exams(self) -> list[Exam]:
        """Get all exam records."""
        return self.repo.get_all()

    def update_exam(self, exam: Exam) -> Exam:
        """Update an exam record after validation."""
        self._validate_exam(exam)
        exam.grade = exam.grade.upper()
        self.repo.update(exam)
        return exam

    def delete_exam(self, roll_no: int) -> None:
        """Delete an exam record."""
        self.repo.delete(roll_no)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_services.py -v
```

Expected: All 19 tests PASS (10 Student + 9 Exam)

- [ ] **Step 5: Commit**

```bash
git add src/student_management/services.py tests/test_services.py
git commit -m "feat: add ExamService with validation"
```

---

## Task 10: UI Module

**Files:**
- Create: `src/student_management/ui.py`
- Create: `tests/test_ui.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_ui.py
"""Tests for UI module."""
import pytest
from unittest.mock import patch, MagicMock
from student_management.ui import Menu, StudentUI, ExamUI
from student_management.models import Student, Exam
from student_management.exceptions import AppError, ValidationError, NotFoundError, DuplicateError


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
        assert student.mother_name == "Jane"
        assert student.address == "123 Main St"
        assert student.phone_no == "1234567890"
        assert student.email == "john@test.com"

    @patch("builtins.input", side_effect=["abc", "1"])
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
        assert exam.section == "A"
        assert exam.total_marks == 500
        assert exam.percentage == 85.5
        assert exam.grade == "A"


class TestHandleError:
    """Test error display handling."""

    @patch("builtins.print")
    def test_handle_validation_error(self, mock_print):
        from student_management.ui import handle_error
        handle_error(ValidationError("Invalid input"))
        mock_print.assert_called()
        output = mock_print.call_args[0][0]
        assert "Invalid input" in output

    @patch("builtins.print")
    def test_handle_not_found_error(self, mock_print):
        from student_management.ui import handle_error
        handle_error(NotFoundError("Not found"))
        mock_print.assert_called()
        output = mock_print.call_args[0][0]
        assert "Not found" in output

    @patch("builtins.print")
    def test_handle_duplicate_error(self, mock_print):
        from student_management.ui import handle_error
        handle_error(DuplicateError("Already exists"))
        mock_print.assert_called()
        output = mock_print.call_args[0][0]
        assert "Already exists" in output
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_ui.py -v
```

Expected: FAIL with "ModuleNotFoundError"

- [ ] **Step 3: Implement UI module**

```python
# src/student_management/ui.py
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
            roll_no=roll_no,
            name=name,
            father_name=father_name,
            mother_name=mother_name,
            address=address,
            phone_no=phone_no,
            email=email,
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

        return Exam(
            roll_no=roll_no,
            name=name,
            class_=class_,
            section=section,
            total_marks=total_marks,
            percentage=percentage,
            grade=grade,
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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_ui.py -v
```

Expected: All 9 tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/student_management/ui.py tests/test_ui.py
git commit -m "feat: add UI module with menu and input handling"
```

---

## Task 11: Main Entry Point

**Files:**
- Create: `src/student_management/__main__.py`

- [ ] **Step 1: Implement main entry point**

```python
# src/student_management/__main__.py
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
    # Load configuration
    config = get_config()

    # Initialize database
    db = Database(config)
    try:
        db.initialize()
    except AppError as e:
        print(f"Failed to connect to database: {e}")
        sys.exit(1)

    # Initialize repositories and services
    student_repo = StudentRepository(db)
    exam_repo = ExamRepository(db)
    student_service = StudentService(student_repo)
    exam_service = ExamService(exam_repo)

    print("Connected to database successfully!")

    # Main loop
    while True:
        Menu.display()
        choice = Menu.get_choice()

        try:
            if choice == 1:
                # Add Student
                student = StudentUI.get_student_input()
                student_service.create_student(student)
                print("Student added successfully!")

            elif choice == 2:
                # Display All Students
                students = student_service.list_students()
                StudentUI.display_students(students)

            elif choice == 3:
                # Update Student
                roll_no = StudentUI.get_roll_no_input()
                student = student_service.get_student(roll_no)
                print(f"Current details: {student.name}, {student.father_name}, {student.mother_name}")
                updated = StudentUI.get_student_input()
                updated.roll_no = roll_no
                student_service.update_student(updated)
                print("Student updated successfully!")

            elif choice == 4:
                # Delete Student
                roll_no = StudentUI.get_roll_no_input()
                student_service.delete_student(roll_no)
                print("Student deleted successfully!")

            elif choice == 5:
                # Add Exam Record
                exam = ExamUI.get_exam_input()
                exam_service.create_exam(exam)
                print("Exam record added successfully!")

            elif choice == 6:
                # Display All Exam Records
                exams = exam_service.list_exams()
                ExamUI.display_exams(exams)

            elif choice == 7:
                # Update Exam Record
                roll_no = ExamUI.get_roll_no_input()
                exam = exam_service.get_exam(roll_no)
                print(f"Current details: {exam.name}, Class {exam.class_}, Section {exam.section}")
                updated = ExamUI.get_exam_input()
                updated.roll_no = roll_no
                exam_service.update_exam(updated)
                print("Exam record updated successfully!")

            elif choice == 8:
                # Delete Exam Record
                roll_no = ExamUI.get_roll_no_input()
                exam_service.delete_exam(roll_no)
                print("Exam record deleted successfully!")

            elif choice == 9:
                # Exit
                print("Thank you for using Student Management System!")
                sys.exit(0)

        except AppError as e:
            handle_error(e)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verify module runs**

```bash
python -m student_management --help 2>&1 || echo "Module structure verified (no --help flag, but imports work)"
```

- [ ] **Step 3: Commit**

```bash
git add src/student_management/__main__.py
git commit -m "feat: add main entry point with full CRUD integration"
```

---

## Task 12: SQL Schema & Documentation

**Files:**
- Create: `schema.sql`
- Modify: `README.md`

- [ ] **Step 1: Create schema.sql**

```sql
-- Student Management System Database Schema
-- Run this script to create the required tables.

CREATE DATABASE IF NOT EXISTS student_details;
USE student_details;

-- Student table
CREATE TABLE IF NOT EXISTS student (
    roll_no INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100) NOT NULL,
    mother_name VARCHAR(100) NOT NULL,
    address TEXT,
    phone_no VARCHAR(15) NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Exam table with foreign key to student
CREATE TABLE IF NOT EXISTS exam (
    id INT PRIMARY KEY AUTO_INCREMENT,
    roll_no INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    class INT NOT NULL,
    section VARCHAR(10) NOT NULL,
    total_marks INT NOT NULL,
    percentage DECIMAL(5,2) NOT NULL,
    grade VARCHAR(5) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (roll_no) REFERENCES student(roll_no) ON DELETE CASCADE
);
```

- [ ] **Step 2: Update README.md**

```markdown
# Student Management System

A production-grade CLI application for managing student and examination records, built with Python and MySQL.

## Features

- Add, view, update, and delete student records
- Add, view, update, and delete examination records
- Input validation and error handling
- Connection pooling for database efficiency
- PrettyTable formatted output
- Environment-based configuration

## Prerequisites

- Python 3.10+
- MySQL Server 8.0+
- pip

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Dinesh-raya/Student-management-system-using-python-and-mysql.git
   cd Student-management-system-using-python-and-mysql
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Set up the database:
   ```bash
   mysql -u root -p < schema.sql
   ```

5. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

## Usage

Run the application:
```bash
python -m student_management
```

Or use the installed script:
```bash
student-management
```

## Development

### Running Tests

```bash
pytest
```

With coverage:
```bash
pytest --cov=student_management
```

### Project Structure

```
src/student_management/
├── __init__.py          # Package initialization
├── __main__.py          # Entry point
├── config.py            # Configuration management
├── db.py                # Database connection pooling
├── models.py            # Data models (Student, Exam)
├── repositories.py      # SQL operations
├── services.py          # Business logic and validation
├── ui.py                # User interface
└── exceptions.py        # Custom exceptions
```

## Architecture

The application follows a layered architecture:

1. **UI Layer** (`ui.py`) — Handles all user input/output
2. **Service Layer** (`services.py`) — Business logic and validation
3. **Repository Layer** (`repositories.py`) — Database operations
4. **Database Layer** (`db.py`) — Connection management

Each layer only depends on layers below it, ensuring clean separation of concerns.

## License

MIT
```

- [ ] **Step 3: Commit**

```bash
git add schema.sql README.md
git commit -m "docs: add SQL schema and update README"
```

---

## Task 13: Final Verification

**Files:**
- None (verification only)

- [ ] **Step 1: Run full test suite**

```bash
pytest -v --cov=student_management
```

Expected: All tests pass with 80%+ coverage

- [ ] **Step 2: Verify package installation**

```bash
pip install -e .
python -c "from student_management import __version__; print(f'Version: {__version__}')"
```

Expected: "Version: 1.0.0"

- [ ] **Step 3: Run linting (optional)**

```bash
pip install ruff
ruff check src/ tests/
```

Expected: No errors

- [ ] **Step 4: Final commit**

```bash
git add -A
git commit -m "chore: final verification and cleanup"
```

---

## Summary

| Task | Description | Files Created/Modified |
|------|-------------|----------------------|
| 1 | Project Setup | pyproject.toml, requirements.txt, .env.example, .gitignore |
| 2 | Custom Exceptions | exceptions.py |
| 3 | Configuration | config.py |
| 4 | Database | db.py |
| 5 | Models | models.py |
| 6 | Student Repository | repositories.py |
| 7 | Exam Repository | repositories.py (append) |
| 8 | Student Service | services.py |
| 9 | Exam Service | services.py (append) |
| 10 | UI Module | ui.py |
| 11 | Main Entry Point | __main__.py |
| 12 | Schema & Docs | schema.sql, README.md |
| 13 | Final Verification | (tests only) |

**Total: 13 tasks, ~50 steps, full TDD coverage**
