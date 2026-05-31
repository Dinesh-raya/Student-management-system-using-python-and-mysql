# Streamlit Live Demo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the terminal-based Student Management System into a Streamlit web app with SQLite, deployable to Streamlit Cloud.

**Architecture:** Replace MySQL with SQLite (zero-infrastructure), keep existing models/services layer, replace terminal UI with multi-page Streamlit app (Dashboard, Students, Exams). Preserve the clean layered architecture: models -> repositories -> services -> Streamlit pages.

**Tech Stack:** Python 3.11+, Streamlit, SQLite3 (built-in), pytest

---

## File Structure

| Action | File | Responsibility |
|--------|------|---------------|
| Rewrite | `src/student_management/db.py` | SQLite connection management |
| Rewrite | `src/student_management/config.py` | SQLite file path config |
| Modify | `src/student_management/repositories.py` | Change MySQL syntax to SQLite |
| Keep | `src/student_management/models.py` | Data models (unchanged) |
| Keep | `src/student_management/services.py` | Business logic (unchanged) |
| Keep | `src/student_management/exceptions.py` | Exceptions (unchanged) |
| Delete | `src/student_management/ui.py` | Terminal UI (replaced) |
| Delete | `src/student_management/__main__.py` | CLI entry point (replaced) |
| Rewrite | `tests/test_db.py` | SQLite database tests |
| Rewrite | `tests/test_config.py` | SQLite config tests |
| Modify | `tests/test_repositories.py` | Update SQL assertions for SQLite |
| Delete | `tests/test_ui.py` | Terminal UI tests (replaced) |
| Create | `app.py` | Streamlit entry point (Dashboard) |
| Create | `pages/1_📊_Dashboard.py` | Dashboard with stats and charts |
| Create | `pages/2_👨‍🎓_Students.py` | Student CRUD page |
| Create | `pages/3_📝_Exams.py` | Exam CRUD page |
| Rewrite | `requirements.txt` | Streamlit deps, remove MySQL |
| Create | `.streamlit/config.toml` | Streamlit theme config |

---

## Task 1: Database Layer — SQLite

Replace MySQL connection pool with SQLite. Same `Database` class interface so repositories/services work unchanged.

**Files:**
- Rewrite: `src/student_management/db.py`
- Rewrite: `tests/test_db.py`

### Step 1: Write failing tests for SQLite Database

```python
"""Tests for database connection module."""
import os
import sqlite3
import pytest
from student_management.db import Database
from student_management.config import DatabaseConfig
from student_management.exceptions import DatabaseError


class TestDatabase:
    """Test Database connection manager with SQLite."""

    @pytest.fixture
    def tmp_db_path(self, tmp_path):
        return str(tmp_path / "test.db")

    @pytest.fixture
    def config(self, tmp_db_path):
        return DatabaseConfig(db_path=tmp_db_path)

    def test_init_stores_config(self, config, tmp_db_path):
        db = Database(config)
        assert db.config == config
        assert db.config.db_path == tmp_db_path

    def test_initialize_creates_database_file(self, config, tmp_db_path):
        db = Database(config)
        db.initialize()
        assert os.path.exists(tmp_db_path)

    def test_initialize_creates_students_table(self, config):
        db = Database(config)
        db.initialize()
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='students'"
            )
            assert cursor.fetchone() is not None

    def test_initialize_creates_exams_table(self, config):
        db = Database(config)
        db.initialize()
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='exams'"
            )
            assert cursor.fetchone() is not None

    def test_initialize_is_idempotent(self, config):
        db = Database(config)
        db.initialize()
        db.initialize()  # Should not raise
        with db.cursor() as cursor:
            cursor.execute("SELECT count(*) FROM students")
            assert cursor.fetchone()[0] == 0

    def test_get_connection_raises_if_not_initialized(self, config):
        db = Database(config)
        with pytest.raises(DatabaseError, match="Database not initialized"):
            db.get_connection()

    def test_cursor_context_manager_commits(self, config):
        db = Database(config)
        db.initialize()
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO students (roll_no, name, father_name, mother_name, phone_no) "
                "VALUES (1, 'John', 'James', 'Jane', '1234567890')"
            )
        # Verify data persisted
        with db.cursor() as cursor:
            cursor.execute("SELECT name FROM students WHERE roll_no=1")
            assert cursor.fetchone()[0] == "John"

    def test_cursor_context_manager_rollbacks_on_error(self, config):
        db = Database(config)
        db.initialize()
        with pytest.raises(sqlite3.IntegrityError):
            with db.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO students (roll_no, name, father_name, mother_name, phone_no) "
                    "VALUES (1, 'John', 'James', 'Jane', '1234567890')"
                )
                # Duplicate roll_no should raise
                cursor.execute(
                    "INSERT INTO students (roll_no, name, father_name, mother_name, phone_no) "
                    "VALUES (1, 'Jane', 'Bob', 'Alice', '0987654321')"
                )
        # First insert should have been rolled back
        with db.cursor() as cursor:
            cursor.execute("SELECT count(*) FROM students WHERE roll_no=1")
            assert cursor.fetchone()[0] == 0

    def test_get_connection_returns_sqlite_connection(self, config):
        db = Database(config)
        db.initialize()
        conn = db.get_connection()
        assert isinstance(conn, sqlite3.Connection)
        conn.close()
```

