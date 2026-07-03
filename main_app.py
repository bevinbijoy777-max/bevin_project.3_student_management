import streamlit as st
import sqlite3
import pandas as pd

# -----------------------------
# Database Connection
# -----------------------------
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
age INTEGER,
gender TEXT,
course TEXT,
marks REAL
)
""")

conn.commit()

# -----------------------------
# Functions
# -----------------------------

def add_student(name, age, gender, course, marks):
    cursor.execute(
        "INSERT INTO students(name,age,gender,course,marks) VALUES(?,?,?,?,?)",
        (name, age, gender, course, marks)
    )
    conn.commit()


def view_students():
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    return data


def delete_student(student_id):
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()


def update_student(student_id, name, age, gender, course, marks):
    cursor.execute("""
    UPDATE students
    SET name=?, age=?, gender=?, course=?, marks=?
    WHERE id=?
    """, (name, age, gender, course, marks, student_id))
    conn.commit()


# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(page_title="Student Record Management System",
                   page_icon="🎓",
                   layout="wide")

st.title("🎓 Student Record Management System")

menu = ["Home", "Add Student", "View Students", "Update Student", "Delete Student"]

choice = st.sidebar.selectbox("Menu", menu)

# -----------------------------
# Home
# -----------------------------

if choice == "Home":

    st.subheader("Dashboard")

    data = view_students()

    df = pd.DataFrame(data,
                      columns=["ID", "Name", "Age", "Gender", "Course", "Marks"])

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Students", len(df))

    if len(df) > 0:

        with col2:
            st.metric("Average Marks", round(df["Marks"].mean(), 2))

        st.dataframe(df, use_container_width=True)

# -----------------------------
# Add Student
# -----------------------------

elif choice == "Add Student":

    st.subheader("Add Student")

    name = st.text_input("Student Name")

    age = st.number_input("Age", 1, 100)

    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    course = st.text_input("Course")

    marks = st.number_input("Marks", 0.0, 100.0)

    if st.button("Add Student"):

        add_student(name, age, gender, course, marks)

        st.success("Student Added Successfully")

# -----------------------------
# View Students
# -----------------------------

elif choice == "View Students":

    st.subheader("Student Records")

    data = view_students()

    df = pd.DataFrame(data,
                      columns=["ID", "Name", "Age", "Gender", "Course", "Marks"])

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download CSV",
        csv,
        "students.csv",
        "text/csv"
    )

# -----------------------------
# Update Student
# -----------------------------

elif choice == "Update Student":

    st.subheader("Update Student")

    data = view_students()

    ids = [i[0] for i in data]

    if ids:

        selected = st.selectbox("Select Student ID", ids)

        record = [x for x in data if x[0] == selected][0]

        name = st.text_input("Name", record[1])

        age = st.number_input("Age", 1, 100, value=record[2])

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"],
            index=["Male", "Female", "Other"].index(record[3])
        )

        course = st.text_input("Course", record[4])

        marks = st.number_input(
            "Marks",
            0.0,
            100.0,
            value=float(record[5])
        )

        if st.button("Update"):

            update_student(selected, name, age, gender, course, marks)

            st.success("Record Updated Successfully")

    else:

        st.warning("No records available.")

# -----------------------------
# Delete Student
# -----------------------------

elif choice == "Delete Student":

    st.subheader("Delete Student")

    data = view_students()

    ids = [i[0] for i in data]

    if ids:

        selected = st.selectbox("Student ID", ids)

        if st.button("Delete"):

            delete_student(selected)

            st.success("Student Deleted Successfully")

    else:

        st.warning("No records available.")

conn.close()
