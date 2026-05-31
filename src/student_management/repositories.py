"""Repository layer — all SQL lives here."""
from student_management.db import Database
from student_management.models import Student, Exam
from student_management.exceptions import NotFoundError, DuplicateError


class StudentRepository:
    """Handles all STUDENT table operations."""

    def __init__(self, db: Database) -> None:
        self.db = db

    def create(self, student: Student) -> None:
        """Insert a new student. Raises DuplicateError if roll_no exists."""
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT roll_no FROM student WHERE roll_no=?", (student.roll_no,)
            )
            if cursor.fetchone():
                raise DuplicateError(f"Roll number {student.roll_no} already exists")

            cursor.execute(
                "INSERT INTO student (roll_no, name, father_name, mother_name, address, phone_no, email) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    student.roll_no,
                    student.name,
                    student.father_name,
                    student.mother_name,
                    student.address,
                    student.phone_no,
                    student.email,
                ),
            )

    def get_by_roll_no(self, roll_no: int) -> Student:
        """Get a student by roll number. Raises NotFoundError if not found."""
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT roll_no, name, father_name, mother_name, address, phone_no, email "
                "FROM student WHERE roll_no=?",
                (roll_no,),
            )
            row = cursor.fetchone()
            if not row:
                raise NotFoundError(f"Student with roll number {roll_no} not found")
            return Student(
                roll_no=row[0],
                name=row[1],
                father_name=row[2],
                mother_name=row[3],
                address=row[4],
                phone_no=row[5],
                email=row[6],
            )

    def get_all(self) -> list[Student]:
        """Get all students."""
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT roll_no, name, father_name, mother_name, address, phone_no, email FROM student"
            )
            rows = cursor.fetchall()
            return [
                Student(
                    roll_no=row[0],
                    name=row[1],
                    father_name=row[2],
                    mother_name=row[3],
                    address=row[4],
                    phone_no=row[5],
                    email=row[6],
                )
                for row in rows
            ]

    def update(self, student: Student) -> None:
        """Update an existing student. Raises NotFoundError if not found."""
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT roll_no FROM student WHERE roll_no=?", (student.roll_no,)
            )
            if not cursor.fetchone():
                raise NotFoundError(f"Student with roll number {student.roll_no} not found")

            cursor.execute(
                "UPDATE student SET name=?, father_name=?, mother_name=?, "
                "address=?, phone_no=?, email=? WHERE roll_no=?",
                (
                    student.name,
                    student.father_name,
                    student.mother_name,
                    student.address,
                    student.phone_no,
                    student.email,
                    student.roll_no,
                ),
            )

    def delete(self, roll_no: int) -> None:
        """Delete a student. Raises NotFoundError if not found."""
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT roll_no FROM student WHERE roll_no=?", (roll_no,)
            )
            if not cursor.fetchone():
                raise NotFoundError(f"Student with roll number {roll_no} not found")

            cursor.execute("DELETE FROM student WHERE roll_no=?", (roll_no,))


class ExamRepository:
    """Handles all EXAM table operations."""

    def __init__(self, db: Database) -> None:
        self.db = db

    def create(self, exam: Exam) -> None:
        """Insert a new exam record. Raises DuplicateError if exam exists for roll_no."""
        with self.db.cursor() as cursor:
            # Verify student exists
            cursor.execute(
                "SELECT roll_no FROM student WHERE roll_no=?", (exam.roll_no,)
            )
            if not cursor.fetchone():
                raise NotFoundError(f"Student with roll number {exam.roll_no} not found")

            # Check for existing exam
            cursor.execute(
                "SELECT roll_no FROM exam WHERE roll_no=?", (exam.roll_no,)
            )
            if cursor.fetchone():
                raise DuplicateError(f"Exam record for roll number {exam.roll_no} already exists")

            cursor.execute(
                "INSERT INTO exam (roll_no, name, class, section, total_marks, percentage, grade) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    exam.roll_no,
                    exam.name,
                    exam.class_,
                    exam.section,
                    exam.total_marks,
                    exam.percentage,
                    exam.grade,
                ),
            )

    def get_by_roll_no(self, roll_no: int) -> Exam:
        """Get exam by roll number. Raises NotFoundError if not found."""
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT id, roll_no, name, class, section, total_marks, percentage, grade "
                "FROM exam WHERE roll_no=?",
                (roll_no,),
            )
            row = cursor.fetchone()
            if not row:
                raise NotFoundError(f"Exam record for roll number {roll_no} not found")
            return Exam(
                id=row[0],
                roll_no=row[1],
                name=row[2],
                class_=row[3],
                section=row[4],
                total_marks=row[5],
                percentage=row[6],
                grade=row[7],
            )

    def get_all(self) -> list[Exam]:
        """Get all exam records."""
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT id, roll_no, name, class, section, total_marks, percentage, grade FROM exam"
            )
            rows = cursor.fetchall()
            return [
                Exam(
                    id=row[0],
                    roll_no=row[1],
                    name=row[2],
                    class_=row[3],
                    section=row[4],
                    total_marks=row[5],
                    percentage=row[6],
                    grade=row[7],
                )
                for row in rows
            ]

    def update(self, exam: Exam) -> None:
        """Update an exam record. Raises NotFoundError if not found."""
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT roll_no FROM exam WHERE roll_no=?", (exam.roll_no,)
            )
            if not cursor.fetchone():
                raise NotFoundError(f"Exam record for roll number {exam.roll_no} not found")

            cursor.execute(
                "UPDATE exam SET name=?, class=?, section=?, total_marks=?, "
                "percentage=?, grade=? WHERE roll_no=?",
                (
                    exam.name,
                    exam.class_,
                    exam.section,
                    exam.total_marks,
                    exam.percentage,
                    exam.grade,
                    exam.roll_no,
                ),
            )

    def delete(self, roll_no: int) -> None:
        """Delete an exam record. Raises NotFoundError if not found."""
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT roll_no FROM exam WHERE roll_no=?", (roll_no,)
            )
            if not cursor.fetchone():
                raise NotFoundError(f"Exam record for roll number {roll_no} not found")

            cursor.execute("DELETE FROM exam WHERE roll_no=?", (roll_no,))
