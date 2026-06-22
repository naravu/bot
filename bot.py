# duckai_pro_code_bot.py
# pip install streamlit ddgs

import streamlit as st
from ddgs import DDGS

# Page config
st.set_page_config(
    page_title="DuckAI Pro Code Bot",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: #fafafa;
    }
    .chat-bubble-user {
        background-color: #1f77b4;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .chat-bubble-bot {
        background-color: #2ca02c;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💻 DuckAI Pro Code Bot")
st.caption("Your AI‑style coding assistant powered by DuckDuckGo")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history with styled bubbles
for role, text in st.session_state["messages"]:
    if role == "user":
        st.markdown(f"<div class='chat-bubble-user'>You: {text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot'>DuckAI:<br>{text}</div>", unsafe_allow_html=True)

# Input box
query = st.text_input("💬 Ask your coding question:")

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
                response_text += f"**{title}**\n\n```{lang}\n{snippet}\n```\n[🔗 Read more]({url})\n\n---\n"
                if lang == "python":
                    code_snippet = snippet
            else:
                response_text += f"**{title}**\n\n{snippet}\n\n[🔗 Read more]({url})\n\n---\n"

        if not response_text:
            response_text = "⚠️ Sorry, I couldn’t find relevant code snippets this time."

        # Save bot response
        st.session_state["messages"].append(("bot", response_text))

        st.rerun()

# If last response contained Python code, allow execution
if st.session_state["messages"]:
    last_role, last_text = st.session_state["messages"][-1]
    if last_role == "bot" and "```python" in last_text:
        st.subheader("▶️ Run Python Code")
        code_input = st.text_area(
            "Edit or run the Python snippet:",
            value=last_text.split("```python")[1].split("```")[0],
            height=200
        )
        if st.button("Execute"):
            try:
                exec_locals = {}
                exec(code_input, {}, exec_locals)
                st.success("✅ Execution successful!")
                if exec_locals:
                    st.json(exec_locals)
            except Exception as e:
                st.error(f"❌ Error: {e}")