### Step 2: Run tests to verify they fail

Run: `pytest tests/test_db.py -v`
Expected: FAIL — `DatabaseConfig` has no `db_path`, `Database` uses MySQL

### Step 3: Rewrite config.py for SQLite

```python
"""Configuration management using environment variables."""
import os
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Database connection configuration."""

    db_path: str = "student_management.db"


def get_config() -> DatabaseConfig:
    """Load configuration from environment variables with defaults."""
    return DatabaseConfig(
        db_path=os.getenv("DB_PATH", "student_management.db"),
    )
```

### Step 4: Rewrite test_config.py

```python
"""Tests for configuration module."""
import os
import pytest
from unittest.mock import patch
from student_management.config import DatabaseConfig, get_config


class TestDatabaseConfig:
    """Test DatabaseConfig dataclass."""

    def test_default_values(self):
        config = DatabaseConfig()
        assert config.db_path == "student_management.db"

    def test_custom_values(self):
        config = DatabaseConfig(db_path="/tmp/custom.db")
        assert config.db_path == "/tmp/custom.db"


class TestGetConfig:
    """Test get_config function with environment variables."""

    def test_reads_from_env_vars(self):
        with patch.dict(os.environ, {"DB_PATH": "/tmp/env.db"}, clear=False):
            config = get_config()
            assert config.db_path == "/tmp/env.db"

    def test_falls_back_to_defaults(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("DB_PATH", None)
            config = get_config()
            assert config.db_path == "student_management.db"
```

### Step 5: Rewrite db.py for SQLite

