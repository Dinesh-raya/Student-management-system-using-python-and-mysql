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
            password="",
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
