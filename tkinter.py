import cv2
import speech_recognition as sr
import pyttsx3
import requests
from PIL import Image
import io
import numpy as np
import tkinter as tk
from tkinter import Button

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to send prompt to Llava model and receive response
def get_llava_response(image, prompt):
    url = "http://ollama_api_endpoint"  # Replace with actual Ollama API endpoint
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_API_KEY"  # Replace with your actual API key
    }
    payload = {
        "image": image,
        "prompt": prompt
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['response']
    else:
        return "Error: Unable to get response from Llava model."

# Function to capture frame and process speech
def process_frame_and_speech():
    global button
    button.config(state=tk.DISABLED)
    
    # Capture current frame from camera
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        button.config(state=tk.NORMAL)
        return
    
    # Convert frame to image
    _, buffer = cv2.imencode('.jpg', frame)
    image = buffer.tobytes()
    
    # Start listening to microphone
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=15)
    
    try:
        # Convert speech to text
        prompt = recognizer.recognize_google(audio)
        print("You said: " + prompt)
        
        # Send prompt and image to Llava model
        response_text = get_llava_response(image, prompt)
        print("Response: " + response_text)
        
        # Convert response text to speech
        engine.say(response_text)
        engine.runAndWait()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
    button.config(state=tk.NORMAL)

# Initialize camera
cap = cv2.VideoCapture(0)

# Create a window
root = tk.Tk()
root.title("Live Camera Feed")

# Create a button
button = Button(root, text="Capture and Process", command=process_frame_and_speech)
button.pack()

# Create a label to display the camera feed
label = tk.Label(root)
label.pack()

# Function to continuously update the camera feed
def update_frame():
    ret, frame = cap.read()
    if ret:
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.configure(image=imgtk)
    root.after(10, update_frame)

# Start updating the camera feed
update_frame()

# Start the GUI event loop
root.mainloop()

# Release the camera when the window is closed
cap.release()
cv2.destroyAllWindows()
