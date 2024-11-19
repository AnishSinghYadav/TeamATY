import streamlit as st
from pymongo import MongoClient
import re
import hashlib

# MongoDB connection setup
client = MongoClient('mongodb+srv://anishsinghyadav2909:4PjO6WZekjc61xNh@cluster0.bbx0f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['internship_db']

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register Function
def register_user():
    st.title('Register for SVVV Internship')
    with st.form("register_form"):
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit_button = st.form_submit_button("Register")

        if submit_button:
            if password == confirm_password and len(password) >= 8 and re.match("^[A-Za-z]*$", password):
                if not db.users.find_one({"email": email}) and not db.users.find_one({"phone": phone}):
                    db.users.insert_one({"email": email, "phone": phone, "password": hash_password(password)})
                    st.success("Registration successful")
                else:
                    st.error("Email or Phone number already exists")
            else:
                st.error("Password validation failed")

# Sign-In Function
def login_user():
    st.title('Sign In to SVVV Internship')
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            user = db.users.find_one({"email": email})
            if user and user['password'] == hash_password(password):
                st.success("Login successful")
                # Redirect to student or mentor dashboard
            else:
                st.error("Invalid credentials")

# Main Page Navigation
page = st.sidebar.selectbox("Choose your role", ["Register", "Sign In"])

if page == "Register":
    register_user()
elif page == "Sign In":
    login_user()
