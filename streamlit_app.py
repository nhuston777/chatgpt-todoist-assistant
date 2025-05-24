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

# Step 2: Show open task count
with st.spinner("🔄 Fetching task count from Todoist..."):
    total_tasks = count_open_tasks()

st.markdown(f"You currently have **{total_tasks} open tasks** in Todoist.")

# Step 3: Let the user choose how many tasks to analyze
if "task_limit_confirmed" not in st.session_state:
    task_limit = st.number_input(
        "How many tasks would you like to analyze?",
        min_value=1,
        max_value=total_tasks,
        value=min(10, total_tasks),
        step=1,
        key="task_limit_input"
    )

    if st.button("✔️ Confirm Task Count"):
        st.session_state["task_limit"] = task_limit
        st.session_state["task_limit_confirmed"] = True
        st.experimental_rerun()

    st.stop()

# Display confirmed value
st.success(f"✅ Task limit confirmed: {st.session_state['task_limit']} tasks")
