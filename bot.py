# duckai_live_coding_bot_pro.py
# pip install streamlit ddgs

import streamlit as st
from ddgs import DDGS

# --- Page Config ---
st.set_page_config(
    page_title="DuckAI Live Coding Bot",
    page_icon="💻",
    layout="wide"
)

# --- Sidebar ---
st.sidebar.title("⚙️ Control Panel")
st.sidebar.markdown("Navigate and customize your experience.")

# Sidebar options
view_mode = st.sidebar.radio("Choose View:", ["Chat", "Run Code", "Settings"])
clear_chat = st.sidebar.button("🗑️ Clear Chat History")

if clear_chat:
    st.session_state["messages"] = []

# --- Main Title ---
st.title("💻 DuckAI Live Coding Bot")
st.write("Ask me coding questions (Python, HTML, JavaScript, etc.) and I'll fetch helpful answers. For Python, you can even run the code live!")

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- Chat View ---
if view_mode == "Chat":
    # Display chat history
    st.subheader("💬 Conversation")
    for role, text in st.session_state["messages"]:
        if role == "user":
            st.markdown(f"<div style='color:#1E90FF'><b>You:</b> {text}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background:#f0f0f0;padding:10px;border-radius:8px'><b>DuckAI:</b><br>{text}</div>", unsafe_allow_html=True)

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
                        code_snippet = snippet
                else:
                    response_text += f"**{title}**\n\n{snippet}\n\n[Read more]({url})\n\n---\n"

            if not response_text:
                response_text = "Sorry, I couldn’t find relevant code snippets this time."

            # Save bot response
            st.session_state["messages"].append(("bot", response_text))
            st.rerun()

# --- Run Code View ---
elif view_mode == "Run Code":
    st.subheader("▶️ Run Python Code")
    if st.session_state["messages"]:
        last_role, last_text = st.session_state["messages"][-1]
        if last_role == "bot" and "```python" in last_text:
            code_input = st.text_area(
                "Edit or run the Python snippet:",
                value=last_text.split("```python")[1].split("```")[0],
                height=200
            )
            if st.button("Execute"):
                try:
                    exec_locals = {}
                    exec(code_input, {}, exec_locals)
                    st.success("Execution successful!")
                    st.write("Output variables:", exec_locals)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.info("No Python code available from the last response.")

# --- Settings View ---
elif view_mode == "Settings":
    st.subheader("⚙️ Preferences")
    theme = st.selectbox("Theme:", ["Light", "Dark"])
    st.write(f"Selected theme: {theme}")
