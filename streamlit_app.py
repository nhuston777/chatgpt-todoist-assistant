import streamlit as st
from todoist_api import count_open_tasks

st.set_page_config(page_title="GPT Todoist Assistant", layout="centered")

# Step 1: Authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("🔐 Enter app password", type="password")
    if password == st.secrets.get("APP_PASSWORD"):
        st.session_state.authenticated = True
        st.rerun()
    elif password:
        st.error("❌ Incorrect password")
        st.stop()
    else:
        st.stop()

st.title("🧠 Todoist Assistant Powered by ChatGPT")

# Step 2: Display open task count (no session state change yet)
with st.spinner("🔄 Fetching task count from Todoist..."):
    total_tasks = count_open_tasks()

st.markdown(f"You currently have **{total_tasks} open tasks** in Todoist.")
