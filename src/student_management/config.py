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
