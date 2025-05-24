import os

# Load from .env file (useful for CLI)
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

# Start with environment variables (fallback)
TODOIST_API_TOKEN = os.getenv("TODOIST_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Safely override with Streamlit secrets only if available
try:
    import streamlit as st
    if hasattr(st, "secrets") and st.secrets._file_paths:  # Check if secrets exist
        if "TODOIST_API_TOKEN" in st.secrets:
            TODOIST_API_TOKEN = st.secrets["TODOIST_API_TOKEN"]
        if "OPENAI_API_KEY" in st.secrets:
            OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except Exception:
    # Not using Streamlit or no secrets found – fall back to .env
    pass