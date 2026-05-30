"""Custom exception hierarchy for Student Management System."""


class AppError(Exception):
    """Base exception for all application errors."""


class DatabaseError(AppError):
    """Raised when database operations fail."""


class ValidationError(AppError):
    """Raised when input data fails validation."""


class NotFoundError(AppError):
    """Raised when a requested record does not exist."""


class DuplicateError(AppError):
    """Raised when attempting to create a record that already exists."""
