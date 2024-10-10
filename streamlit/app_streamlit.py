APP_NAME = "DecisionFlow"

import streamlit as st
st.set_page_config(page_title=APP_NAME, layout="wide")

import time
from enum import Enum
# from dotenv import load_dotenv
# import os

# load_dotenv()

from chatbot.chatbot2 import chatbot2

from chatbot.chatbot_response import *
from chatbot.commands.chatbot import chatbot
from visualizations import visualizations
from streamlit_option_menu import option_menu
from login_streamlit import display_login_page  # Import the function
from authentication import create_table

# All other functions and setup code follow after the set_page_config call


class Page(Enum):
    HOME = "Home"
    CHATBOT = "Chatbot"
    CHATBOT_2 = "Chatbot2"
    VISUALIZATION = "Visualization"
    LOGIN_SIGN_UP = "Login / Sign Up"


class Icon(Enum):
    HOME = "house"
    CHATBOT = "android"
    CHATBOT_2 = "chat-left-quote"
    VISUALIZATION = "clipboard-data"
    LOGIN_SIGN_UP = "android"


def initialize_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False  

    if "show_login" not in st.session_state:
        st.session_state.show_login = False

    if "user" not in st.session_state:
        st.session_state.user = False


def greet_user_if_user_loggedin():
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
                <span class="custom-text">Hi, {st.session_state.user}!</span>
                """,
                unsafe_allow_html=True
            )


# Main app page
def show_main_app():
    with st.sidebar:
        greet_user_if_user_loggedin()
        selected = option_menu(
            menu_title=APP_NAME,
            options=[Page.HOME.value, Page.CHATBOT.value, Page.CHATBOT_2.value, Page.VISUALIZATION.value, Page.LOGIN_SIGN_UP.value],
            icons=[Icon.HOME.value, Icon.CHATBOT.value, Icon.CHATBOT_2.value, Icon.VISUALIZATION.value],
            menu_icon="app-indicator",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "fafafa"},
                "icon": {"color": "blue", "font-size": "25px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#B5C3F9"}
            }
        )
    
    print("selected: ", selected)
    
    # Only show main content if not on the login page
    if selected == Page.HOME.value:
        st.write("Welcome to the Home Page!")
    elif selected == Page.CHATBOT.value:
        chatbot()
    elif selected == Page.CHATBOT_2.value:
        chatbot2()
    elif selected == Page.VISUALIZATION.value:
        visualizations()
    elif selected == Page.LOGIN_SIGN_UP.value:
        if not st.session_state.logged_in:
            logged_in = display_login_page()
            if logged_in:
                st.session_state.logged_in = True
                time.sleep(1)
                st.rerun()
        else:
            st.write("You are already logged in!")


create_table()
initialize_session_state()
show_main_app()  # Show main app if logged in

print("does this get reprinted when app is refreshed?")
print(st.session_state)
print()
