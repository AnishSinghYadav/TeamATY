import streamlit as st
import pandas as pd
import numpy as np

# Sample Data for Interns, Mentors, and Admin (for demo purposes)
interns_data = [
    {'Name': 'John Doe', 'Age': 21, 'Contact': '1234567890', 'Qualifications': 'B.Tech', 'Email': 'john@example.com', 'College': 'SVVV', 'Internship': 'Data Science', 'Company': 'ABC Corp', 'Start Date': '2024-06-01', 'Stipend': '20000'},
    {'Name': 'Jane Smith', 'Age': 22, 'Contact': '0987654321', 'Qualifications': 'B.Tech', 'Email': 'jane@example.com', 'College': 'SVVV', 'Internship': 'Web Development', 'Company': 'XYZ Ltd', 'Start Date': '2024-07-01', 'Stipend': '15000'}
]

mentors_data = [
    {'Name': 'Dr. A Sharma', 'Contact': '1122334455', 'Email': 'asharma@mentor.com'},
    {'Name': 'Prof. B Patel', 'Contact': '6677889900', 'Email': 'bpatel@mentor.com'}
]

# Role-based login details (for demo purposes)
users = {
    'admin': {'password': 'adminpass', 'role': 'Admin'},
    'mentor1': {'password': 'mentorpass', 'role': 'Mentor'},
    'intern1': {'password': 'internpass', 'role': 'Intern'}
}

# Global variable to store the user role (for demonstration purposes)
user_role = None

# Store the assignments (for demo purposes)
assignments = {}

# Function to clear session and logout
def logout():
    global user_role
    user_role = None
    st.session_state.clear()  # Clear session data
    st.rerun()  # Reload the page to reflect changes after logout

# Function for Admin Dashboard
def admin_dashboard():
    st.title("Admin Dashboard")
    st.write("Welcome, Admin!")

    # Graphical Data for Mentors and Interns
    mentor_count = len(mentors_data)
    intern_count = len(interns_data)

    # Create a bar chart to show the count of mentors and interns
    data = {'Role': ['Mentors', 'Interns'], 'Count': [mentor_count, intern_count]}
    df = pd.DataFrame(data)

    st.write("Mentor vs Intern Count")
    st.bar_chart(df.set_index('Role'))

    # Admin can assign mentors to interns here
    st.subheader("Assign Mentor to Intern")
    
    # Select an intern and assign a mentor
    intern_names = [intern['Name'] for intern in interns_data]
    mentor_names = [mentor['Name'] for mentor in mentors_data]
    
    selected_intern = st.selectbox("Select Intern", intern_names)
    selected_mentor = st.selectbox("Select Mentor", mentor_names)
    
    if st.button("Assign Mentor"):
        assignments[selected_intern] = selected_mentor
        st.success(f"Assigned {selected_mentor} to {selected_intern}")
    
    st.write("Assigned Mentors to Interns:")
    for intern, mentor in assignments.items():
        st.write(f"{intern} -> {mentor}")

# Function for Mentor Dashboard
def mentor_dashboard():
    st.title("Mentor Dashboard")
    st.write("Welcome, Mentor!")
    
    # Display assigned interns to the mentor
    st.subheader("Assigned Interns")
    assigned_interns = [intern for intern, mentor in assignments.items() if mentor == st.session_state['user_role']]
    
    if assigned_interns:
        for intern in assigned_interns:
            st.write(f"Intern Name: {intern}")
            st.write(f"Internship: {interns_data[intern]['Internship']}")
            st.write(f"Company: {interns_data[intern]['Company']}")
            st.write("------")
    else:
        st.write("No interns assigned.")

# Function for Intern Dashboard
def intern_dashboard():
    st.title("Intern Dashboard")
    st.write("Welcome, Intern!")
    
    # Display intern's details
    intern_name = st.session_state['user_role']
    intern_details = interns_data[intern_name]
    
    st.write(f"Name: {intern_details['Name']}")
    st.write(f"Age: {intern_details['Age']}")
    st.write(f"Internship: {intern_details['Internship']}")
    st.write(f"Company: {intern_details['Company']}")
    st.write("------")
    
    # Display mentor assigned to intern
    assigned_mentor = [mentor for intern, mentor in assignments.items() if intern == intern_name]
    if assigned_mentor:
        st.write(f"Assigned Mentor: {assigned_mentor[0]}")
    else:
        st.write("No mentor assigned yet.")

# Login function
def login():
    global user_role
    st.title("Login")

    # Login form
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        submit_button = st.form_submit_button("Login")

        if submit_button:
            # Validate user credentials
            if username in users and users[username]['password'] == password:
                user_role = users[username]['role']
                st.session_state['logged_in'] = True
                st.session_state['user_role'] = user_role
                st.success(f"Logged in as {username} ({user_role})")
                st.rerun()  # Reload the page to reflect changes after login
            else:
                st.error("Invalid credentials")

# Sidebar for user navigation
def sidebar():
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        st.sidebar.title("Navigation")
        # Display dashboard button based on the role
        if st.session_state['user_role'] == "Admin":
            st.sidebar.button("Admin Dashboard", on_click=admin_dashboard)
        elif st.session_state['user_role'] == "Mentor":
            st.sidebar.button("Mentor Dashboard", on_click=mentor_dashboard)
        elif st.session_state['user_role'] == "Intern":
            st.sidebar.button("Intern Dashboard", on_click=intern_dashboard)
        st.sidebar.button("Logout", on_click=logout)

# Main function to run the app
def main():
    st.title("SVVV Internship Management System")

    # Adding CSS for hover animations
    st.markdown("""
    <style>
    .stButton > button {
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        transition-duration: 0.4s;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #45a049;
        transform: scale(1.1);
    }

    .stTextInput input {
        font-size: 16px;
        border-radius: 5px;
    }

    .stTextInput label {
        font-size: 14px;
    }

    </style>
    """, unsafe_allow_html=True)

    # Show login form if not logged in
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        login()
    else:
        # Show sidebar for user navigation
        sidebar()

        # Show role-based dashboard
        if st.session_state['user_role'] == "Admin":
            admin_dashboard()
        elif st.session_state['user_role'] == "Mentor":
            mentor_dashboard()
        elif st.session_state['user_role'] == "Intern":
            intern_dashboard()

# Run the app
if __name__ == "__main__":
    main()
