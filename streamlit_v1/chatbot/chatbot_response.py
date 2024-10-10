import streamlit as st
import json
import os

# Load the roles and skills from JSON file
current_dir = os.path.dirname(os.path.abspath(__file__))
ROLES_AND_SKILLS_FILE_PATH = os.path.join(current_dir, "../../dataset/roles_and_associated_skills.json")
with open(ROLES_AND_SKILLS_FILE_PATH, 'r') as file:
    roles_and_skills = json.load(file)

job_roles_list = list(roles_and_skills['jobRoles'].keys())

# Ensure that set_page_config is at the top of the script
st.set_page_config(page_title="DecisionFlow", layout="wide")

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_menu' not in st.session_state:
    st.session_state.current_menu = None
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = None
if 'option_clicked' not in st.session_state:
    st.session_state.option_clicked = False
if 'selected_job_role' not in st.session_state:
    st.session_state.selected_job_role = None
if 'waiting_for_job_role' not in st.session_state:
    st.session_state.waiting_for_job_role = False
if 'job_prompt_shown' not in st.session_state:
    st.session_state.job_prompt_shown = None

menu_list = [
    "Recruitment-related Questions",
    "Visualizations?",
    "Just wanna have a chat?"
]

recruitment_qns_list = [
    "Recommend degrees or skills for a job position",
    "Jobs I can apply for with my qualifications",
    "Find a job quickly after graduation",
    "Does my school affect my employment rate?",
    "Industries in high demand"
]

visualizations_list = [
    "What is the distribution of skills that are highly sought by companies?",
    "What are the top 3 aspects of employer branding that are most important to new graduates?",
    "What are the entry-level jobs for new graduates in AI?"
]

# Function to display options
def display_options(options_list, add):
    st.write("Please select an option:")
    for idx, option in enumerate(options_list):
        if st.button(option, key=f"option_{idx+add}"):
            st.session_state.selected_option = option
            st.session_state.option_clicked = True  # Set flag to indicate an option was clicked
            st.rerun()  # Force rerun after option is clicked

    # Add a back button to return to the main menu
    if st.session_state.current_menu != None and st.button("Back to Main Menu"):
        st.session_state.current_menu = None  # Reset the current menu
        st.session_state.selected_job_role = None  # Reset job role selection
        st.session_state.waiting_for_job_role = False  # Reset waiting state
        st.rerun()  # Trigger a rerun to refresh the options

def handle_option(option):
    if option:
        st.session_state.messages.append({"user": "user", "message": option})

        if option == menu_list[0]:  # Recruitment-related Questions
            st.session_state.current_menu = 'recruitment'
        elif option == menu_list[1]:  # Visualizations
            st.session_state.current_menu = 'visualization'
        elif option == menu_list[2]:  # Chat
            st.session_state.current_menu = 'chat'
            st.session_state.messages.append({"user": "bot", "message": "I'm here to chat!"})

        elif option in recruitment_qns_list:  # Handle recruitment options
            handle_recruitment_option(option)
        elif option in visualizations_list:  # Handle visualization options
            handle_visualization_option(option)

        st.session_state.option_clicked = False
        st.rerun()

# Function to handle recruitment options
def handle_recruitment_option(option):
    if option == recruitment_qns_list[0]:  # Recommend degrees or skills for a job position
        bot_response = "What jobs are you looking for?"
        st.session_state.messages.append({"user": "bot", "message": bot_response})

        # Set the flag to true, which will show job roles
        st.session_state.waiting_for_job_role = True

    if st.session_state.waiting_for_job_role:
        # Display job role options dynamically
        st.write("Select a job role:")
        for idx, job_role in enumerate(job_roles_list):
            if st.button(job_role, key=f"job_role_{idx}"):
                st.session_state.selected_job_role = job_role
                st.session_state.waiting_for_job_role = False  # Stop showing job role buttons
                st.rerun()

    if st.session_state.selected_job_role:
        # Show skills associated with the selected job role
        selected_role = st.session_state.selected_job_role
        skills = roles_and_skills['jobRoles'][selected_role]
        skills_message = f"Skills required for {selected_role}:\n- " + '\n- '.join(skills)
        st.session_state.messages.append({"user": "bot", "message": skills_message})
        st.session_state.selected_job_role = None  # Reset job role selection

    # Handle other recruitment options
    elif option == recruitment_qns_list[1]:
        bot_response = "Based on your qualifications, you can apply for jobs such as Data Analyst, Software Developer, or Marketing Specialist."
    elif option == recruitment_qns_list[2]:
        bot_response = "To find a job quickly, consider internships, networking events, and job fairs as they can provide valuable opportunities."
    elif option == recruitment_qns_list[3]:
        bot_response = "Yes, the reputation and resources of your school can influence your employment opportunities."
    elif option == recruitment_qns_list[4]:
        bot_response = "Currently, industries such as Technology, Healthcare, and Renewable Energy are in high demand."
    else:
        bot_response = "I'm sorry, I didn't understand that option."

    st.session_state.messages.append({"user": "bot", "message": bot_response})

# Function to handle visualization options
def handle_visualization_option(option):
    bot_response = "Feature currently not available."
    st.session_state.messages.append({"user": "bot", "message": bot_response})

# Function to display chat messages with bubbles
def display_messages():
    for msg in st.session_state.messages:
        if msg['user'] == "user":
            st.markdown(
                f"""
                <div style='text-align: right; margin: 10px;'>
                    <div style='display: inline-block; background-color: #D4EDDA; color: black; padding: 10px 15px; border-radius: 20px;'>
                        <b>You:</b> {msg['message']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style='text-align: left; margin: 10px;'>
                    <div style='display: inline-block; background-color: #F0F0F0; color: black; padding: 10px 15px; border-radius: 20px;'>
                        <b>Bot:</b> {msg['message']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

# Display the main menu
st.title("Chat Interface with Text Bubbles")

if not st.session_state.current_menu:
    display_options(menu_list, 0)

elif st.session_state.current_menu == 'recruitment':
    display_options(recruitment_qns_list, len(menu_list))
elif st.session_state.current_menu == 'visualization':
    display_options(visualizations_list, len(menu_list) + len(recruitment_qns_list))

# Add a text input for user to enter a message if chatting
if st.session_state.current_menu == 'chat':
    user_message = st.text_input("Type your message here:", key="user_input")

    if st.button("Send"):
        if user_message:
            st.session_state.messages.append({"user": "user", "message": user_message})
            st.session_state.messages.append({"user": "bot", "message": "This is a response from the bot."})
            st.rerun()

display_messages()
