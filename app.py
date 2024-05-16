import streamlit as st
import cv2
import numpy as np
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import pyttsx3

# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()

# Load the model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

st.title("Real-Time Image Description for Blind Individuals")
st.write("This app provides real-time image descriptions.")

# Camera input
camera = st.camera_input("Capture an image")

if camera:
    # Convert the camera input to an image
    img = Image.open(camera)
    
    # Preprocess the image
    inputs = processor(images=img, return_tensors="pt")
    
    # Generate description
    outputs = model.generate(**inputs)
    description = processor.decode(outputs[0], skip_special_tokens=True)
    
    st.image(img, caption="Captured Image", use_column_width=True)
    st.write(f"Description: {description}")
    
    # Convert text to speech
    tts_engine.say(description)
    tts_engine.runAndWait()
