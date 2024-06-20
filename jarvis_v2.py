# import library
import pygame
import speech_recognition as sr
import winsound
from gtts import gTTS
from openai import OpenAI

client = OpenAI(api_key="sk")
pygame.mixer.init()


def chat_gpt(query):
    response = client.chat.completions.create(
        # model="gpt-3.5-turbo-instruct",
        # model="davinci-002",
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a science teacher"},
            {"role": "user", "content": query},
        ],
        # prompt=query,
        max_tokens=1000,
    )
    return str.strip(response.choices[0].message.content)


# Initialize recognizer class (for recognizing the speech)

r = sr.Recognizer()

# Reading Microphone as source
# listening the speech and store in audio_text variable

# with sr.AudioFile("../microphone-results.wav") as source:
with sr.Microphone() as source:
    print("Talk")
    audio_text = r.listen(source)
    print("Time over, thanks")
    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling

    try:
        # using google speech recognition
        command = r.recognize_google(audio_text)
        print("Text: " + command)
        query = command
        (res) = chat_gpt(query)
        print(res)
        tts = gTTS(text=res, lang="en")
        tts.save("good.mp3")
        # main_file = open("good.mp3", "rb").read()
        # dest_file = open("./file_name.mp3", "wb+")
        # dest_file.write(main_file)
        # pygame.mixer.music.load("good.mp3")
        # pygame.mixer.music.play()
        # playsound("good.mp3")
        winsound.PlaySound("good.mp3", 0)

    except ValueError as ve:
        print("Sorry, I did not get that")
        raise ve
