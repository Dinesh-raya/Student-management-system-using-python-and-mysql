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

    def test_initialize_creates_student_table(self, config):
        db = Database(config)
        db.initialize()
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='student'"
            )
            assert cursor.fetchone() is not None

    def test_initialize_creates_exam_table(self, config):
        db = Database(config)
        db.initialize()
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='exam'"
            )
            assert cursor.fetchone() is not None

    def test_initialize_is_idempotent(self, config):
        db = Database(config)
        db.initialize()
        db.initialize()  # Should not raise
        with db.cursor() as cursor:
            cursor.execute("SELECT count(*) FROM student")
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
                "INSERT INTO student (roll_no, name, father_name, mother_name, phone_no) "
                "VALUES (1, 'John', 'James', 'Jane', '1234567890')"
            )
        # Verify data persisted
        with db.cursor() as cursor:
            cursor.execute("SELECT name FROM student WHERE roll_no=1")
            assert cursor.fetchone()[0] == "John"

    def test_cursor_context_manager_rollbacks_on_error(self, config):
        db = Database(config)
        db.initialize()
        with pytest.raises(sqlite3.IntegrityError):
            with db.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO student (roll_no, name, father_name, mother_name, phone_no) "
                    "VALUES (1, 'John', 'James', 'Jane', '1234567890')"
                )
                # Duplicate roll_no should raise
                cursor.execute(
                    "INSERT INTO student (roll_no, name, father_name, mother_name, phone_no) "
                    "VALUES (1, 'Jane', 'Bob', 'Alice', '0987654321')"
                )
        # First insert should have been rolled back
        with db.cursor() as cursor:
            cursor.execute("SELECT count(*) FROM student WHERE roll_no=1")
            assert cursor.fetchone()[0] == 0

    def test_get_connection_returns_sqlite_connection(self, config):
        db = Database(config)
        db.initialize()
        conn = db.get_connection()
        assert isinstance(conn, sqlite3.Connection)
        conn.close()
