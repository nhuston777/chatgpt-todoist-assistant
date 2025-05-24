import streamlit as st

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

# Temporary test message
st.success("You are authenticated!")