import streamlit as st
from visualizations import *
from chatbot.support_functions import *
import json
import os


# Ensure that set_page_config is at the top of the script
#t.set_page_config(page_title="DecisionFlow", layout="wide")

#Recruitment-related question required variables
# Load the roles and skills from JSON file
current_dir = os.path.dirname(os.path.abspath(__file__))
ROLES_AND_SKILLS_FILE_PATH = os.path.join(current_dir, "../../dataset/roles_and_associated_skills.json")
with open(ROLES_AND_SKILLS_FILE_PATH, 'r') as file:
    roles_and_skills = json.load(file)

job_roles_list = list(roles_and_skills['jobRoles'].keys())

#Visualizations required variables
indeed_df = initialize_indeed_dataset()
bar_column_to_plot = "Skill"

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
    st.session_state.waiting_for_job_role = True

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

# Function to display options dynamically (for main options, not for job roles)
def display_options(options_list, add):
    st.write("Please select an option:")
    for idx, option in enumerate(options_list):
        if st.button(option, key=f"option_{idx+add}"):
            st.session_state.selected_option = option
            st.session_state.option_clicked = True
            st.rerun()  # Only rerun after option is clicked

    # Add a back button to return to the main menu
    if st.session_state.current_menu is not None and st.button("Back to Main Menu"):
        st.session_state.current_menu = None
        st.session_state.selected_job_role = None
        st.session_state.waiting_for_job_role = False
        st.rerun()

# New function to handle job role selections separately
# def display_job_roles():
#     st.write("Select a job role:")
#     for idx, job_role in enumerate(job_roles_list):
#         if st.button(job_role, key=f"job_role_{idx}"):
#             st.session_state.selected_job_role = job_role
#             st.session_state.waiting_for_job_role = False  # Stop showing job roles after selection
#             break  # Exit loop to show skills

def handle_option(option):
    if option:
        st.session_state.messages.append({"user": "user", "message": option})

        if option == menu_list[0]:  # Recruitment-related Questions
            st.session_state.current_menu = 'recruitment'
            st.session_state.messages.append({"user": "bot", "message":"What would you like to know about recruitment?"})
        elif option == menu_list[1]:  # Visualizations
            st.session_state.current_menu = 'visualization'
            st.session_state.messages.append({"user": "bot", "message": "Here are some charts we have! Do you visit the visualizations tab for more info!"})
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
    print(f"handle_recruitment_option called with option: {option}")

    # Print the session state to understand what's going on
    print("Session state before anything:", st.session_state)

    if option == recruitment_qns_list[0]:  # Recommend degrees or skills for a job position

        # Initialize session state variables only if not already set
        if st.session_state.waiting_for_job_role == False:
            st.session_state.waiting_for_job_role = True
            print("waiting_for_job_role initialized as True")  # Debugging

        if 'selected_job_role' not in st.session_state:
            st.session_state.selected_job_role = None
            print("selected_job_role initialized as None")  # Debugging

        # Ensure dropdown shows up when waiting_for_job_role is True
        if st.session_state.waiting_for_job_role:
            # Display job role options as a dropdown
            job_roles_list = ['Software Engineer', 'Data Scientist', 'DevOps Engineer', 'UX/UI Designer', 'Cybersecurity Analyst']
            selected_job_role = st.selectbox("Please select a job role:", job_roles_list)
            print(f"Dropdown rendered: {selected_job_role}")  # Debugging to check if dropdown is rendering
            
            # Confirm the selection using a button
            if st.button("Confirm Selection"):
                # Once the button is clicked, store the selected job role and stop showing the dropdown
                st.session_state.selected_job_role = selected_job_role
                st.session_state.waiting_for_job_role = False
                print(f"Job role '{selected_job_role}' selected, setting waiting_for_job_role to False")  # Debugging
                st.experimental_rerun()  # Force a rerun to refresh the UI after confirmation

        # Debugging: See if we skip to this point unintentionally
        print("Step 1 completed or skipped. Current session state:", st.session_state)

        # Step 2: Show skills for the selected job role if one is selected
        if st.session_state.selected_job_role is not None and not st.session_state.waiting_for_job_role:
            selected_role = st.session_state.selected_job_role
            print(f"Selected role is: {selected_role}")  # Debugging

            # Fetch and display the skills for the selected job role
            if selected_role in roles_and_skills['jobRoles']:
                skills = roles_and_skills['jobRoles'][selected_role]
                skills_message = f"Skills required for {selected_role}:\n- " + '\n- '.join(skills)

                # Add the skills message to the bot's responses
                st.session_state.messages.append({"user": "bot", "message": skills_message})

                # Display the skills
                st.write(skills_message)

                # Optionally, reset the flow and allow the user to select another job role
                if st.button("Select another job role"):
                    st.session_state.selected_job_role = None
                    st.session_state.waiting_for_job_role = True
                    print("Resetting selected job role and waiting for job role")  # Debugging
                    st.experimental_rerun()

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

    # Add the bot response to session state messages (only if we handled other options)
    if option != recruitment_qns_list[0]:
        st.session_state.messages.append({"user": "bot", "message": bot_response})

    # Debugging: Final state of session state
    print("Session state after everything:", st.session_state)
