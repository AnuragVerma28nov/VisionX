import streamlit as st
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
from collections import Counter
from pathlib import Path

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Real-Time Object Detection",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Real-Time Object Detection")
st.write("YOLO + OpenCV Object Detection")

# -----------------------------
# Model
# -----------------------------

MODEL_PATH = "yolo26n.pt"

@st.cache_resource
def load_model():
    return YOLO(MODEL_PATH)

model = load_model()

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.header("Detection Settings")

confidence = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.10,
    max_value=1.00,
    value=0.50,
    step=0.05
)

# -----------------------------
# Detection Function
# -----------------------------

def detect_objects(image):

    results = model.predict(
        source=image,
        conf=confidence,
        imgsz=640,
        verbose=False
    )

    result = results[0]

    detected_image = result.plot()

    counts = Counter()

    if result.boxes is not None:
        for class_id in result.boxes.cls:
            class_id = int(class_id)
            class_name = result.names[class_id]
            counts[class_name] += 1

    return detected_image, counts


# -----------------------------
# Tabs
# -----------------------------

tab1, tab2 = st.tabs([
    "📷 Image Detection",
    "📹 Camera"
])

# -----------------------------
# Image Detection
# -----------------------------

with tab1:

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:

        image = Image.open(uploaded_file).convert("RGB")

        image_array = np.array(image)

        detected_image, counts = detect_objects(image_array)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Image")
            st.image(image, use_container_width=True)

        with col2:
            st.subheader("Detected Objects")
            st.image(
                detected_image,
                channels="BGR",
                use_container_width=True
            )

        st.subheader("Object Count")

        if counts:
            for name, count in counts.items():
                st.write(f"**{name}:** {count}")
        else:
            st.info("No objects detected.")


# -----------------------------
# Camera
# -----------------------------

with tab2:

    st.info(
        "Allow camera access when your browser asks for permission."
    )

    camera_image = st.camera_input(
        "Take a picture using your camera"
    )

    if camera_image:

        image = Image.open(camera_image).convert("RGB")

        image_array = np.array(image)

        detected_image, counts = detect_objects(image_array)

        st.subheader("Detection Result")

        st.image(
            detected_image,
            channels="BGR",
            use_container_width=True
        )

        st.subheader("Object Count")

        if counts:
            for name, count in counts.items():
                st.write(f"**{name}:** {count}")
        else:
            st.info("No objects detected.")