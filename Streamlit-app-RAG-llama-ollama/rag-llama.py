import os
import streamlit as st
from doc_utility import get_answer

working_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Chat with Doc",
    page_icon="🗎",
    layout="centered"
)

st.title("Document Q&A - Llama 3 - Ollama")

uploaded_file = st.file_uploader(label="Upload your file Here", type=["PDF"])

user_query = st.text_input("Ask your question")

if st.button("RUN"):
    bytes_data = uploaded_file.read()
    file_name = uploaded_file.name

    # Save the file to the working directory
    file_path = os.path.join(working_dir, file_name)
    with open(file_path, "wb") as f:
        f.write(bytes_data)
    answer = get_answer(file_name, user_query)

    st.success(answer)