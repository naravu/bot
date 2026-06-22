# duckai_live_coding_bot_pro_fixed.py
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
view_mode = st.sidebar.radio("Choose View:", ["Chat", "Run Code", "Settings"])
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state["messages"] = []

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- Fixed Search Bar ---
st.markdown("### 🔍 Ask DuckAI")
col1, col2 = st.columns([4,1])
with col1:
    query = st.text_input("Your coding question:", label_visibility="collapsed")
with col2:
    ask_button = st.button("Ask")

# --- Chat View ---
if view_mode == "Chat":
    st.subheader("💬 Conversation")

    # Scrollable results container
    with st.container():
        chat_area = st.container()
        chat_area.markdown(
            "<div style='max-height:400px;overflow-y:auto;padding:10px;border:1px solid #ddd;border-radius:8px;'>",
            unsafe_allow_html=True
        )

        for role, text in st.session_state["messages"]:
            if role == "user":
                st.markdown(f"<div style='color:#1E90FF'><b>You:</b> {text}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background:#f9f9f9;padding:10px;border-radius:8px'><b>DuckAI:</b><br>{text}</div>", unsafe_allow_html=True)

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
