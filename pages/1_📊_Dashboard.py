"""Dashboard page with analytics."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from app import get_services


def main():
    st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
    st.title("📊 Dashboard")

    student_service, exam_service = get_services()

    students = student_service.list_students()
    exams = exam_service.list_exams()

    # Key metrics
    col1, col2, col3 = st.columns(3)

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

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Grade Distribution")
        if exams:
            grade_counts = {}
            for grade in ["A", "B", "C", "D", "F"]:
                grade_counts[grade] = sum(1 for e in exams if e.grade == grade)
            st.bar_chart(grade_counts)
        else:
            st.info("No exam data yet.")

    with col2:
        st.subheader("Class Distribution")
        if exams:
            class_counts = {}
            for e in exams:
                key = f"Class {e.class_}"
                class_counts[key] = class_counts.get(key, 0) + 1
            st.bar_chart(class_counts)
        else:
            st.info("No exam data yet.")

    st.divider()

    # Top performers
    st.subheader("Top Performers")
    if exams:
        top = sorted(exams, key=lambda e: e.percentage, reverse=True)[:5]
        for i, e in enumerate(top, 1):
            st.write(f"**{i}. {e.name}** — {e.percentage}% (Grade {e.grade})")
    else:
        st.info("No exam data yet.")


if __name__ == "__main__":
    main()
