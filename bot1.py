# duckai_live_coding_bot_pro_ui_v3.py
# pip install streamlit ddgs

import streamlit as st
from ddgs import DDGS

# --- Page Config ---
st.set_page_config(
    page_title="DuckAI Live Coding Bot",
    page_icon="💻",
    layout="wide"
)

# --- Custom CSS for professional look ---
st.markdown("""
<style>
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 14px;
    color: #ffffff;
    background-color: #000000;
}
.chat-container {
    max-height: 500px;
    overflow-y: auto;
    padding: 12px;
    border: 1px solid #444;
    border-radius: 8px;
    background-color: #000000; /* black background */
    color: #ffffff; /* white text */
}
.user-msg {
    color: #4da6ff; /* light blue for user */
    margin-bottom: 8px;
    font-weight: 500;
}
.bot-msg {
    background: #1c1c1c; /* dark gray for bot bubble */
    color: #ffffff;
    padding: 10px;
    border-radius: 6px;
    margin-bottom: 12px;
    font-size: 13px;
    line-height: 1.4;
}
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("⚙️ Control Panel")
view_mode = st.sidebar.radio("Choose View:", ["Chat", "Run Code", "Settings"])
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state["messages"] = []

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- Fixed Search Bar ---
col1, col2 = st.columns([5,1])
with col1:
    query = st.text_input("Your coding question:", label_visibility="collapsed", placeholder="Type your question here...")
with col2:
    ask_button = st.button("Ask")

# --- Chat View ---
if view_mode == "Chat":
    st.subheader("💬 Conversation")

    # Scrollable results container
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for role, text in st.session_state["messages"]:
        if role == "user":
            st.markdown(f"<div class='user-msg'>You: {text}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-msg'><b>DuckAI:</b><br>{text}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Handle query
    if ask_button and query.strip():
        st.session_state["messages"].append(("user", query))

        with DDGS() as ddgs:
            results = ddgs.text(query + " site:stackoverflow.com OR site:github.com", max_results=3)

        response_text = ""
        code_snippet = None
        lang = None

        for r in results:
            title = r.get("title", "")
            url = r.get("href", "")
            snippet = r.get("body", "")

            if "def " in snippet or "import " in snippet:
                lang = "python"
            elif "<" in snippet and ">" in snippet:
                lang = "html"
            elif "function" in snippet or "console.log" in snippet:
                lang = "javascript"

            if lang:
                response_text += f"**{title}**\n\n```{lang}\n{snippet}\n```\n[Read more]({url})\n\n---\n"
                if lang == "python":
                    code_snippet = snippet
            else:
                response_text += f"**{title}**\n\n{snippet}\n\n[Read more]({url})\n\n---\n"

        if not response_text:
            response_text = "Sorry, I couldn’t find relevant code snippets this time."

        st.session_state["messages"].append(("bot", response_text))
        st.rerun()

# --- Run Code View ---
elif view_mode == "Run Code":
    st.subheader("▶️ Run Python Code")

    # Always show manual input box
    manual_code = st.text_area("Write your own Python code:", height=200, placeholder="Enter Python code here...")
    if st.button("Execute Manual Code"):
        try:
            exec_locals = {}
            exec(manual_code, {}, exec_locals)
            st.success("Execution successful!")
            st.write("Output variables:", exec_locals)
        except Exception as e:
            st.error(f"Error: {e}")

    # If last response contained Python code, show it too
    if st.session_state["messages"]:
        last_role, last_text = st.session_state["messages"][-1]
        if last_role == "bot" and "```python" in last_text:
            code_input = st.text_area(
                "Edit or run the Python snippet from DuckAI:",
                value=last_text.split("```python")[1].split("```")[0],
                height=200
            )
            if st.button("Execute Snippet"):
                try:
                    exec_locals = {}
                    exec(code_input, {}, exec_locals)
                    st.success("Execution successful!")
                    st.write("Output variables:", exec_locals)
                except Exception as e:
                    st.error(f"Error: {e}")

# --- Settings View ---
elif view_mode == "Settings":
    st.subheader("⚙️ Preferences")
    theme = st.selectbox("Theme:", ["Light", "Dark"])
    st.write(f"Selected theme: {theme}")
