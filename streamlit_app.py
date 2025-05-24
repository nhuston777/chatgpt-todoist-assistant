import streamlit as st
from todoist_api import count_open_tasks, extract_task_descriptions
from openai_api import get_task_summary, get_task_improvement_suggestions

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

        for key in ["summary", "messages", "task_descriptions", "pending", "approved"]:
            if key in st.session_state:
                del st.session_state[key]

        st.rerun()

    st.stop()

# Step 4: Show confirmed input
st.success(f"✅ Task limit confirmed: {st.session_state['task_limit']} tasks")

# Step 5: Pull tasks and send to GPT
if "summary" not in st.session_state or "messages" not in st.session_state:
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

# 🛠 Reset if broken state
if "pending" in st.session_state and not st.session_state["pending"]:
    del st.session_state["pending"]
    st.rerun()

# Step 7: Ask how many suggestions
if "pending" not in st.session_state and "messages" in st.session_state:
    num = st.number_input("How many suggestions would you like?", min_value=1, max_value=20, value=3)
    if st.button("🤖 Get Suggestions"):
        with st.spinner("Generating suggestions from GPT..."):
            raw = get_task_improvement_suggestions(st.session_state["messages"], num)
            parsed = [line.strip() for line in raw.splitlines() if line.strip().startswith("- ")]
            st.session_state["pending"] = parsed
        st.rerun()

# Step 8: Suggestion approval loop
if st.session_state.get("pending"):
    if st.session_state["pending"]:  # still suggestions left
        current = st.session_state["pending"][0]
        st.markdown("### ✨ Suggestion")
        st.write(current)

        col1, col2 = st.columns(2)
        if col1.button("✅ Approve"):
            st.session_state["approved"].append(st.session_state["pending"].pop(0))
            st.rerun()
        if col2.button("⏭️ Skip"):
            st.session_state["pending"].pop(0)
            st.rerun()
    else:
        # ✅ All suggestions handled — clear "pending" to prevent re-entry
        del st.session_state["pending"]
        st.rerun()

# Step 9: Show and export approved suggestions
if "approved" in st.session_state and "pending" not in st.session_state:
    st.markdown("### ✅ Approved Suggestions")

    if st.session_state["approved"]:
        for suggestion in st.session_state["approved"]:
            st.success(suggestion)
    else:
        st.warning("No suggestions were approved.")
        st.write("None")

    # ✅ Build downloadable content
    summary = st.session_state.get("summary", "")
    approved = st.session_state["approved"]
    suggestion_text = "\n".join(approved) if approved else "None"

    download_text = f"GPT Summary:\n{summary}\n\nApproved Suggestions:\n{suggestion_text}"
    st.download_button("📄 Download Summary + Suggestions", download_text, file_name="gpt_todoist_summary.txt")