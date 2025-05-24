import streamlit as st

st.set_page_config(page_title="GPT Todoist Assistant", layout="centered")

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

from todoist_api import extract_task_descriptions
from openai_api import get_task_summary, get_task_improvement_suggestions


st.title("🧠 Todoist Assistant Powered by ChatGPT")

# Reset button
if st.button("🔁 Start Over"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

# Step 1: Task analysis input
task_limit = st.number_input("How many Todoist tasks should I analyze?", min_value=1, max_value=50, value=5)

if st.button("📋 Analyze Tasks"):
    with st.spinner("Pulling your tasks from Todoist..."):
        task_descriptions = extract_task_descriptions(limit=task_limit)
        summary, messages = get_task_summary(task_descriptions)

    st.session_state["messages"] = messages
    st.session_state["task_descriptions"] = task_descriptions
    st.session_state["summary"] = summary  # ✅ Save summary
    st.session_state["approved"] = []
    st.session_state["pending"] = []

# ✅ Show GPT Summary (Always display if it exists)
if "summary" in st.session_state:
    st.markdown("### 🔍 GPT Summary")
    for paragraph in st.session_state["summary"].split("\n\n"):
        st.markdown(paragraph.strip())

# Step 2: Suggestions input
if "messages" in st.session_state and not st.session_state.get("pending"):
    num = st.number_input("How many suggestions would you like?", min_value=1, max_value=20, value=3)

    if st.button("🤖 Get Suggestions"):
        with st.spinner("Thinking..."):
            suggestions = get_task_improvement_suggestions(st.session_state["messages"], num)
            lines = [line.strip() for line in suggestions.splitlines() if line.strip().startswith("- ")]
            st.session_state["pending"] = lines

# Step 3: Interactive approval
if st.session_state.get("pending"):
    suggestion = st.session_state["pending"][0]
    st.markdown("### ✨ Suggestion")
    st.write(suggestion)

    col1, col2 = st.columns(2)
    if col1.button("✅ Approve"):
        if st.session_state["pending"]:
            st.session_state["approved"].append(st.session_state["pending"].pop(0))
        st.rerun()

    if col2.button("⏭️ Skip"):
        if st.session_state["pending"]:
            st.session_state["pending"].pop(0)
        st.rerun()

# Step 4: Final output + download
if st.session_state.get("pending") == [] and "approved" in st.session_state:
    st.markdown("### ✅ Approved Suggestions")

    if st.session_state["approved"]:
        for item in st.session_state["approved"]:
            st.success(item)
    else:
        st.warning("No suggestions approved.")
        st.write("None")

    # ✅ Build downloadable content
    summary = st.session_state.get("summary", "")
    approved = st.session_state["approved"]
    suggestion_text = "\n".join(approved) if approved else "None"

    download_text = f"GPT Summary:\n{summary}\n\nApproved Suggestions:\n{suggestion_text}"
    st.download_button("📄 Download Summary + Suggestions", download_text, file_name="gpt_todoist_summary.txt")
