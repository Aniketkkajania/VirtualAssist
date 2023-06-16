import speech_recognition as sr


def speak():
    mic = sr.Microphone()
    r = sr.Recognizer()
    with mic as source:
        r.adjust_for_ambient_noise(source)
        # print("Listening....")
        audio = r.listen(source)
        # print("Recognizing Now....")

    return r.recognize_google(audio)
