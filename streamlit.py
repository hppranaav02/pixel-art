import streamlit as st
import requests
from PIL import Image, ImageDraw
from streamlit_drawable_canvas import st_canvas
import pandas as pd
import numpy as np

# Streamlit app
st.title("Sketch and API App")

# Create a canvas to sketch

# Specify canvas parameters in application
drawing_mode = st.sidebar.selectbox(
    "Drawing tool:", ("freedraw")
)

stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
stroke_color = st.sidebar.color_picker("Stroke color hex: ")
bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])

realtime_update = st.sidebar.checkbox("Update in realtime", True)

# canvas_result = st_canvas(
#     fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
#     stroke_width=stroke_width,
#     stroke_color=stroke_color,
#     background_color=bg_color,
#     background_image=Image.open(bg_image) if bg_image else None,
#     update_streamlit=realtime_update,
#     height=150,
#     drawing_mode=drawing_mode,
#     point_display_radius=0,
#     key="canvas",
# )

canvas_result = st_canvas(
    fill_color="rgb(255, 255, 255)",  # Background color in RGB format
    stroke_width=10,
    stroke_color="rgb(0, 0, 0)",  # Stroke color in RGB format
    background_color="rgb(255, 255, 255)",  # Initial canvas color
    height=300,  # Canvas height
    drawing_mode="freedraw",  # Set to "freedraw" for free drawing
    key="canvas",
)

# Button to clear the canvas
if st.button("Clear Canvas"):
    canvas_result.json_data["objects"] = []

# User prompt input
user_prompt = st.text_input("Enter your prompt")

# Button to trigger API call
if st.button("Generate"):
    # Convert the canvas data to an image
    image_array = np.array(canvas_result.image_data)
    image = Image.fromarray((image_array * 255).astype(np.uint8))

    image = image.convert("RGB")

    # Check if the image is square, resize if necessary
    if image.width != image.height:
        min_dimension = min(image.width, image.height)
        image = image.crop((0, 0, min_dimension, min_dimension))

    # Save the image locally
    image.save("sketch.jpg")

    sketch_file_object = open("sketch.jpg", "rb")

    response = requests.post(
        "http://localhost:8000/sketch-to-image",
        data={"prompt": user_prompt + ", pixel art"},
    )

    st.text("Generated Image")
    st.image(response.content, caption="Generated Image", use_column_width=True)
