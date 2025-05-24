import streamlit as st
from todoist_api import count_open_tasks, extract_task_descriptions
from openai_api import get_task_summary

st.set_page_config(page_title="GPT Todoist Assistant", layout="centered")

# 🔁 Reset button
if "authenticated" in st.session_state and st.session_state["authenticated"]:
    if st.button("🔁 Start Over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

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

# Step 2: Cache open task count
if "total_tasks" not in st.session_state:
    with st.spinner("🔄 Fetching task count from Todoist..."):
        st.session_state["total_tasks"] = count_open_tasks()

total_tasks = st.session_state["total_tasks"]
st.markdown(f"You currently have **{total_tasks} open tasks** in Todoist.")

# Step 3: Let user choose how many tasks to analyze
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

        # 🧹 Clear any previous GPT state
        for key in ["summary", "messages", "task_descriptions", "pending", "approved"]:
            if key in st.session_state:
                del st.session_state[key]

        st.rerun()

    st.stop()

# Step 4: Show confirmed input
st.success(f"✅ Task limit confirmed: {st.session_state['task_limit']} tasks")

# Step 5: Pull tasks and send to GPT
if "summary" not in st.session_state:
    with st.spinner("📋 Pulling tasks and sending to GPT..."):
        task_descriptions = extract_task_descriptions(limit=st.session_state["task_limit"])
        summary, messages = get_task_summary(task_descriptions)

        st.session_state["task_descriptions"] = task_descriptions
        st.session_state["summary"] = summary
        st.session_state["messages"] = messages
        st.session_state["approved"] = []
        st.session_state["pending"] = []
    st.rerun()

# Step 6: Display GPT summary
st.markdown("### 🔍 GPT Summary")
for paragraph in st.session_state["summary"].split("\n\n"):
    st.markdown(paragraph.strip())
