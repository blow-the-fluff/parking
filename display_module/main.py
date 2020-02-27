import streamlit as st
from PIL import Image
import numpy as np


st.title("Hand Text Recognition - Module")

uploaded_file = st.file_uploader("Upload an image (png, jpeg, jpg): ", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    temp_png = './temp.png'
    image.save(temp_png)
    st.image(image, caption='Uploaded Image:', use_column_width=True)
    st.write("")
    st.write("Prediction:")