"""Configuration management using environment variables."""
import os
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Database connection configuration."""

    host: str = "localhost"
    user: str = "root"
    password: str = ""
    database: str = "student_details"
    pool_size: int = 5


def get_config() -> DatabaseConfig:
    """Load configuration from environment variables with defaults."""
    return DatabaseConfig(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "student_details"),
        pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
    )
