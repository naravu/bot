# duckai_chat_code_bot.py
# pip install streamlit ddgs

import streamlit as st
from ddgs import DDGS

st.set_page_config(page_title="DuckAI Code Bot", page_icon="💻")

st.title("💻 DuckAI Chat Code Bot")
st.write("Ask me coding questions (Python, HTML, JavaScript, etc.) and I'll fetch helpful answers!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for role, text in st.session_state["messages"]:
    if role == "user":
        st.markdown(f"**You:** {text}")
    else:
        st.markdown(f"**DuckAI:**\n{text}")

# Input box
query = st.text_input("Your coding question:")

if st.button("Ask DuckAI"):
    if query.strip():
        # Save user query
        st.session_state["messages"].append(("user", query))

        # Perform search
        with DDGS() as ddgs:
            results = ddgs.text(query + " site:stackoverflow.com OR site:github.com", max_results=3)

        # Build response with syntax highlighting
        response_text = ""
        for r in results:
            title = r.get("title", "")
            url = r.get("href", "")
            snippet = r.get("body", "")

            # Detect language for highlighting
            if "def " in snippet or "import " in snippet:
                lang = "python"
            elif "<" in snippet and ">" in snippet:
                lang = "html"
            elif "function" in snippet or "console.log" in snippet:
                lang = "javascript"
            else:
                lang = ""

            if lang:
                response_text += f"**{title}**\n\n```{lang}\n{snippet}\n```\n[Read more]({url})\n\n---\n"
            else:
                response_text += f"**{title}**\n\n{snippet}\n\n[Read more]({url})\n\n---\n"

        if not response_text:
            response_text = "Sorry, I couldn’t find relevant code snippets this time."

        # Save bot response
        st.session_state["messages"].append(("bot", response_text))

        st.rerun()
