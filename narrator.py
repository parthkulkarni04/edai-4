import os
import ollama
import base64
import json
import time
# import simpleaudio as sa
import errno
import speech_recognition as sr
import os
from gtts import gTTS
import playsound

# client = OpenAI()

# set_api_key(os.environ.get("ELEVENLABS_API_KEY"))

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
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""

def generate_audio(text):
    tts = gTTS(text=text, lang='en')
    unique_id = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8").rstrip("=")
    dir_path = os.path.join("narration", unique_id)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, "audio.mp3")
    tts.save(file_path)
    return file_path

def play_audio(text):
    file_path = generate_audio(text)
    playsound.playsound(file_path)


def generate_new_line(base64_image):
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "provide a short description for the following image"},
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        },
    ]


def analyze_image(base64_image, script):
    res = ollama.chat(
	model="llava",
	messages=script + [
		{
			'role': 'user',
			'content': 'Describe this image:',
			'images': [base64_image]
		}
	]
)

    return(res['message']['content'])
    # client = ollama.Client()
    # response = client.chat(
    #     model="llava",
    #     messages=script + [{'role': 'user', 'content': '', 'images': [base64_image]}]
    # )
    # response_text = response['message']['content']
    # return response_text


def main():
    script = []

    while True:
        # path to your image
        image_path = os.path.join(os.getcwd(), "./frames/frame.jpg")

        # getting the base64 encoding
        base64_image = encode_image(image_path)

        # analyze posture
        print("Analyzing the imgae...")
        analysis = analyze_image(base64_image, script=script)

        print("description : ")
        print(analysis)


        play_audio(analysis)

        script = script + [{"role": "assistant", "content": analysis}]

        # wait for 5 seconds
        time.sleep(5)


if __name__ == "__main__":
    main()