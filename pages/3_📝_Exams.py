"""Exams CRUD page."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from student_management.models import Exam
from student_management.exceptions import AppError
from app import get_services


VALID_GRADES = ["A", "B", "C", "D", "F"]


def display_exam_form(exam: Exam | None = None) -> Exam | None:
    """Display exam form. Returns Exam if submitted, None otherwise."""
    with st.form("exam_form", clear_on_submit=True):
        roll_no = st.number_input(
            "Roll No",
            min_value=1,
            value=exam.roll_no if exam else 1,
            disabled=exam is not None,
        )
        name = st.text_input("Student Name", value=exam.name if exam else "")
        class_ = st.number_input("Class", min_value=1, value=exam.class_ if exam else 1)
        section = st.text_input("Section", value=exam.section if exam else "")
        total_marks = st.number_input("Total Marks", min_value=0, value=exam.total_marks if exam else 0)
        percentage = st.number_input(
            "Percentage",
            min_value=0.0,
            max_value=100.0,
            value=exam.percentage if exam else 0.0,
            step=0.1,
        )
        grade = st.selectbox(
            "Grade",
            VALID_GRADES,
            index=VALID_GRADES.index(exam.grade) if exam and exam.grade in VALID_GRADES else 0,
        )

        submitted = st.form_submit_button("Update" if exam else "Add")

        if submitted:
            return Exam(
                roll_no=roll_no,
                name=name,
                class_=class_,
                section=section,
                total_marks=total_marks,
                percentage=percentage,
                grade=grade,
            )
    return None


def main():
    st.set_page_config(page_title="Exams", page_icon="📝", layout="wide")
    st.title("📝 Exams")

    _, exam_service = get_services()

    # Sidebar for mode selection
    mode = st.sidebar.radio("Action", ["View All", "Add Exam", "Edit Exam", "Delete Exam"])

    if mode == "View All":
        st.subheader("All Exam Records")
        exams = exam_service.list_exams()

        if not exams:
            st.info("No exam records found. Add one using the sidebar.")
            return

        # Search
        search = st.text_input("Search by name or roll number")
        if search:
            exams = [
                e for e in exams
                if search.lower() in e.name.lower() or str(e.roll_no) == search
            ]

        # Display as table with progress bars for percentage
        if exams:
            data = [
                {
                    "Roll No": e.roll_no,
                    "Name": e.name,
                    "Class": e.class_,
                    "Section": e.section,
                    "Total Marks": e.total_marks,
                    "Percentage": e.percentage,
                    "Grade": e.grade,
                }
                for e in exams
            ]
            st.dataframe(
                data,
                use_container_width=True,
                column_config={
                    "Percentage": st.column_config.ProgressColumn(
                        "Percentage",
                        min_value=0,
                        max_value=100,
                        format="%.1f%%",
                    ),
                    "Grade": st.column_config.TextColumn("Grade"),
                },
            )

    elif mode == "Add Exam":
        st.subheader("Add New Exam Record")
        exam = display_exam_form()
        if exam:
            try:
                exam_service.create_exam(exam)
                st.success(f"Exam record for {exam.name} added successfully!")
            except AppError as e:
                st.error(str(e))

    elif mode == "Edit Exam":
        st.subheader("Edit Exam Record")
        exams = exam_service.list_exams()
        if not exams:
            st.info("No exam records to edit.")
            return

        roll_options = {f"{e.name} (Roll #{e.roll_no})": e.roll_no for e in exams}
        selected = st.selectbox("Select Exam Record", list(roll_options.keys()))

        if selected:
            roll_no = roll_options[selected]
            exam = exam_service.get_exam(roll_no)
            updated = display_exam_form(exam)
            if updated:
                try:
                    exam_service.update_exam(updated)
                    st.success(f"Exam record for {updated.name} updated successfully!")
                except AppError as e:
                    st.error(str(e))

    elif mode == "Delete Exam":
        st.subheader("Delete Exam Record")
        exams = exam_service.list_exams()
        if not exams:
            st.info("No exam records to delete.")
            return

        roll_options = {f"{e.name} (Roll #{e.roll_no})": e.roll_no for e in exams}
        selected = st.selectbox("Select Exam Record", list(roll_options.keys()))

        if selected:
            roll_no = roll_options[selected]
            exam = exam_service.get_exam(roll_no)
            st.warning(f"Are you sure you want to delete exam record for **{exam.name}** (Roll #{roll_no})?")
            if st.button("Delete", type="primary"):
                try:
                    exam_service.delete_exam(roll_no)
                    st.success(f"Exam record for {exam.name} deleted successfully!")
                    st.rerun()
                except AppError as e:
                    st.error(str(e))


if __name__ == "__main__":
    main()
