import streamlit as st
from duckai import DuckAI

# Initialize DuckAI
duckai = DuckAI()

# Streamlit UI
st.title("DuckAI WebApp 🦆🤖")

# Input box for user question
question = st.text_input("Ask DuckAI:", placeholder="Type your question here...")

# Button to submit
if st.button("Get Answer"):
    if question.strip():
        # Call DuckAI
        results = duckai.chat(question)
        st.subheader("Answer:")
        st.write(results)
    else:
        st.warning("Please enter a question before submitting.")
