# Streamlit Live Demo — Design Spec

**Date:** 2026-05-31
**Status:** Approved

## Goal

Convert the terminal-based Student Management System into a Streamlit web app deployable to Streamlit Cloud. Replace MySQL with SQLite for zero-infrastructure hosting.

## Scope

- Full CRUD for Students and Exams (existing 8 operations)
- Dashboard with stats and charts
- Replace terminal UI entirely with Streamlit
- Deploy to Streamlit Cloud (free tier)

## Architecture

### Reuse as-is

| File | Reason |
|------|--------|
| `models.py` | Dataclasses are DB-agnostic |
| `services.py` | Business logic + validation, no DB dependency |
| `exceptions.py` | Custom exceptions, no changes needed |

### Adapt

| File | Change |
|------|--------|
| `db.py` | Replace MySQL connection pool with `sqlite3`. Same `Database` class interface (`initialize()`, `cursor()`). Auto-create tables on first run. |
| `repositories.py` | Change `%s` to `?` (SQLite placeholders). Adjust `INSERT` to `INSERT OR REPLACE`. Change `AUTO_INCREMENT` to `INTEGER PRIMARY KEY AUTOINCREMENT`. |
| `config.py` | Point to SQLite file path instead of MySQL connection params. Remove `mysql-connector-python` dependency. |

### Remove

| File | Reason |
|------|--------|
| `ui.py` | Terminal UI replaced by Streamlit pages |
| `__main__.py` | Streamlit has its own entry point (`streamlit run app.py`) |

### New files

```
app.py                      # Streamlit entry point — home/dashboard
pages/
  1_📊_Dashboard.py         # Stats, charts, overview
  2_👨‍🎓_Students.py          # Full CRUD for students
  3_📝_Exams.py             # Full CRUD for exams
requirements.txt            # Add streamlit, remove mysql-connector-python
.streamlit/config.toml      # Theme settings
```

## Database (SQLite)

- File: `student_management.db` in project root
- Auto-created on first run by `db.py`
- Tables: `students` and `exams` (same schema as current MySQL)
- `Database` class preserves existing interface so repositories/services work unchanged

**Students table:**
```sql
CREATE TABLE IF NOT EXISTS students (
    roll_no INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    father_name TEXT NOT NULL,
    mother_name TEXT NOT NULL,
    address TEXT,
    phone_no TEXT NOT NULL,
    email TEXT
)
```

**Exams table:**
```sql
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
)
```

## Streamlit Pages

### Dashboard (`app.py`)

The home page / landing page.

- **Metrics row:** Total students, total exams, average percentage
- **Grade distribution:** Bar chart of grade counts (A/B/C/D/F)
- **Recent records:** Last 5 students and last 5 exam records in expanders

### Students page (`pages/2_👨‍🎓_Students.py`)

Full CRUD with Streamlit forms and data editor.

- **Add Student:** `st.form` with fields matching `Student` dataclass. Validation via `StudentService.create_student()`. Success/error messages via `st.success`/`st.error`.
- **View Students:** `st.dataframe` showing all students. Search box to filter by roll number or name.
- **Edit Student:** Select row, pre-fill form with current values, submit calls `StudentService.update_student()`.
- **Delete Student:** Select by roll number, confirm with `st.warning` + button, calls `StudentService.delete_student()`.

### Exams page (`pages/3_📝_Exams.py`)

Same pattern as Students page.

- **Add Exam:** Form with all Exam fields. Grade validated against `{"A", "B", "C", "D", "F"}`.
- **View Exams:** `st.dataframe` with color-coded grades. Filter by roll number.
- **Edit Exam:** Select row, pre-fill form, submit updates.
- **Delete Exam:** Select by roll number, confirm and delete.

## Page Layout

- Sidebar: navigation handled automatically by Streamlit multi-page
- Each page uses `st.set_page_config(layout="wide")` for table-heavy views
- Session state used to track current operation (add/edit/delete mode)

## Deployment

1. `requirements.txt`: `streamlit`, `prettytable`, `mysql-connector-python` removed
2. `.streamlit/config.toml`: Theme (primary color, background, font)
3. Streamlit Cloud: connect GitHub repo, set main file to `app.py`
4. SQLite DB auto-initializes — no manual setup for viewers

## What Stays the Same

- All business logic in `services.py` (validation, error handling)
- All data models in `models.py`
- All custom exceptions in `exceptions.py`
- Repository pattern in `repositories.py` (just SQL syntax changes)
- Test structure — `test_models.py`, `test_services.py`, `test_exceptions.py` keep working. `test_db.py` and `test_repositories.py` need SQLite setup changes. `test_ui.py` removed (terminal UI gone).

## Out of Scope

- User authentication / login
- MySQL support (removed — SQLite only)
- Export to CSV / PDF
- Mobile-responsive layout (Streamlit handles this natively)