```python
"""Database connection management with SQLite."""
import sqlite3
from contextlib import contextmanager

from student_management.config import DatabaseConfig
from student_management.exceptions import DatabaseError

_CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS students (
    roll_no INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    father_name TEXT NOT NULL,
    mother_name TEXT NOT NULL,
    address TEXT DEFAULT '',
    phone_no TEXT NOT NULL,
    email TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no INTEGER NOT NULL,
    name TEXT NOT NULL,
    class INTEGER NOT NULL,
    section TEXT NOT NULL,
    total_marks INTEGER NOT NULL,
    percentage REAL NOT NULL,
    grade TEXT NOT NULL,
    FOREIGN KEY (roll_no) REFERENCES students(roll_no)
);
"""


class Database:
    """Manages SQLite connection and provides context-managed cursors."""

    def __init__(self, config: DatabaseConfig) -> None:
        self.config = config
        self._initialized = False

    def initialize(self) -> None:
        """Create the database file and tables. Call once at startup."""
        try:
            conn = sqlite3.connect(self.config.db_path)
            conn.executescript(_CREATE_TABLES_SQL)
            conn.close()
            self._initialized = True
        except Exception as e:
            raise DatabaseError(f"Failed to initialize database: {e}") from e

    def get_connection(self) -> sqlite3.Connection:
        """Get a connection to the SQLite database."""
        if not self._initialized:
            raise DatabaseError("Database not initialized. Call initialize() first.")
        return sqlite3.connect(self.config.db_path)

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

### Step 6: Run tests to verify they pass

Run: `pytest tests/test_db.py tests/test_config.py -v`
Expected: ALL PASS

### Step 7: Commit

```bash
git add src/student_management/db.py src/student_management/config.py tests/test_db.py tests/test_config.py
git commit -m "feat: replace MySQL with SQLite database layer"
```

---

## Task 2: Repository Layer — SQLite Syntax

Change MySQL `%s` placeholders to SQLite `?` syntax.

**Files:**
- Modify: `src/student_management/repositories.py`
- Modify: `tests/test_repositories.py`

### Step 1: Update repositories.py — change all `%s` to `?`

Replace every `%s` with `?` in all SQL queries. The table names stay the same (`student`, `exam`). The logic stays identical.

Specific changes:
- Line 17: `%s` -> `?`
- Line 24: `%s` -> `?` (6 times in INSERT)
- Line 41: `%s` -> `?`
- Line 61: no change (no placeholders)
- Line 81: `%s` -> `?`
- Line 87-88: `%s` -> `?` (7 times in UPDATE)
- Line 103: `%s` -> `?`
- Line 109: `%s` -> `?`
- Line 123: `%s` -> `?`
- Line 131: `%s` -> `?`
- Line 137: `%s` -> `?` (7 times in INSERT)
- Line 153: `%s` -> `?`
- Line 175: no change (no placeholders)
- Line 196: `%s` -> `?`
- Line 202-203: `%s` -> `?` (7 times in UPDATE)
- Line 219: `%s` -> `?`
- Line 225: `%s` -> `?`

### Step 2: Update test_repositories.py — SQL assertions

Update the SQL string assertions to match SQLite `?` syntax:

```python
# In test_create_student:
assert "INSERT INTO student" in call_args[0][0]
# Keep as-is — INSERT INTO student is still the same

# In test_update_student:
assert "UPDATE student" in call_args[0][0]
# Keep as-is — UPDATE student is still the same

# In test_delete_student:
assert "DELETE FROM student" in call_args[0][0]
# Keep as-is — DELETE FROM student is still the same
```

The SQL assertions in tests check table names and operation types, not placeholder syntax, so they should still pass after the `%s` -> `?` change.

### Step 3: Run all tests to verify

Run: `pytest tests/ -v`
Expected: ALL PASS (repositories tests use mocks, so the placeholder change doesn't affect them)

### Step 4: Commit

```bash
git add src/student_management/repositories.py tests/test_repositories.py
git commit -m "feat: update repository SQL syntax for SQLite"
```

---

## Task 3: Remove Terminal UI Files

Clean up old terminal UI code that's being replaced by Streamlit.

**Files:**
- Delete: `src/student_management/ui.py`
- Delete: `src/student_management/__main__.py`
- Delete: `tests/test_ui.py`

### Step 1: Delete the files

```bash
rm src/student_management/ui.py
rm src/student_management/__main__.py
rm tests/test_ui.py
```

### Step 2: Run remaining tests to verify nothing breaks

Run: `pytest tests/ -v`
Expected: ALL PASS (no remaining code imports ui.py or __main__.py)

### Step 3: Commit

```bash
git add -A
git commit -m "chore: remove terminal UI and CLI entry point"
```

---

## Task 4: Requirements and Streamlit Config

Set up dependencies and theme configuration.

**Files:**
- Rewrite: `requirements.txt`
- Create: `.streamlit/config.toml`

### Step 1: Rewrite requirements.txt

```
streamlit>=1.30.0
prettytable>=3.0
python-dotenv>=1.0
pytest>=8.0
```

Remove `mysql-connector-python`. Add `streamlit`.

### Step 2: Create .streamlit/config.toml

```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true

