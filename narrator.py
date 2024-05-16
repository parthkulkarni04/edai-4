import os
import ollama
import base64
import time
import errno
import speech_recognition as sr
import os
from gtts import gTTS
import playsound
import capture #from capture.py

def encode_image(image_path):
    while True:
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
                
        except IOError as e:
            if e.errno != errno.EACCES:
                # Not a "file in use" error, re-raise
                raise
            # File is being written to, wait a bit and retry
            time.sleep(0.1)


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source, timeout=5)  # Listen for up to 5 seconds
        
    try:
        text = recognizer.recognize_google(audio)
        print('You : ' + text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""

def generate_audio(text):
    tts = gTTS(text=text, lang='en')
    os.makedirs("narration", exist_ok=True)
    file_path = os.path.join("narration", "audio.mp3")
    tts.save(file_path)
    return file_path


def play_audio(text):
    file_path = generate_audio(text)
    playsound.playsound(file_path)

def analyze_image(base64_image, script, question):
    res = ollama.chat(
	model="llava",
	messages=script + [
		{
			'role': 'user',
			'content': 'based on the given image give short answer to the following question, Question:' + question,
			'images': [base64_image]
		}
	]
)

    return(res['message']['content'])


def main():
    script = []
    
    while True:
        # path to your image
        print("Press Q to Start")
        capture.capture()
        image_path = os.path.join(os.getcwd(), "./frames/frame.jpg")
        # getting the base64 encoding
        base64_image = encode_image(image_path)
        time.sleep(3)
        question = recognize_speech()

        # analyze posture
        print("Analyzing the imgae...")
        analysis = analyze_image(base64_image, script=script, question=question)

        print("Description : ")
        print(analysis)


        play_audio(analysis)

        script = script + [{"role": "assistant", "content": analysis}]



if __name__ == "__main__":
    main()