# Function to handle visualization options


def handle_visualization_option(option):
    if option == visualizations_list[0]:
        if bar_column_to_plot in indeed_df.columns:
            category_counts = indeed_df[bar_column_to_plot].value_counts()

            if not category_counts.empty:
                # Try to generate the bar chart as a matplotlib figure
                try:
                    fig, ax = plt.subplots(figsize=(10,9))
                    category_counts.plot(kind='bar', ax=ax, color='skyblue')
                    chart_title = 'Distribution of Skills'
                    ax.set_title(chart_title)
                    ax.set_xlabel(bar_column_to_plot)
                    ax.set_ylabel('Frequency')

                    save_chart_as_img(ax, chart_title)
                    # st.session_state['chart_fig'] = fig  # Store the figure in session_state
                    
                    # print("Chart figure successfully saved to session state.")  # Debugging
                    # # Always check and display the chart using st.pyplot if it exists in session state
                    # if 'chart_fig' in st.session_state:
                    #     chart = st.pyplot(st.session_state['chart_fig'])  # Display the chart using st.pyplot
                    #     print("Chart displayed using st.pyplot.")
                        
                    
                    # Attach the chart to the bot's response and store in session state

                except Exception as e:
                    st.error(f"An error occurred while generating the chart: {e}")
                    print(f"Error: {e}")  # Debugging
            else:
                st.warning("No data available to display the chart.")
        else:
            st.error(f"Column '{bar_column_to_plot}' not found.")
    # else:
    #     st.session_state.messages.append({"user": "bot", "message": bot_response})

    print(st.session_state)

# Function to display chat messages with bubbles
def display_messages():
    # Define styles for the scrollable container and message boxes
    st.html(
        """
        <style>
        .scrollable-container {
            height: 400px; /* Set a fixed height */
            overflow-y: auto; /* Enable vertical scrolling */
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 10px;
            background-color: #f9f9f9;
        }
        .message-bot {
            text-align: left;
            margin: 10px;
        }
        .message-user {
            text-align: right;
            margin: 10px;
        }
        .message-box {
            display: inline-block;
            padding: 10px 15px;
            border-radius: 20px;
        }
        .message-box-bot {
            background-color: #F0F0F0;
            color: black;
        }
        .message-box-user {
            background-color: #D4EDDA;
            color: black;
        }
        </style>
        """,
        #unsafe_allow_html=True
    )

    # Start the scrollable container and build the entire content as a single string
    chat_html = '<div class="scrollable-container">'

    # Loop through the messages stored in session state and build the HTML content
    for msg in st.session_state.messages:
        if msg['user'] == "user":
            chat_html += f"""
                <div class="message-user">
                    <div class="message-box message-box-user">
                        <b>You:</b> {msg['message']}
                    </div>
                </div>
            """
        else:
            print("Bot message", st.session_state)
            chat_html += f"""
                <div class="message-bot">
                    <div class="message-box message-box-bot">
                        <b>Bot:</b> {msg['message']}
                    </div>
                </div>
            """

    # Close the scrollable container div
    #chat_html += '</div>'

    # Render the entire chat HTML in one go
    st.html(chat_html)



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