[browser]
gatherUsageStats = false
```

### Step 3: Install dependencies

Run: `pip install -r requirements.txt`

### Step 4: Commit

```bash
git add requirements.txt .streamlit/config.toml
git commit -m "feat: add Streamlit dependency and theme config"
```

---

## Task 5: Streamlit App Entry Point (Dashboard)

Create the main app.py that serves as the home/dashboard page.

**Files:**
- Create: `app.py`

### Step 1: Create app.py

```python
"""Student Management System — Streamlit Dashboard."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
from student_management.config import get_config
from student_management.db import Database
from student_management.repositories import StudentRepository, ExamRepository
from student_management.services import StudentService, ExamService


@st.cache_resource
def init_database():
    """Initialize database connection (cached across reruns)."""
    config = get_config()
    db = Database(config)
    db.initialize()
    return db


def get_services():
    """Get service instances."""
    db = init_database()
    student_repo = StudentRepository(db)
    exam_repo = ExamRepository(db)
    return StudentService(student_repo), ExamService(exam_repo)


def main():
    st.set_page_config(
        page_title="Student Management System",
        page_icon="🎓",
        layout="wide",
    )

    st.title("🎓 Student Management System")
    st.markdown("Welcome to the Student Management System dashboard.")

    student_service, exam_service = get_services()

    # Metrics
    col1, col2, col3 = st.columns(3)

    students = student_service.list_students()
    exams = exam_service.list_exams()

    with col1:
        st.metric("Total Students", len(students))

    with col2:
        st.metric("Total Exams", len(exams))

    with col3:
        if exams:
            avg_pct = sum(e.percentage for e in exams) / len(exams)
            st.metric("Average Percentage", f"{avg_pct:.1f}%")
        else:
            st.metric("Average Percentage", "N/A")

    st.divider()

    # Grade distribution
    if exams:
        st.subheader("Grade Distribution")
        grade_counts = {}
        for e in exams:
            grade_counts[e.grade] = grade_counts.get(e.grade, 0) + 1

        st.bar_chart(grade_counts)
    else:
        st.info("No exam records yet. Add some on the Exams page.")

    # Recent records
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Recent Students")
        if students:
            for s in students[-5:]:
                with st.expander(f"{s.name} (Roll #{s.roll_no})"):
                    st.write(f"**Father:** {s.father_name}")
                    st.write(f"**Mother:** {s.mother_name}")
                    st.write(f"**Phone:** {s.phone_no}")
                    if s.email:
                        st.write(f"**Email:** {s.email}")
        else:
            st.info("No students yet. Add some on the Students page.")

    with col2:
        st.subheader("Recent Exams")
        if exams:
            for e in exams[-5:]:
                with st.expander(f"{e.name} — Grade {e.grade}"):
                    st.write(f"**Class:** {e.class_}, Section {e.section}")
                    st.write(f"**Total Marks:** {e.total_marks}")
                    st.write(f"**Percentage:** {e.percentage}%")
        else:
            st.info("No exam records yet. Add some on the Exams page.")


if __name__ == "__main__":
    main()
```

### Step 2: Verify it runs

Run: `streamlit run app.py --server.headless true`
Expected: App starts without errors, shows dashboard with empty metrics

### Step 3: Commit

```bash
git add app.py
git commit -m "feat: add Streamlit dashboard entry point"
```

---

## Task 6: Students CRUD Page

Create the Students page with full Create/Read/Update/Delete operations.

**Files:**
- Create: `pages/2_👨‍🎓_Students.py`

### Step 1: Create pages directory and Students page

Create `pages/` directory first, then create the file:

```python
"""Students CRUD page."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from student_management.models import Student
from student_management.exceptions import AppError, ValidationError, NotFoundError, DuplicateError
from app import get_services


