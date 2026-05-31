"""Dashboard page with analytics."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import plotly.express as px
import pandas as pd
from app import get_services
from student_management.seed import seed_database


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

    # Seed data button
    st.divider()
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🌱 Load Demo Data"):
            count = seed_database(student_service, exam_service)
            if count > 0:
                st.success(f"Added {count} records!")
                st.rerun()
            else:
                st.info("Demo data already loaded.")
    with col2:
        st.caption("Populates sample students and exam records for demonstration.")

    st.divider()

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Grade Distribution")
        if exams:
            grade_counts = {}
            for grade in ["A", "B", "C", "D", "F"]:
                grade_counts[grade] = sum(1 for e in exams if e.grade == grade)
            grade_df = pd.DataFrame({
                "Grade": list(grade_counts.keys()),
                "Count": list(grade_counts.values()),
            })
            fig = px.bar(
                grade_df,
                x="Grade",
                y="Count",
                color="Grade",
                color_discrete_map={"A": "#4CAF50", "B": "#2196F3", "C": "#FF9800", "D": "#F44336", "F": "#9C27B0"},
                title="Grade Distribution",
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No exam data yet.")

    with col2:
        st.subheader("Class Distribution")
        if exams:
            class_counts = {}
            for e in exams:
                key = f"Class {e.class_}"
                class_counts[key] = class_counts.get(key, 0) + 1
            class_df = pd.DataFrame({
                "Class": list(class_counts.keys()),
                "Count": list(class_counts.values()),
            })
            fig = px.bar(
                class_df,
                x="Class",
                y="Count",
                color="Class",
                title="Class Distribution",
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
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
