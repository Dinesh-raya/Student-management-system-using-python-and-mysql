# Student Management System

A production-grade CLI application for managing student and examination records, built with Python and MySQL.

## Features

- Add, view, update, and delete student records
- Add, view, update, and delete examination records
- Input validation and error handling
- Connection pooling for database efficiency
- PrettyTable formatted output
- Environment-based configuration

## Prerequisites

- Python 3.10+
- MySQL Server 8.0+
- pip

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Dinesh-raya/Student-management-system-using-python-and-mysql.git
   cd Student-management-system-using-python-and-mysql
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Set up the database:
   ```bash
   mysql -u root -p < schema.sql
   ```

5. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

## Usage

Run the application:
```bash
python -m student_management
```

Or use the installed script:
```bash
student-management
```

## Development

### Running Tests

```bash
pytest
```

With coverage:
```bash
pytest --cov=student_management
```

### Project Structure

```
src/student_management/
├── __init__.py          # Package initialization
├── __main__.py          # Entry point
├── config.py            # Configuration management
├── db.py                # Database connection pooling
├── models.py            # Data models (Student, Exam)
├── repositories.py      # SQL operations
├── services.py          # Business logic and validation
├── ui.py                # User interface
└── exceptions.py        # Custom exceptions
```

## Architecture

The application follows a layered architecture:

1. **UI Layer** (`ui.py`) — Handles all user input/output
2. **Service Layer** (`services.py`) — Business logic and validation
3. **Repository Layer** (`repositories.py`) — Database operations
4. **Database Layer** (`db.py`) — Connection management

Each layer only depends on layers below it, ensuring clean separation of concerns.

## License

MIT
