import streamlit as st
from main import prompt_task_limit, run_productivity_assistant

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

st.title("🧠 Todoist Assistant Powered by ChatGPT")

# Reset button
if st.button("🔁 Start Over"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

# Prompt only after login
if st.session_state.authenticated and "task_limit" not in st.session_state:
    st.session_state["task_limit"] = prompt_task_limit(interactive=True, streamlit_obj=st)

# Main GPT analysis trigger
if st.button("📋 Analyze Tasks"):
    run_productivity_assistant(st.session_state["task_limit"])

# Show GPT Summary
if "summary" in st.session_state:
    st.markdown("### 🔍 GPT Summary")
    for paragraph in st.session_state["summary"].split("\n\n"):
        st.markdown(paragraph.strip())

# Suggestion generation
if "messages" in st.session_state and not st.session_state.get("pending"):
    num = st.number_input("How many suggestions would you like?", min_value=1, max_value=20, value=3)

    if st.button("🤖 Get Suggestions"):
        from openai_api import get_task_improvement_suggestions
        with st.spinner("Thinking..."):
            suggestions = get_task_improvement_suggestions(st.session_state["messages"], num)
            lines = [line.strip() for line in suggestions.splitlines() if line.strip().startswith("- ")]
            st.session_state["pending"] = lines
            st.session_state["approved"] = []

# Approvals
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

# Final download
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
