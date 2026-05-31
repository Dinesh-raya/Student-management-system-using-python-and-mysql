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
