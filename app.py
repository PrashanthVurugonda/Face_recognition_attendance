import streamlit as st
import subprocess
import json
import os
import pandas as pd

# Constants for admin credentials
ADMIN_USERNAME = "Admin"
ADMIN_PASSWORD = "AU@1234"

# Load user credentials and other data
def load_data():
    if os.path.exists('data/user_credentials.json'):
        with open('data/user_credentials.json', 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    os.makedirs('data', exist_ok=True)
    with open('data/user_credentials.json', 'w') as f:
        json.dump(data, f)

# Load attendance data
def load_attendance_data(date):
    file_path = f"Attendance/Attendance_{date}.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return None

# Save appeals
def save_appeal(roll_no, appeal):
    appeals = load_appeals()
    appeals[roll_no] = appeal
    os.makedirs('data', exist_ok=True)
    with open('data/appeals.json', 'w') as f:
        json.dump(appeals, f)

def load_appeals():
    if os.path.exists('data/appeals.json'):
        with open('data/appeals.json', 'r') as f:
            return json.load(f)
    return {}

# Home page
def home_page():
    st.title("Welcome to Facetrack")
    if st.button("Login", key="home_login_button"):
        st.session_state.page = "login"

# Login page
def login_page():
    st.sidebar.header("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type='password')

    if st.sidebar.button("Login", key="login_button"):
        user_data = load_data()
        if (username == ADMIN_USERNAME and password == ADMIN_PASSWORD) or (
                username in user_data and user_data[username]['password'] == password):
            role = "admin" if username == ADMIN_USERNAME else user_data[username]['role']
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role
            st.session_state.page = role  # Redirect to the role page
        else:
            st.sidebar.error("Invalid credentials. Please try again.")

# Admin page for registering users
def admin_page():
    st.title("Admin Page")
    st.subheader("Register Users")

    username = st.text_input("Enter Username")
    roll_no = st.text_input("Enter Roll No./EMP ID")
    department = st.text_input("Enter Department Name")
    password = st.text_input("Enter Password", type='password')
    role = st.selectbox("Select Role", ['student', 'teacher', 'H.O.D'])

    if st.button("Register", key="register_button"):
        user_data = load_data()
        user_data[username] = {
            "roll_no": roll_no,
            "department": department,
            "password": password,
            "role": role
        }
        save_data(user_data)
        st.success(f"User {username} registered successfully!")

    if role == 'student':
        if st.button("Capture Face", key="capture_face_button"):
            # Replace with the appropriate path to your `add_faces.py` file
            script_path = r"C:/Users/vurug/OneDrive/Desktop/Face recog/add_faces.py"
            subprocess.Popen(["python", script_path, username, roll_no, department])

# Teacher page
def teacher_page(username):
    st.title("Teacher Page")
    st.subheader(f"Welcome, {username}")

    working_days = st.number_input("Enter Number of Working Days", min_value=1, max_value=31)
    if st.button("Declare Working Days", key="declare_working_days_button"):
        st.success(f"Working days declared: {working_days}")

    if st.button("Capture Attendance", key="capture_attendance_button"):
        # Replace with the appropriate path to your attendance capture script
        script_path = r"C:/Users/vurug/OneDrive/Desktop/Face recog/test.py"
        subprocess.Popen(["python", script_path])

# H.O.D page
def hod_page():
    st.title("H.O.D Page")
    st.subheader("Analyze Attendance Data")
    today_date = pd.to_datetime("today").strftime("%d-%m-%Y")
    attendance_data = load_attendance_data(today_date)

    if attendance_data is not None:
        attendance_percentage = attendance_data.groupby('ROLL_NO').size() / len(attendance_data) * 100
        report_data = attendance_data[['NAME', 'ROLL_NO']].copy()
        report_data['ATTENDANCE_PERCENTAGE'] = attendance_percentage

        if st.button("Download Attendance Report", key="download_report_button"):
            report_file = f"Attendance_Report_{today_date}.csv"
            report_data.to_csv(report_file, index=False)
            st.success(f"Attendance report downloaded: {report_file}")
    else:
        st.error("No attendance data found for today.")

# Student page
def student_page(username):
    st.title("Student Page")
    st.subheader(f"Welcome, {username}")
    
    today_date = pd.to_datetime("today").strftime("%d-%m-%Y")
    attendance_data = load_attendance_data(today_date)

    if attendance_data is not None:
        student_data = attendance_data[attendance_data['ROLL_NO'] == username]
        if not student_data.empty:
            st.write(student_data)
        else:
            st.write("No attendance record found for today.")

    appeal = st.text_area("Appeal for Incorrect Attendance")
    if st.button("Submit Appeal", key="submit_appeal_button"):
        save_appeal(username, appeal)
        st.success("Your appeal has been submitted!")

# Main function to run the app
def main():
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.page = "home"

    # Determine which page to display
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "login":
        login_page()
    elif st.session_state.logged_in:
        if st.session_state.role == 'admin':
            admin_page()
        elif st.session_state.role == 'teacher':
            teacher_page(st.session_state.username)
        elif st.session_state.role == 'H.O.D':
            hod_page()
        elif st.session_state.role == 'student':
            student_page(st.session_state.username)

if __name__ == "__main__":
    main()
