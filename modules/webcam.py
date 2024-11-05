# modules/webcam.py
import cv2
import streamlit as st
from .model import load_model, class_names
from .telegram import TelegramConfig
from .logger import logger

class WebcamDetector:
    def __init__(self, base_dir):
        self.model = load_model(base_dir)
        self.telegram = TelegramConfig()

    def start_detection(self):
        cap = cv2.VideoCapture(0)
        stframe = st.empty()
        stop_button = st.button("Stop Webcam Detection")

        logger.info("Webcam detection started.")

        while cap.isOpened():
            if stop_button:
                logger.info("Webcam detection stopped by user.")
                break

            ret, frame = cap.read()
            if not ret:
                logger.warning("Failed to read frame from webcam.")
                break

            # Perform inference on the frame
            results = self.model.predict(source=frame)

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
                                "Webcam Realtime Detection",
                                conf * 100
                            )

            stframe.image(frame, channels="BGR")

        cap.release()
        logger.info("Webcam capture released.")
