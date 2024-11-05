# modules/screencapture.py
import cv2
import numpy as np
import pyautogui
import streamlit as st
import time
from pathlib import Path
from .model import load_model, class_names
from .telegram import TelegramConfig
from .logger import logger

class ScreenMonitor:
    def __init__(self, base_dir: Path):
        self.model = load_model(base_dir)
        self.telegram = TelegramConfig()

    def start_monitoring(self):
        st.sidebar.subheader("Monitoring Control")
        monitoring = st.sidebar.checkbox("Start Monitoring", key="monitor_checkbox")

        stframe = st.empty()

        logger.info("Screen monitoring started.")

        while monitoring:
            # Capture the screen
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert colors from RGB to BGR

            # Perform inference on the captured frame
            results = self.model.predict(source=frame)

            # Draw bounding boxes on the frame for detected objects
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    xyxy = box.xyxy[0].cpu().numpy()
                    conf = box.conf[0].item()
                    cls = int(box.cls[0].item())
                    if conf >= 0.5:
                        label = f'{class_names.get(cls, "Unknown")}: {conf:.2f}'
                        frame = cv2.rectangle(
                            frame,
                            (int(xyxy[0]), int(xyxy[1])),
                            (int(xyxy[2]), int(xyxy[3])),
                            (0, 255, 0),
                            2
                        )
                        frame = cv2.putText(
                            frame,
                            label,
                            (int(xyxy[0]), int(xyxy[1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 255, 0),
                            2
                        )

                        # Send alert if Telegram is enabled
                        if st.session_state.get("enable_telegram", False):
                            self.telegram.send_telegram_alert(
                                class_names.get(cls, "Unknown"),
                                "Screen Monitoring",
                                conf * 100
                            )

            # Display the frame in Streamlit
            stframe.image(frame, channels="BGR")

            # Short delay to allow Streamlit to refresh
            time.sleep(0.1)

            # Update the monitoring state based on the checkbox
            monitoring = st.session_state.monitor_checkbox

            if not monitoring:
                logger.info("Screen monitoring stopped by user.")
                break

        logger.info("Screen monitoring ended.")
