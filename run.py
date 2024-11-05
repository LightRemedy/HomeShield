# run.py
import streamlit as st
from pathlib import Path
from modules.photovideo import PhotoVideoProcessor
from modules.webcam import WebcamDetector
from modules.screencapture import ScreenMonitor
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
    ["Upload Photo/Video", "Webcam Realtime Detection"]#, "Screen Monitoring"]
)

# Get Base Directory
BASE_DIR = Path(__file__).resolve().parent

# Run selected mode
if mode == "Upload Photo/Video":
    processor = PhotoVideoProcessor(BASE_DIR)
    processor.process()
elif mode == "Webcam Realtime Detection":
    detector = WebcamDetector(BASE_DIR)
    detector.start_detection()
# elif mode == "Screen Monitoring":
#     monitor = ScreenMonitor(BASE_DIR)
#     monitor.start_monitoring()

logger.info("Application ended.")
