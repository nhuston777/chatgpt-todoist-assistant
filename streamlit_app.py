import streamlit as st
from main import run_productivity_assistant
from todoist_api import count_open_tasks
from openai_api import get_task_improvement_suggestions

st.set_page_config(page_title="GPT Todoist Assistant", layout="centered")

# Authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("🔐 Enter app password", type="password")
    if password == st.secrets["APP_PASSWORD"]:
        st.session_state.authenticated = True
        st.rerun()
    elif password:
        st.error("❌ Incorrect password")
        st.stop()

st.title("🧠 Todoist Assistant Powered by ChatGPT")

# Reset button
if st.button("🔁 Start Over"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Step 1: Show total tasks and get analysis input
if "task_limit" not in st.session_state:
    with st.spinner("Counting your open Todoist tasks..."):
        total = count_open_tasks()
    st.markdown(f"You currently have **{total} open tasks** in Todoist.")
    st.session_state["task_limit"] = st.number_input(
        "How many tasks would you like to analyze?",
        min_value=1,
        max_value=total,
        value=min(10, total),
        step=1
    )

# Step 2: Analyze Tasks
if st.button("📋 Analyze Tasks"):
    with st.spinner("Analyzing tasks with GPT..."):
        run_productivity_assistant(st.session_state["task_limit"])

# Step 3: Display GPT summary
if "summary" in st.session_state:
    st.markdown("### 🔍 GPT Summary")
    for paragraph in st.session_state["summary"].split("\n\n"):
        st.markdown(paragraph.strip())

# Step 4: Ask how many suggestions to generate
if "messages" in st.session_state and not st.session_state.get("pending"):
    num = st.number_input("How many suggestions would you like?", min_value=1, max_value=20, value=3)

    if st.button("🤖 Get Suggestions"):
        with st.spinner("Generating suggestions..."):
            suggestions = get_task_improvement_suggestions(st.session_state["messages"], num)
            lines = [line.strip() for line in suggestions.splitlines() if line.strip().startswith("- ")]
            st.session_state["pending"] = lines
            st.session_state["approved"] = []

# Step 5: Interactive suggestion approval
if st.session_state.get("pending"):
    suggestion = st.session_state["pending"][0]
    st.markdown("### ✨ Suggestion")
    st.write(suggestion)

    col1, col2 = st.columns(2)
    if col1.button("✅ Approve"):
        st.session_state["approved"].append(st.session_state["pending"].pop(0))
        st.rerun()
    if col2.button("⏭️ Skip"):
        st.session_state["pending"].pop(0)
        st.rerun()

# Step 6: Final summary and download
if st.session_state.get("pending") == [] and "approved" in st.session_state:
    st.markdown("### ✅ Approved Suggestions")

    if st.session_state["approved"]:
        for item in st.session_state["approved"]:
            st.success(item)
    else:
        st.warning("No suggestions approved.")
        st.write("None")

    summary = st.session_state.get("summary", "")
    approved = st.session_state["approved"]
    suggestion_text = "\n".join(approved) if approved else "None"
    download_text = f"GPT Summary:\n{summary}\n\nApproved Suggestions:\n{suggestion_text}"

    st.download_button("📄 Download Summary + Suggestions", download_text, file_name="gpt_todoist_summary.txt")
