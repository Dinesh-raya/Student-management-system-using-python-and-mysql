"""Students CRUD page."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from student_management.models import Student
from student_management.exceptions import AppError, ValidationError, NotFoundError, DuplicateError
from app import get_services


def display_student_form(student: Student | None = None) -> Student | None:
    """Display student form. Returns Student if submitted, None otherwise."""
    with st.form("student_form", clear_on_submit=True):
        roll_no = st.number_input(
            "Roll No",
            min_value=1,
            value=student.roll_no if student else 1,
            disabled=student is not None,
        )
        name = st.text_input("Name", value=student.name if student else "")
        father_name = st.text_input("Father's Name", value=student.father_name if student else "")
        mother_name = st.text_input("Mother's Name", value=student.mother_name if student else "")
        address = st.text_input("Address", value=student.address if student else "")
        phone_no = st.text_input("Phone No", value=student.phone_no if student else "")
        email = st.text_input("Email", value=student.email if student else "")

        submitted = st.form_submit_button("Update" if student else "Add")

        if submitted:
            return Student(
                roll_no=roll_no,
                name=name,
                father_name=father_name,
                mother_name=mother_name,
                address=address,
                phone_no=phone_no,
                email=email,
            )
    return None


def main():
    st.set_page_config(page_title="Students", page_icon="👨‍🎓", layout="wide")
    st.title("👨‍🎓 Students")

    student_service, _ = get_services()

    # Sidebar for mode selection
    mode = st.sidebar.radio("Action", ["View All", "Add Student", "Edit Student", "Delete Student"])

    if mode == "View All":
        st.subheader("All Students")
        students = student_service.list_students()

        if not students:
            st.info("No students found. Add one using the sidebar.")
            return

        # Search
        search = st.text_input("Search by name or roll number")
        if search:
            students = [
                s for s in students
                if search.lower() in s.name.lower() or str(s.roll_no) == search
            ]

        # Display as table
        if students:
            data = [
                {
                    "Roll No": s.roll_no,
                    "Name": s.name,
                    "Father's Name": s.father_name,
                    "Mother's Name": s.mother_name,
                    "Address": s.address,
                    "Phone": s.phone_no,
                    "Email": s.email,
                }
                for s in students
            ]
            st.dataframe(data, use_container_width=True)

            # CSV export
            import pandas as pd
            df = pd.DataFrame(data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="students.csv",
                mime="text/csv",
            )

    elif mode == "Add Student":
        st.subheader("Add New Student")
        student = display_student_form()
        if student:
            try:
                student_service.create_student(student)
                st.success(f"Student {student.name} added successfully!")
            except AppError as e:
                st.error(str(e))

    elif mode == "Edit Student":
        st.subheader("Edit Student")
        students = student_service.list_students()
        if not students:
            st.info("No students to edit.")
            return

        roll_options = {f"{s.name} (Roll #{s.roll_no})": s.roll_no for s in students}
        selected = st.selectbox("Select Student", list(roll_options.keys()))

        if selected:
            roll_no = roll_options[selected]
            student = student_service.get_student(roll_no)
            updated = display_student_form(student)
            if updated:
                try:
                    student_service.update_student(updated)
                    st.success(f"Student {updated.name} updated successfully!")
                except AppError as e:
                    st.error(str(e))

    elif mode == "Delete Student":
        st.subheader("Delete Student")
        students = student_service.list_students()
        if not students:
            st.info("No students to delete.")
            return

        roll_options = {f"{s.name} (Roll #{s.roll_no})": s.roll_no for s in students}
        selected = st.selectbox("Select Student", list(roll_options.keys()))

        if selected:
            roll_no = roll_options[selected]
            student = student_service.get_student(roll_no)
            st.warning(f"Are you sure you want to delete **{student.name}** (Roll #{roll_no})?")
            if st.button("Delete", type="primary"):
                try:
                    student_service.delete_student(roll_no)
                    st.success(f"Student {student.name} deleted successfully!")
                    st.rerun()
                except AppError as e:
                    st.error(str(e))


if __name__ == "__main__":
    main()
