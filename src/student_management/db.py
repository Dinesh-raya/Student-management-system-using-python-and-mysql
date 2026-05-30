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
