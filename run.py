# run.py
import streamlit as st
from pathlib import Path
from modules.photovideo import PhotoVideoProcessor
from modules.telegram import TelegramConfig
from modules.logger import logger

# Initialize Logger
logger.info("Application started.")

# Initialize Streamlit App
st.title("CCTV Fire and Smoke Detection")
st.sidebar.title("Navigation")

# Initialize Telegram Configuration
telegram = TelegramConfig()
telegram.configure_sidebar()

# Sidebar: Choose detection mode
mode = st.sidebar.selectbox(
    "Choose a Detection Mode:",
    ["Upload Photo/Video"]
)

# Get Base Directory
BASE_DIR = Path(__file__).resolve().parent

# Run selected mode
if mode == "Upload Photo/Video":
    processor = PhotoVideoProcessor(BASE_DIR)
    processor.process()


logger.info("Application ended.")
