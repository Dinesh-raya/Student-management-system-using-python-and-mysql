"""Student Management System — Streamlit Dashboard."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
from student_management.config import get_config
from student_management.db import Database
from student_management.repositories import StudentRepository, ExamRepository
from student_management.services import StudentService, ExamService


@st.cache_resource
def init_database():
    """Initialize database connection (cached across reruns)."""
    config = get_config()
    db = Database(config)
    db.initialize()
    return db


def get_services():
    """Get service instances."""
    db = init_database()
    student_repo = StudentRepository(db)
    exam_repo = ExamRepository(db)
    return StudentService(student_repo), ExamService(exam_repo)


def main():
    st.set_page_config(
        page_title="Student Management System",
        page_icon="🎓",
        layout="wide",
    )

    st.title("🎓 Student Management System")
    st.markdown("Welcome to the Student Management System dashboard.")

    student_service, exam_service = get_services()

    # Metrics
    col1, col2, col3 = st.columns(3)

    students = student_service.list_students()
    exams = exam_service.list_exams()

    with col1:
        st.metric("Total Students", len(students))

    with col2:
        st.metric("Total Exams", len(exams))

    with col3:
        if exams:
            avg_pct = sum(e.percentage for e in exams) / len(exams)
            st.metric("Average Percentage", f"{avg_pct:.1f}%")
        else:
            st.metric("Average Percentage", "N/A")

    st.divider()

    # Grade distribution
    if exams:
        st.subheader("Grade Distribution")
        grade_counts = {}
        for e in exams:
            grade_counts[e.grade] = grade_counts.get(e.grade, 0) + 1

        st.bar_chart(grade_counts)
    else:
        st.info("No exam records yet. Add some on the Exams page.")

    # Recent records
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Recent Students")
        if students:
            for s in students[-5:]:
                with st.expander(f"{s.name} (Roll #{s.roll_no})"):
                    st.write(f"**Father:** {s.father_name}")
                    st.write(f"**Mother:** {s.mother_name}")
                    st.write(f"**Phone:** {s.phone_no}")
                    if s.email:
                        st.write(f"**Email:** {s.email}")
        else:
            st.info("No students yet. Add some on the Students page.")

    with col2:
        st.subheader("Recent Exams")
        if exams:
            for e in exams[-5:]:
                with st.expander(f"{e.name} — Grade {e.grade}"):
                    st.write(f"**Class:** {e.class_}, Section {e.section}")
                    st.write(f"**Total Marks:** {e.total_marks}")
                    st.write(f"**Percentage:** {e.percentage}%")
        else:
            st.info("No exam records yet. Add some on the Exams page.")


if __name__ == "__main__":
    main()
