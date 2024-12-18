# run.py
import streamlit as st
from pathlib import Path
from modules.photovideo import PhotoVideoProcessor
from modules.telegram import TelegramConfig
from modules.logger import logger

# Initialize Logger
logger.info("Application started.")

# Get Base Directory (the directory where this script is located)
BASE_DIRECTORY = Path(__file__).resolve().parent

# Define the path to the company logo image
logo_file_path = BASE_DIRECTORY / "assets" / "icon.png"

# Display the company logo in the Streamlit sidebar
st.sidebar.image(str(logo_file_path), width=150)  # Adjust the width as needed

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
