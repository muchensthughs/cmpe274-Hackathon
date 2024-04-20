import streamlit as st
from file_reader import file_reader


st.title("CMPE 274 Hackathon - SOFI-2023.pdf")

if  "sofi_chatbot" not in st.session_state:
    st.session_state["sofi_chatbot"] = file_reader("/Users/muchen/Downloads/SOFI-2023.pdf")

# Initialize chat history
if "sofi_messages" not in st.session_state:
    st.session_state.sofi_messages = []

# Display chat messages from history on app rerun
for message in st.session_state.sofi_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Question"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.sofi_messages.append({"role": "user", "content": prompt})

    response = st.session_state["sofi_chatbot"].ask_doc(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.sofi_messages.append({"role": "assistant", "content": response})
