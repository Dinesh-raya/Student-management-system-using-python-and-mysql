"""Tests for configuration module."""
import os
import pytest
from unittest.mock import patch
from student_management.config import DatabaseConfig, get_config


class TestDatabaseConfig:
    """Test DatabaseConfig dataclass."""

    def test_default_values(self):
        config = DatabaseConfig()
        assert config.host == "localhost"
        assert config.user == "root"
        assert config.password == "root"
        assert config.database == "student_details"
        assert config.pool_size == 5

    def test_custom_values(self):
        config = DatabaseConfig(
            host="remotehost",
            user="admin",
            password="secret",
            database="mydb",
            pool_size=10,
        )
        assert config.host == "remotehost"
        assert config.user == "admin"
        assert config.password == "secret"
        assert config.database == "mydb"
        assert config.pool_size == 10


class TestGetConfig:
    """Test get_config function with environment variables."""

    def test_reads_from_env_vars(self):
        env_vars = {
            "DB_HOST": "envhost",
            "DB_USER": "envuser",
            "DB_PASSWORD": "envpass",
            "DB_NAME": "envdb",
            "DB_POOL_SIZE": "3",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            config = get_config()
            assert config.host == "envhost"
            assert config.user == "envuser"
            assert config.password == "envpass"
            assert config.database == "envdb"
            assert config.pool_size == 3

    def test_falls_back_to_defaults(self):
        # Clear relevant env vars
        env_keys = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME", "DB_POOL_SIZE"]
        for k in env_keys:
            os.environ.pop(k, None)
        config = get_config()
        assert config.host == "localhost"
        assert config.user == "root"

    def test_pool_size_converts_to_int(self):
        with patch.dict(os.environ, {"DB_POOL_SIZE": "8"}, clear=False):
            config = get_config()
            assert config.pool_size == 8
            assert isinstance(config.pool_size, int)
