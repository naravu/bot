# duckai_live_coding_bot.py
# pip install streamlit ddgs

import streamlit as st
from ddgs import DDGS

st.set_page_config(page_title="DuckAI Live Coding Bot", page_icon="💻")

st.title("💻 DuckAI Live Coding Bot")
st.write("Ask me coding questions (Python, HTML, JavaScript, etc.) and I'll fetch helpful answers. For Python, you can even run the code live!")

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
        code_snippet = None
        lang = None

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

            if lang:
                response_text += f"**{title}**\n\n```{lang}\n{snippet}\n```\n[Read more]({url})\n\n---\n"
                if lang == "python":
                    code_snippet = snippet  # Save Python snippet for execution
            else:
                response_text += f"**{title}**\n\n{snippet}\n\n[Read more]({url})\n\n---\n"

        if not response_text:
            response_text = "Sorry, I couldn’t find relevant code snippets this time."

        # Save bot response
        st.session_state["messages"].append(("bot", response_text))

        st.rerun()

# If last response contained Python code, allow execution
if st.session_state["messages"]:
    last_role, last_text = st.session_state["messages"][-1]
    if last_role == "bot" and "```python" in last_text:
        st.subheader("▶️ Run Python Code")
        code_input = st.text_area("Edit or run the Python snippet:", value=last_text.split("```python")[1].split("```")[0])
        if st.button("Execute"):
            try:
                exec_locals = {}
                exec(code_input, {}, exec_locals)
                st.success("Execution successful!")
                st.write("Output variables:", exec_locals)
            except Exception as e:
                st.error(f"Error: {e}")
