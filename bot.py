# pip install streamlit ddgs

import streamlit as st
from ddgs import DDGS

st.title("💻 DuckDuckGo Code Bot")

# Input field for coding question
query = st.text_input("Ask me a coding question:")

if st.button("Search Code"):
    if query.strip():
        with DDGS() as ddgs:
            results = ddgs.text(query + " site:stackoverflow.com OR site:github.com", max_results=5)
            
            st.subheader("🔎 Top Code Results")
            for r in results:
                st.write(f"**Title:** {r.get('title')}")
                st.write(f"**URL:** {r.get('href')}")
                st.write(f"**Snippet:** {r.get('body')}")
                st.markdown("---")
    else:
        st.warning("Please enter a coding question.")

# pip install streamlit ddgs

import streamlit as st
from ddgs import DDGS

st.title("DuckDuckGo Search with DDGS")

# Input field for search query
query = st.text_input("Enter your search query:")

# Button to trigger search
if st.button("Search"):
    if query.strip():
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=5)
            st.subheader("Top Results")
            for r in results:
                # Display each result nicely
                st.write(f"**Title:** {r.get('title')}")
                st.write(f"**URL:** {r.get('href')}")
                st.write(f"**Body:** {r.get('body')}")
                st.markdown("---")
    else:
        st.warning("Please enter a query before searching.")
