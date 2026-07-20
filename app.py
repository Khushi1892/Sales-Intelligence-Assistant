import streamlit as st

from chain import answer_question
st.set_page_config(
    page_title="Sales Intelligence Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Sales Intelligence Assistant")
st.write("Ask questions about sales data or company policies.")

question = st.text_input("Enter your question")
if st.button("Ask"):
    if question:
        with st.spinner("Thinking..."):
            answer = answer_question(question)
        st.success(answer)