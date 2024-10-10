import streamlit as st
from chatbot.chatbot_response import *

def chatbot():
    # Initialize session state for chat history, selected option, and option click flag
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "selected_option" not in st.session_state:
        st.session_state.selected_option = None  # Initialize selected_option

    if "current_menu" not in st.session_state:
        st.session_state.current_menu = None  # Keep track of current menu

    if "option_clicked" not in st.session_state:
        st.session_state.option_clicked = False  # Initialize option clicked flag
        
    # Check if an option was clicked
    if st.session_state.option_clicked:
        handle_option(st.session_state.selected_option)
    else:
        # Show the correct menu based on the user's last selection
        if st.session_state.current_menu == 'recruitment':
            display_options(recruitment_qns_list, 10)
        elif st.session_state.current_menu == 'visualization':
            display_options(visualizations_list, 20)
        else:
            # Show the main menu only if no submenu is active
            display_options(menu_list, 0)

    # Display chat messages
    display_messages()