def display_student_form(student: Student | None = None) -> Student | None:
    """Display student form. Returns Student if submitted, None otherwise."""
    with st.form("student_form", clear_on_submit=True):
        roll_no = st.number_input(
            "Roll No",
            min_value=1,
            value=student.roll_no if student else 1,
            disabled=student is not None,
        )
        name = st.text_input("Name", value=student.name if student else "")
        father_name = st.text_input("Father's Name", value=student.father_name if student else "")
        mother_name = st.text_input("Mother's Name", value=student.mother_name if student else "")
        address = st.text_input("Address", value=student.address if student else "")
        phone_no = st.text_input("Phone No", value=student.phone_no if student else "")
        email = st.text_input("Email", value=student.email if student else "")

        submitted = st.form_submit_button("Update" if student else "Add")

        if submitted:
            return Student(
                roll_no=roll_no,
                name=name,
                father_name=father_name,
                mother_name=mother_name,
                address=address,
                phone_no=phone_no,
                email=email,
            )
    return None


def main():
    st.set_page_config(page_title="Students", page_icon="👨‍🎓", layout="wide")
    st.title("👨‍🎓 Students")

    student_service, _ = get_services()

    # Sidebar for mode selection
    mode = st.sidebar.radio("Action", ["View All", "Add Student", "Edit Student", "Delete Student"])

    if mode == "View All":
        st.subheader("All Students")
        students = student_service.list_students()

        if not students:
            st.info("No students found. Add one using the sidebar.")
            return

        # Search
        search = st.text_input("Search by name or roll number")
        if search:
            students = [
                s for s in students
                if search.lower() in s.name.lower() or str(s.roll_no) == search
            ]

        # Display as table
        if students:
            data = [
                {
                    "Roll No": s.roll_no,
                    "Name": s.name,
                    "Father's Name": s.father_name,
                    "Mother's Name": s.mother_name,
                    "Address": s.address,
                    "Phone": s.phone_no,
                    "Email": s.email,
                }
                for s in students
            ]
            st.dataframe(data, use_container_width=True)

    elif mode == "Add Student":
        st.subheader("Add New Student")
        student = display_student_form()
        if student:
            try:
                student_service.create_student(student)
                st.success(f"Student {student.name} added successfully!")
            except AppError as e:
                st.error(str(e))

    elif mode == "Edit Student":
        st.subheader("Edit Student")
        students = student_service.list_students()
        if not students:
            st.info("No students to edit.")
            return

        roll_options = {f"{s.name} (Roll #{s.roll_no})": s.roll_no for s in students}
        selected = st.selectbox("Select Student", list(roll_options.keys()))

        if selected:
            roll_no = roll_options[selected]
            student = student_service.get_student(roll_no)
            updated = display_student_form(student)
            if updated:
                try:
                    student_service.update_student(updated)
                    st.success(f"Student {updated.name} updated successfully!")
                except AppError as e:
                    st.error(str(e))

    elif mode == "Delete Student":
        st.subheader("Delete Student")
        students = student_service.list_students()
        if not students:
            st.info("No students to delete.")
            return

        roll_options = {f"{s.name} (Roll #{s.roll_no})": s.roll_no for s in students}
        selected = st.selectbox("Select Student", list(roll_options.keys()))

        if selected:
            roll_no = roll_options[selected]
            student = student_service.get_student(roll_no)
            st.warning(f"Are you sure you want to delete **{student.name}** (Roll #{roll_no})?")
            if st.button("Delete", type="primary"):
                try:
                    student_service.delete_student(roll_no)
                    st.success(f"Student {student.name} deleted successfully!")
                    st.rerun()
                except AppError as e:
                    st.error(str(e))


if __name__ == "__main__":
    main()
