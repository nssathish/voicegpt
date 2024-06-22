import time

import pygame
import speech_recognition as sr
from gtts import gTTS
from openai import OpenAI


def initialize():
    API_KEY = "<OpenAI-API-KEY>"
    client = OpenAI(api_key=API_KEY)
    pygame.mixer.init()
    r = sr.Recognizer()
    return client, r


def get_audio_source(audio_file=None):
    return sr.Microphone() if audio_file is None else sr.AudioFile(audio_file)


def chat_gpt(query, client):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a science teacher"},
            {"role": "user", "content": query},
        ],
        max_tokens=1000,
    )
    return str.strip(response.choices[0].message.content)


def speech_to_text(audio_source, r):
    print("Talk")
    audio_text = r.listen(audio_source)
    print("Time over, thanks")
    return audio_text


def text_to_speech(query, client, r):
    query = r.recognize_google(query)
    res = chat_gpt(query, client)
    tts = gTTS(text=res, lang="en")
    tts.save("good.mp3")

    pygame.mixer.music.load("good.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(10)


def serve(client, r):
    with get_audio_source() as source:
        query = speech_to_text(source, r)
        try:
            text_to_speech(query, client, r)
        except ValueError as ve:
            print("Sorry, I did not get that")
            raise ve


def save_audio_file(name):
    main_file = open(name, "rb").read()
    dest_file = open("./file_name.mp3", "wb+")
    dest_file.write(main_file)


def main():
    (client, r) = initialize()
    serve(client, r)


main()
