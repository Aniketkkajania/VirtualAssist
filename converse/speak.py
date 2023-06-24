import speech_recognition as sr
from converse.translate import google_text_translate

mic = sr.Microphone()
r = sr.Recognizer()

def speak():
    with mic as source:
        r.adjust_for_ambient_noise(source)
        # print("Listening....")
        audio = r.listen(source, 30, 3)
        # print("Recognizing Now....")

    return google_text_translate(r.recognize_google(audio))