```

### Step 2: Verify it runs

Run: `streamlit run app.py --server.headless true`
Expected: Sidebar shows "Students" page, navigation works

### Step 3: Commit

```bash
git add pages/
git commit -m "feat: add Students CRUD page"
```

---

## Task 7: Exams CRUD Page

Create the Exams page with full CRUD operations.

**Files:**
- Create: `pages/3_📝_Exams.py`

### Step 1: Create Exams page

```python
"""Exams CRUD page."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from student_management.models import Exam
from student_management.exceptions import AppError
from app import get_services


VALID_GRADES = ["A", "B", "C", "D", "F"]


def display_exam_form(exam: Exam | None = None) -> Exam | None:
    """Display exam form. Returns Exam if submitted, None otherwise."""
    with st.form("exam_form", clear_on_submit=True):
        roll_no = st.number_input(
            "Roll No",
            min_value=1,
            value=exam.roll_no if exam else 1,
            disabled=exam is not None,
        )
        name = st.text_input("Student Name", value=exam.name if exam else "")
        class_ = st.number_input("Class", min_value=1, value=exam.class_ if exam else 1)
        section = st.text_input("Section", value=exam.section if exam else "")
        total_marks = st.number_input("Total Marks", min_value=0, value=exam.total_marks if exam else 0)
        percentage = st.number_input(
            "Percentage",
            min_value=0.0,
            max_value=100.0,
            value=exam.percentage if exam else 0.0,
            step=0.1,
        )
        grade = st.selectbox(
            "Grade",
            VALID_GRADES,
            index=VALID_GRADES.index(exam.grade) if exam and exam.grade in VALID_GRADES else 0,
        )

        submitted = st.form_submit_button("Update" if exam else "Add")

        if submitted:
            return Exam(
                roll_no=roll_no,
                name=name,
                class_=class_,
                section=section,
                total_marks=total_marks,
                percentage=percentage,
                grade=grade,
            )
    return None


def main():
    st.set_page_config(page_title="Exams", page_icon="📝", layout="wide")
    st.title("📝 Exams")

    _, exam_service = get_services()

    # Sidebar for mode selection
    mode = st.sidebar.radio("Action", ["View All", "Add Exam", "Edit Exam", "Delete Exam"])

    if mode == "View All":
        st.subheader("All Exam Records")
        exams = exam_service.list_exams()

        if not exams:
            st.info("No exam records found. Add one using the sidebar.")
            return

        # Search
        search = st.text_input("Search by name or roll number")
        if search:
            exams = [
                e for e in exams
                if search.lower() in e.name.lower() or str(e.roll_no) == search
            ]

        # Display as table with color coding
        if exams:
            data = [
                {
                    "Roll No": e.roll_no,
                    "Name": e.name,
                    "Class": e.class_,
                    "Section": e.section,
                    "Total Marks": e.total_marks,
                    "Percentage": e.percentage,
                    "Grade": e.grade,
                }
                for e in exams
            ]
            st.dataframe(
                data,
                use_container_width=True,
                column_config={
                    "Percentage": st.column_config.ProgressColumn(
                        "Percentage",
                        min_value=0,
                        max_value=100,
                        format="%.1f%%",
                    ),
                    "Grade": st.column_config.TextColumn("Grade"),
                },
            )

    elif mode == "Add Exam":
        st.subheader("Add New Exam Record")
        exam = display_exam_form()
        if exam:
            try:
                exam_service.create_exam(exam)
                st.success(f"Exam record for {exam.name} added successfully!")
            except AppError as e:
                st.error(str(e))

    elif mode == "Edit Exam":
        st.subheader("Edit Exam Record")
        exams = exam_service.list_exams()
        if not exams:
            st.info("No exam records to edit.")
            return

        roll_options = {f"{e.name} (Roll #{e.roll_no})": e.roll_no for e in exams}
        selected = st.selectbox("Select Exam Record", list(roll_options.keys()))

        if selected:
            roll_no = roll_options[selected]
            exam = exam_service.get_exam(roll_no)
            updated = display_exam_form(exam)
            if updated:
                try:
                    exam_service.update_exam(updated)
                    st.success(f"Exam record for {updated.name} updated successfully!")
                except AppError as e:
                    st.error(str(e))

    elif mode == "Delete Exam":
        st.subheader("Delete Exam Record")
        exams = exam_service.list_exams()
        if not exams:
            st.info("No exam records to delete.")
            return

        roll_options = {f"{e.name} (Roll #{e.roll_no})": e.roll_no for e in exams}
        selected = st.selectbox("Select Exam Record", list(roll_options.keys()))

        if selected:
            roll_no = roll_options[selected]
            exam = exam_service.get_exam(roll_no)
            st.warning(f"Are you sure you want to delete exam record for **{exam.name}** (Roll #{roll_no})?")
            if st.button("Delete", type="primary"):
                try:
                    exam_service.delete_exam(roll_no)
                    st.success(f"Exam record for {exam.name} deleted successfully!")
                    st.rerun()
                except AppError as e:
                    st.error(str(e))


if __name__ == "__main__":
    main()
```

### Step 2: Verify it runs

Run: `streamlit run app.py --server.headless true`
Expected: Exams page accessible from sidebar, all CRUD operations work

### Step 3: Commit

```bash
git add pages/3_📝_Exams.py
git commit -m "feat: add Exams CRUD page"
```

---

## Task 8: Dashboard Page (Separate from app.py)

Create a dedicated Dashboard page with richer analytics.

**Files:**
- Create: `pages/1_📊_Dashboard.py`

### Step 1: Create Dashboard page

```python
"""Dashboard page with analytics."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from app import get_services


