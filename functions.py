import winsound
import random
import yaml
import subprocess
import os
from google import genai
import wave
from piper import PiperVoice

voice = PiperVoice.load("text-to-speech-models\en-jarvis-medium\jarvis-medium.onnx")

def load_yaml_file(file_path: str) -> dict:
    """Загружает содержимое yaml файла и возвращает его как словарь."""
    with open(file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return data

client = genai.Client(api_key=load_yaml_file("keys.yaml")["genai"])

def playRandomSound(list: list[str]) -> None:
    """Проигрывает случайный звук из списка."""
    text_to_speech(random.choice(list))

def command(text: str) -> bool:
    """Обрабатывает команду пользователя: если такая команда есть в расширениях, выполняет её, если команда - отмена, возвращает False, иначе генерирует ответ с помощью gemai."""
    command_was_executed = False
    extentions = os.listdir("extentions") # Получаем список расширений
    for file in extentions:
        with open(f"extentions/{file}", "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            if any(phrase in text for phrase in data.get("phrases", [])): # Проверяем, есть ли в тексте команды фразы из расширения
                command_was_executed = True
                try:
                    playRandomSound(data.get("voice", {}).get("sounds", [])) # Проигрываем звук, если он есть
                except IndexError:
                    pass
                for action in data.get("actions", []): # Выполняем действия из расширения
                    if action.startswith("sp/run"):
                        command = action.replace("sp/run ", "")
                        subprocess.run(command, shell=True)
    if not command_was_executed: 
        if text == "cancel": # Если команда - cancel, возвращаем False
            return False
        response = client.models.generate_content( # Иначе генерируем ответ с помощью genai
            model="gemini-2.0-flash", 
            contents=f"You are the voice assistant Jarvis from the movie Iron Man. {text}, say this as short as possible, in one monolithic text."
        )
        print(response.text)
        text_to_speech(response.text)
    return True

def text_to_speech(text: str) -> None:
    with wave.open("test.wav", "wb") as wav_file:  
        voice.synthesize_wav(text, wav_file)

    winsound.PlaySound("test.wav", winsound.SND_FILENAME)
