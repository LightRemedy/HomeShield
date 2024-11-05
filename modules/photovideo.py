# modules/photovideo.py
import streamlit as st
import cv2
import numpy as np
from pathlib import Path
from .model import load_model, class_names
from .telegram import TelegramConfig
from .logger import logger

class PhotoVideoProcessor:
    def __init__(self, base_dir: Path):
        self.model = load_model(base_dir)
        self.telegram = TelegramConfig()

    def process(self):
        uploaded_file = st.file_uploader("Choose an image or video...", type=["jpg", "jpeg", "png", "mp4"])

        if uploaded_file is not None:
            if uploaded_file.type.startswith("image"):
                self.process_image(uploaded_file)
            elif uploaded_file.type == "video/mp4":
                self.process_video(uploaded_file)

    def process_image(self, uploaded_file):
        try:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, 1)

            # Perform inference on the image
            results = self.model.predict(source=img)

            # Draw bounding boxes on the image
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    xyxy = box.xyxy[0].cpu().numpy()
                    conf = box.conf[0].item()
                    cls = int(box.cls[0].item())
                    if conf >= 0.5:
                        label = f'{class_names.get(cls, "Unknown")}: {conf:.2f}'
                        img = cv2.rectangle(
                            img,
                            (int(xyxy[0]), int(xyxy[1])),
                            (int(xyxy[2]), int(xyxy[3])),
                            (0, 255, 0),
                            2
                        )
                        img = cv2.putText(
                            img,
                            label,
                            (int(xyxy[0]), int(xyxy[1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,
                            (0, 255, 0),
                            2
                        )

                        # Send alert if Telegram is enabled
                        if st.session_state.get("enable_telegram", False):
                            self.telegram.send_telegram_alert(
                                class_names.get(cls, "Unknown"),
                                "Image/Video Upload",
                                conf * 100
                            )

            # Display the processed image
            st.image(img, channels="BGR", caption="Processed Image")
            logger.info("Processed an image successfully.")
        except Exception as e:
            st.error(f"An error occurred while processing the image: {e}")
            logger.error(f"Error processing image: {e}")

    def process_video(self, uploaded_file):
        try:
            base_dir = Path(__file__).resolve().parent.parent
            temp_file_path = base_dir / "temp_video.mp4"
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.read())

            cap = cv2.VideoCapture(str(temp_file_path))
            stframe = st.empty()

            logger.info("Started processing video.")

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Perform inference on each frame
                results = self.model.predict(source=frame)

                # Draw bounding boxes on the frame
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
                                    "Image/Video Upload",
                                    conf * 100
                                )

                # Display the video frame in Streamlit
                stframe.image(frame, channels="BGR")

            cap.release()
            logger.info("Finished processing video.")
        except Exception as e:
            st.error(f"An error occurred while processing the video: {e}")
            logger.error(f"Error processing video: {e}")
