import os
from PIL import Image

import streamlit as st
from streamlit_option_menu import option_menu

from gemini_utility import (load_gemini_pro_model,
                            gemini_pro_vision_response,
                            embedding_model_response,
                            gemini_pro_response)


# Get the working directory
working_directory = os.path.dirname(os.path.abspath(__file__))

# Settins up the page configuration
st.set_page_config(
    page_title="Kunle AI",
    page_icon="🧠",
    layout="centered"
)

with st.sidebar:
    selected = option_menu("Kunle AI",
                           ["ChatBot",
                            "Image Captioning",
                            "Embed text",
                            "Ask me anything"],
                            menu_icon = "robot", icons=["chat-dots-fill", "image-fill",
                                                        "textarea-t", "patch-question-fill"],
                            default_index=0)

#function to translate role between gemini-pro and streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role
    

if selected == "ChatBot":
    model = load_gemini_pro_model()

    # Initialize chat session/history in streamlit if not already present
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    #streamlit page title
    st.title("🤖 ChatBot")

    # Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # input field for user's message
    user_prompt = st.chat_input("Ask KunleAI...")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Display Gemini_pro response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)



# Image Captioning Page
if selected == "Image Captioning":

    # Streamlit page title
    st.title("📷 Snap Narrate")
    uploaded_image = st.file_uploader("upload an image...", type=["jpg", "jpeg", "png"])

    if st.button("Generate Caption"):
        if uploaded_image is not None:
            image = Image.open(uploaded_image)

            col1, col2 = st.columns(2)

            with col1:
                resized_image = image.resize((800, 500))
                st.image(resized_image)

            default_prompt = "write a short caption for this image"

            # Getting the response from gemini-pro-vision model
            caption = gemini_pro_vision_response(default_prompt, image)

            with col2:
                st.info(caption)
        else:
            st.error("Please upload an image before generating a caption.")



# Text embedding page
if selected == "Embed text":

    st.title("🔠 Embed Text")

    # Input text box
    input_text = st.text_area(label="", placeholder="Enter the text to get embeddings")

    if st.button("get Embeddings"):
        response = embedding_model_response(input_text)
        st.markdown(response)


# Question answering page
if selected == "Ask me anything":

    st.title("❓ Ask Kunle a question")

    # text box to enter prompt
    user_prompt = st.text_area(label="", placeholder="Ask Kunle-AI...")

    if st.button("Get an answer"):
        response = gemini_pro_response(user_prompt)
        st.markdown(response)