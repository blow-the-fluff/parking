import streamlit as st
import cv2
from PIL import Image
import predict
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
    prediction = predict.predict(temp_png, np_array=False)
    st.write('{}'.format(prediction[0]))