from openai import OpenAI

client = OpenAI(api_key="sk")
import pygame
import speech_recognition as sr
from gtts import gTTS

pygame.mixer.init()
# model_to_use = "text-davinci-003"
# model_to_use = "text-curie-001"
# model_to_use = "text-babbage-001"
model_to_use = "text-ada-001"
r = sr.Recognizer()


def chat_gpt(query):
    response = client.completions.create(model_to_use, prompt=query)
    return str.strip(response.choices[0].text), response.usage.total_token


def save_and_check(audio):
    audio_data_output_file_name = "../microphone-results.wav"
    print("saving now as 'microphone-results.wav'..")
    with open(audio_data_output_file_name, "wb") as f:
        f.write(audio.get_wav_data())


def main():
    print("LED is ON while button is pressed(Ctrl-C for exit)")
    while True:
        with sr.AudioFile("../microphone-results.wav") as source:
            # with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Say something")
            audio = r.listen(source)
            #     save_and_check(audio)
            # break
            print("Recognizing now...")
            command = str(r.recognize_google(audio_data=audio, language="en"))
            print("Google Speech Recognition thinks you said " + f"'{command}'")
            query = command
            (res, usage) = chat_gpt(query)
            print(res)
            tts = gTTS(text=res, lang="en")
            tts.save("good.mp3")
            pygame.mixer.music.load("good.mp3")
            pygame.mixer.music.play()


# if __name__ == "__main__":
main()
