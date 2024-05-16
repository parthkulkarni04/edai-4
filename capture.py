import cv2
import time
from PIL import Image
import numpy as np
import os

def capture():
    # Folder
    folder = "frames"

    # Create the frames folder if it doesn't exist
    frames_dir = os.path.join(os.getcwd(), folder)
    os.makedirs(frames_dir, exist_ok=True)

    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    # Create a window for the webcam feed
    cv2.namedWindow("Webcam Feed")



    # Set smaller window size
    cv2.resizeWindow("Webcam Feed", 100, 100)

    # Wait for the camera to initialize and adjust light levels
    time.sleep(2)

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        frame_count += 1

        # Display "Press Q to start" text
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, "Press Q to start", (20, 40), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Show the webcam feed
        cv2.imshow("Webcam Feed", frame)

        # Check for key press
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            # Save the current frame as "frame.jpg"
            print("Saving frame.")
            cv2.imwrite(os.path.join(frames_dir, "frame.jpg"), frame)
            break


    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

capture()
