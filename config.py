import os
from dotenv import load_dotenv
load_dotenv()

try:
    import streamlit as st
    OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY")
    TODOIST_API_TOKEN = st.secrets.get("TODOIST_API_TOKEN")
except ModuleNotFoundError:
    from dotenv import load_dotenv
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TODOIST_API_TOKEN = os.getenv("TODOIST_API_TOKEN")