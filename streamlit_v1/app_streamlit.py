import streamlit as st
import time
from chatbot.chatbot_response import *
from chatbot.commands.chatbot import chatbot
from streamlit_option_menu import option_menu
from login_streamlit import display_login_page  # Import the function
from authentication import create_table

create_table()
# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False  
if "show_login" not in st.session_state:
    st.session_state.show_login = False
if "user" not in st.session_state:
    st.session_state.user = False
# if "redirect_message" not in st.session_state:
#     st.session_state.redirect_message = ""

# Main app page
def show_main_app():
    st.set_page_config(page_title="DecisionFlow", layout="wide")

    with st.sidebar:
        if st.session_state.user:
            st.markdown(
                f"""
                <style>
                .custom-text {{
                    font-size:30px;
                    font-weight:bold;
                    color:blue;
                }}
                </style>
                <span class="custom-text">Hi, {st.session_state.user}</span>!
                """,
                unsafe_allow_html=True
            )
        selected = option_menu(
            menu_title="DecisionFlow",
            options=["Home", "Chatbot", "Visualisation", "Login / Sign Up"],
            icons=["house", "android", "clipboard-data"],
            menu_icon="app-indicator",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "fafafa"},
                "icon": {"color": "blue", "font-size": "25px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#B5C3F9"}
            }
        )
    
    
    # Only show main content if not on the login page
    if selected == "Home":
        st.write("Welcome to the Home Page!")
    elif selected == "Chatbot":
        chatbot()
    elif selected == "Visualisation":
        st.write("Visualisation content goes here.")
    elif selected == "Login / Sign Up":
        if not st.session_state.logged_in:
            logged_in = display_login_page()
            if logged_in:
                st.session_state.logged_in = True
                time.sleep(1)
                st.rerun()

show_main_app()  # Show main app if logged in
