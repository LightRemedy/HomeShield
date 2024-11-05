# modules/model.py
from ultralytics import YOLO
import streamlit as st
from pathlib import Path
from .logger import logger

class_names = {0: "fire", 1: "smoke"}

@st.cache_resource
def load_model(base_dir: Path):
    try:
        model_path = base_dir / 'runs' / 'detect' / 'HomeShield' / 'weights' / 'best.pt'
        logger.info(f"Loading YOLO model from {model_path}")
        model = YOLO(str(model_path))
        logger.info("YOLO model loaded successfully.")
        return model
    except Exception as e:
        logger.error(f"Error loading YOLO model: {e}")
        st.error(f"Failed to load YOLO model: {e}")
        raise e
