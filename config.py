import os

# For local development (.env file)
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

# Try Streamlit secrets first, then fall back to environment variables
TODOIST_API_TOKEN = os.getenv("TODOIST_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Streamlit will override these if secrets are defined
try:
    import streamlit as st
    if "TODOIST_API_TOKEN" in st.secrets:
        TODOIST_API_TOKEN = st.secrets["TODOIST_API_TOKEN"]
    if "OPENAI_API_KEY" in st.secrets:
        OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except ImportError:
    pass