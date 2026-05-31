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
