import os
import json

import streamlit as st
import openai

# configuring streamlit page settings
st.set_page_config(
    page_title="GPT-4o Chat",
    page_icon="💬",
    layout="centered"
)

# Initalize chat session in streamlit if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history =[]
    
# Streamlit page title
st.title("🤖 GPT-4o - ChatBot")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
# Input field for user's message
user_prompt = st.chat_input("Ask GPT-4o...")

if user_prompt:
# add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    
# Send user's message to GPT-4o and get a response
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            *st.session_state.chat_history
        ]
    )
    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
    
# Display GPT-4o's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)