def main():
    st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
    st.title("📊 Dashboard")

    student_service, exam_service = get_services()

    students = student_service.list_students()
    exams = exam_service.list_exams()

    # Key metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Students", len(students))

    with col2:
        st.metric("Total Exams", len(exams))

    with col3:
        if exams:
            avg_pct = sum(e.percentage for e in exams) / len(exams)
            st.metric("Average Percentage", f"{avg_pct:.1f}%")
        else:
            st.metric("Average Percentage", "N/A")

    st.divider()

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Grade Distribution")
        if exams:
            grade_counts = {}
            for grade in ["A", "B", "C", "D", "F"]:
                grade_counts[grade] = sum(1 for e in exams if e.grade == grade)
            st.bar_chart(grade_counts)
        else:
            st.info("No exam data yet.")

    with col2:
        st.subheader("Class Distribution")
        if exams:
            class_counts = {}
            for e in exams:
                key = f"Class {e.class_}"
                class_counts[key] = class_counts.get(key, 0) + 1
            st.bar_chart(class_counts)
        else:
            st.info("No exam data yet.")

    st.divider()

    # Top performers
    st.subheader("Top Performers")
    if exams:
        top = sorted(exams, key=lambda e: e.percentage, reverse=True)[:5]
        for i, e in enumerate(top, 1):
            st.write(f"**{i}. {e.name}** — {e.percentage}% (Grade {e.grade})")
    else:
        st.info("No exam data yet.")


if __name__ == "__main__":
    main()
```

### Step 2: Verify navigation works

Run: `streamlit run app.py --server.headless true`
Expected: Three pages in sidebar — Dashboard, Students, Exams

### Step 3: Commit

```bash
git add pages/1_📊_Dashboard.py
git commit -m "feat: add Dashboard analytics page"
```

---

## Task 9: Final Verification and Cleanup

Run full test suite and verify the Streamlit app works end-to-end.

### Step 1: Run all tests

Run: `pytest tests/ -v`
Expected: ALL PASS

### Step 2: Verify no imports to deleted files

Run: `grep -r "from student_management.ui" src/` and `grep -r "from student_management.__main__" src/`
Expected: No matches

### Step 3: Verify Streamlit app starts

Run: `streamlit run app.py --server.headless true --server.port 8501`
Expected: App starts, all three pages accessible

### Step 4: Final commit

```bash
git add -A
git commit -m "chore: final cleanup for Streamlit demo"
```

---

## Execution Notes

**Parallelization opportunities:**
- Tasks 1-3 (backend) must be sequential
- Tasks 5-8 (Streamlit pages) can be parallel after Task 4
- Task 4 (requirements) can run in parallel with Tasks 1-3

**Critical path:** Task 1 -> Task 2 -> Task 3 -> Task 5 (app.py) -> Tasks 6,7,8 (parallel) -> Task 9
