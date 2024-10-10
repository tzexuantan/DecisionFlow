from openai import OpenAI
import streamlit as st

def chatbot2():

    def handleUserInput(userInput):
        #if userInput:
        st.session_state.messagesList.append({"role": "user", "content": userInput})
        with st.chat_message("user"):
            st.markdown(userInput)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {
                        "role": message["role"], 
                        "content": message["content"]
                    }
                    for message in st.session_state.messagesList
                ],
                stream=True,
            )
            response = st.write_stream(stream)

        st.session_state.messagesList.append({"role": "assistant", "content": response})


    def initializeSessionStateVariables():
        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = OPENAI_MODEL_TYPE

        if "messagesList" not in st.session_state:
            st.session_state.messagesList = []
            st.session_state.messagesList.append({"role": "system", "content": SYSTEM_ROLE})


    def displayMessageHistory():
        for message in st.session_state.messagesList:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


    OPENAI_MODEL_TYPE = "gpt-4o-mini"
    SYSTEM_ROLE = "You are a helpful assistant that answers recruitment-related questions to students \
                planning for their professional future in the field of tech in the context of Singapore. VAR_A is 3"

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    initializeSessionStateVariables()

    st.title("Chatbot2")
    st.write("Select from a pre-determined list of questions from either button category shown below or ask the chatbot directly!")

    userInput2 = ""

    with st.expander("Recruitment-related Questions"):
        print("triggered or not")
        question = "Recommend degrees or skills for a job position."
        if st.button(question):
            print("how does this work?")
            userInput2 = question

    # with st.expander("Visualization-type Questions"):
    #     if st.button("Recommend degrees or skills for a job position.2"):
    #         print("how does this work?2")

    displayMessageHistory()

    userInput = st.chat_input("Message Chatbot")
    # print("userInput: ", userInput)
    # print(type(userInput))
    # print("the messagesList: ", st.session_state.messagesList)

    if userInput2 != "":
        print("this got triggered")
        handleUserInput(userInput2)

    else:
        if userInput:
            handleUserInput(userInput)
