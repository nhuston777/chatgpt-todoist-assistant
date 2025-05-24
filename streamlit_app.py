import streamlit as st
from main import run_productivity_assistant
from todoist_api import count_open_tasks
from openai_api import get_task_improvement_suggestions

st.set_page_config(page_title="GPT Todoist Assistant", layout="centered")

# 🔐 Authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("🔐 Enter app password", type="password")
    if password == st.secrets.get("APP_PASSWORD"):
        st.session_state.authenticated = True
    elif password:
        st.error("❌ Incorrect password")
        st.stop()
    else:
        st.stop()

# 🧠 Header
st.title("🧠 Todoist Assistant Powered by ChatGPT")

# 🔁 Reset
if st.button("🔁 Start Over"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

# STEP 1: Show open task count and collect task limit input (no mutation yet)
with st.spinner("Counting open Todoist tasks..."):
    total_tasks = count_open_tasks()

st.markdown(f"You currently have **{total_tasks} open tasks** in Todoist.")
task_limit = st.number_input(
    "How many tasks would you like to analyze?",
    min_value=1,
    max_value=total_tasks,
    value=min(10, total_tasks),
    step=1
)

# STEP 2: Analyze button (mutates state on click)
if st.button("📋 Analyze Now"):
    st.session_state["task_limit"] = task_limit
    st.session_state["analysis_complete"] = False
    with st.spinner("Analyzing tasks with GPT..."):
        run_productivity_assistant(st.session_state["task_limit"])
        st.session_state["analysis_complete"] = True

# STEP 3: Show summary
if st.session_state.get("analysis_complete") and "summary" in st.session_state:
    st.markdown("### 🔍 GPT Summary")
    for paragraph in st.session_state["summary"].split("\n\n"):
        st.markdown(paragraph.strip())

# STEP 4: Suggestion generation
if st.session_state.get("messages") and not st.session_state.get("pending"):
    num = st.number_input("How many suggestions would you like?", min_value=1, max_value=20, value=3)

    if st.button("🤖 Get Suggestions"):
        with st.spinner("Generating suggestions..."):
            suggestions = get_task_improvement_suggestions(st.session_state["messages"], num)
            lines = [line.strip() for line in suggestions.splitlines() if line.strip().startswith("- ")]
            st.session_state["pending"] = lines
            st.session_state["approved"] = []

# STEP 5: Approve or skip
if st.session_state.get("pending"):
    current = st.session_state["pending"][0]
    st.markdown("### ✨ Suggestion")
    st.write(current)

    col1, col2 = st.columns(2)
    if col1.button("✅ Approve"):
        st.session_state["approved"].append(st.session_state["pending"].pop(0))
    if col2.button("⏭️ Skip"):
        st.session_state["pending"].pop(0)

# STEP 6: Final output
if st.session_state.get("pending") == [] and "approved" in st.session_state:
    st.markdown("### ✅ Approved Suggestions")

    if st.session_state["approved"]:
        for suggestion in st.session_state["approved"]:
            st.success(suggestion)
    else:
        st.warning("No suggestions approved.")
        st.write("None")

    summary = st.session_state.get("summary", "")
    approved_text = "\n".join(st.session_state["approved"]) if st.session_state["approved"] else "None"
    download_text = f"GPT Summary:\n{summary}\n\nApproved Suggestions:\n{approved_text}"

    st.download_button("📄 Download Summary + Suggestions", download_text, file_name="gpt_todoist_summary.txt")
