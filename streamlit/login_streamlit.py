# login_streamlit.py
import streamlit as st
from authentication import *

def display_login_page():
    # Add custom CSS for styling
    st.markdown(
        """
        <style>
        .switch-buttons {
            display: flex;
            justify-content: space-around;
            width: 100%;
        }

        .switch-buttons button {
            flex: 1;
            padding: 10px;
            border: none;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s ease;
            border-radius: 10px;
            background-color: lightgray;
        }

        .switch-buttons button.active {
            background-color: orange;
            color: white;
        }

        .input-box {
            margin-bottom: 15px;
        }

        input {
            width: 100%;
            padding: 10px;
            border: 1px solid #007bff;
            border-radius: 5px;
        }

        button {
            width: 100%;
            padding: 10px;
            border: none;
            border-radius: 5px;
            background-color: #007bff;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background-color: #0056b3;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Initialize session state to track the active form
    if "form_type" not in st.session_state:
        st.session_state.form_type = "Login"  # Default to the login form

    # Function to handle form switching
    def switch_form(form):
        st.session_state.form_type = form

    st.markdown('<div class="switch-buttons">', unsafe_allow_html=True)

    # Login and Signup Buttons side by side
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", key="login_btn", help="Switch to Login"):
            switch_form("Login")

    with col2:
        if st.button("Signup", key="signup_btn", help="Switch to Signup"):
            switch_form("Signup")

    st.markdown('</div>', unsafe_allow_html=True)  # Close switch buttons

    # Display the correct form based on selection
    if st.session_state.form_type == "Login":
        st.header("Login Form")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            if login_username and login_password:
                login_user(login_username, login_password)
                if st.session_state.logged_in:
                    st.session_state.user = login_username
                    return True  # Indicate successful login
            else:
                st.error("Please enter both username and password.")
                return False  # Indicate unsuccessful login
    else:
        st.header("Signup Form")
        signup_username = st.text_input("Username", key="signup_username")
        signup_password = st.text_input("Password", type="password", key="signup_password")

        if st.button("Signup"):
            if signup_username and signup_password:
                register_user(signup_username, signup_password)
            else:
                st.error("Please enter both email and password")

    return False  # Indicate no login has occurred
