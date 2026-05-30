# Student Management System — Production-Grade CLI Refactor

**Date:** 2026-05-30
**Status:** Approved
**Repository:** https://github.com/Dinesh-raya/Student-management-system-using-python-and-mysql.git

## Problem Statement

The current Student Management System is a single-file (203 lines) beginner-level Python script with:
- No separation of concerns (all logic in one file)
- Hardcoded database credentials
- Poor error handling (crashes on invalid input)
- No tests, no type hints, no docstrings
- Database schema issues (INT for phone numbers, INT for percentage)
- No dependency management

**Current Rating: 2.5/10**

**Goal:** Refactor to a production-grade CLI application rated 10/10.

## Target Architecture

### Multi-Module Package Structure

```
student-management-system/
├── src/
│   └── student_management/
│       ├── __init__.py
│       ├── __main__.py          # Entry point (python -m student_management)
│       ├── config.py            # .env loading, settings
│       ├── db.py                # Connection pool, cursor management
│       ├── models.py            # dataclass for Student, Exam
│       ├── repositories.py      # StudentRepo, ExamRepo (SQL operations)
│       ├── services.py          # Business logic (validation, orchestration)
│       ├── ui.py                # Menu display, input handling, PrettyTable formatting
│       └── exceptions.py        # Custom exception hierarchy
├── tests/
│   ├── conftest.py              # Shared fixtures (mock DB, sample data)
│   ├── test_repositories.py     # DB operation tests
│   ├── test_services.py         # Business logic tests
│   └── test_ui.py               # Input/output tests
├── .env.example                 # Template for credentials
├── .gitignore
├── pyproject.toml               # Modern Python packaging
├── requirements.txt             # Pinned dependencies
└── README.md                    # Updated docs
```

**Key decisions:**
- `src/` layout prevents accidental imports from the project root
- `__main__.py` enables `python -m student_management` execution
- `repositories.py` isolates all SQL from business logic
- `services.py` handles validation and orchestration (no SQL)
- `ui.py` handles all user interaction (no business logic)

## Database Layer

### Schema Design

```sql
-- STUDENT table: proper constraints and types
CREATE TABLE student (
    roll_no INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100) NOT NULL,
    mother_name VARCHAR(100) NOT NULL,
    address TEXT,
    phone_no VARCHAR(15) NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- EXAM table: foreign key to student, proper types
CREATE TABLE exam (
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

### Connection Management
- Connection pooling via `mysql.connector.pooling.MySQLConnectionPool`
- Context manager for automatic cursor cleanup
- Configurable pool size via `.env`

## Models

```python
@dataclass
class Student:
    roll_no: int | None = None
    name: str = ""
    father_name: str = ""
    mother_name: str = ""
    address: str = ""
    phone_no: str = ""
    email: str = ""

@dataclass
class Exam:
    id: int | None = None
    roll_no: int = 0
    name: str = ""
    class_: int = 0
    section: str = ""
    total_marks: int = 0
    percentage: float = 0.0
    grade: str = ""
```

## Services Layer

- `StudentService.create_student(data) -> Student` — validates, calls repo, returns created record
- `StudentService.get_student(roll_no) -> Student`
- `StudentService.update_student(roll_no, data) -> Student`
- `StudentService.delete_student(roll_no) -> bool`
- `StudentService.list_students() -> list[Student]`
- `ExamService.create_exam(data) -> Exam` — validates student exists, validates grade/marks, calls repo
- `ExamService.get_exam(roll_no) -> Exam`
- `ExamService.update_exam(roll_no, data) -> Exam`
- `ExamService.delete_exam(roll_no) -> bool`
- `ExamService.list_exams() -> list[Exam]`

**Validation rules:**
- Email format validation (regex)
- Phone number length (10-15 digits)
- Percentage 0-100
- Grade in {A, B, C, D, F}
- Total marks > 0
- Class > 0

## UI Layer

- `Menu.display_main_menu()` — renders the 9-option menu
- `Menu.get_choice()` — validated input (1-9 only, no crash on string)
- `StudentUI.add_student()` — guided input with validation feedback
- `StudentUI.display_students()` — PrettyTable formatted output
- `StudentUI.update_student()` — guided update flow
- `StudentUI.delete_student()` — confirmation before delete
- `ExamUI.add_exam()` — guided input with validation feedback
- `ExamUI.display_exams()` — PrettyTable formatted output
- `ExamUI.update_exam()` — guided update flow
- `ExamUI.delete_exam()` — confirmation before delete

All `print()` and `input()` calls isolated in this module.

## Error Handling

### Exception Hierarchy

```
AppError (base)
├── DatabaseError      — connection/query failures
├── ValidationError    — invalid input data
├── NotFoundError      — record doesn't exist
└── DuplicateError     — roll_no already exists
```

### Error Handling Strategy
- All DB operations wrapped in try/except, raise custom exceptions
- UI layer catches exceptions, displays user-friendly messages
- No raw tracebacks shown to user
- Connection retry logic (3 attempts) for transient DB failures
- Transaction rollback on partial failures

## Configuration

### .env file (python-dotenv)

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=root
DB_NAME=student_details
DB_POOL_SIZE=5
```

### .env.example (committed to git)

Same structure with placeholder values.

## Testing Strategy

### Test Structure

- `conftest.py`: fixtures for mock DB connection, sample Student/Exam objects
- `test_repositories.py`: test each CRUD operation with mocked cursor
- `test_services.py`: test validation logic, business rules, error cases
- `test_ui.py`: test input parsing, menu display (mock input()/print())

### Coverage Target
- 80%+ coverage on services and repositories
- All validation rules tested
- All error paths tested
- Edge cases: empty strings, max lengths, boundary values

### Mocking Strategy
- Mock `mysql.connector` for repository tests
- Mock `input()` for UI tests
- Use `pytest-mock` for clean mocking

## Packaging

### pyproject.toml

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
```

### requirements.txt

```
mysql-connector-python>=8.0
prettytable>=3.0
python-dotenv>=1.0
```

## Migration Path

1. Create new project structure
2. Implement config and db modules first
3. Implement models and repositories
4. Implement services with validation
5. Implement UI layer
6. Write tests
7. Update README
8. Remove old `modified.py`

## Success Criteria

- [ ] All 8 CRUD operations work correctly
- [ ] No crashes on invalid input
- [ ] Database credentials not hardcoded
- [ ] Connection pooling implemented
- [ ] Foreign key relationship between STUDENT and EXAM
- [ ] Proper data types (VARCHAR for phone, DECIMAL for percentage)
- [ ] 80%+ test coverage
- [ ] Clean `python -m student_management` entry point
- [ ] No SQL in UI or service layers
- [ ] Custom exception hierarchy with user-friendly messages
