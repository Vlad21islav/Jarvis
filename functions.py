import winsound
import random
import yaml
import subprocess
import os
from google import genai
import wave
import sys
import quetions
from pynput.keyboard import Key, Controller
import time

def resource_path(relative_path):
    """Функция для получения абсолютного пути к файлам (учитывает как режим разработки, так и работу через PyInstaller)"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))  # Проверка, что мы не в PyInstaller
    return os.path.join(base_path, relative_path)

def load_yaml_file(file_path: str) -> dict:
    """Загружает содержимое yaml файла и возвращает его как словарь."""
    with open(file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return data

def load_yaml_file(file_path: str) -> dict:
    """Загружает содержимое yaml файла и возвращает его как словарь."""
    with open(file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return data

def playRandomSound(list: list[str]) -> None:
    """Проигрывает случайный звук из списка."""
    choice = random.choice(list)
    print(choice)
    text_to_speech(choice)

def command(text: str) -> bool:
    """Обрабатывает команду пользователя: если такая команда есть в расширениях, выполняет её, если команда - отмена, возвращает False, иначе генерирует ответ с помощью gemai."""
    command_was_executed = False
    extentions = os.listdir(resource_path("extentions")) # Получаем список расширений
    for file in extentions:
        with open(resource_path(f"extentions/{file}"), "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            if any(phrase in text for phrase in data.get("phrases", [])): # Проверяем, есть ли в тексте команды фразы из расширения
                command_was_executed = True
                try:
                    playRandomSound(data.get("voice", {}).get(quetions.language, [])) # Проигрываем звук, если он есть
                except IndexError:
                    pass
                for action in data.get("actions", []): # Выполняем действия из расширения
                    if action.startswith("sp/run"): # Если sp/run - запуск команды в терминале
                        command = action.replace("sp/run ", "")
                        subprocess.run(command, shell=True)
                    if action.startswith("keyboard"): # Если keyboard.что-то, выполняется что-то с клавиатурой
                        action = action.replace("keyboard.", "")
                        keyboard = Controller()
                        if action.startswith("press"):
                            button = action.replace("press ", "")
                            if len(button) == 1:
                                keyboard.press(button)
                            else:
                                keyboard.press(Key[button])
                        if action.startswith("release"):
                            button = action.replace("release ", "")
                            if len(button) == 1:
                                keyboard.release(button)
                            else:
                                keyboard.release(Key[button])
                        if action.startswith("tap"):
                            button = action.replace("tap ", "")
                            if len(button) == 1:
                                keyboard.tap(button)
                            else:
                                keyboard.tap(Key[button])
                        if action.startswith("type"):
                            text = action.replace("type ", "")
                            keyboard.type(text)
                    if action.startswith("freeze"): # Если freeze, задержка на столько секунд, сколько надо
                        sleep_time = action.replace("freeze ", "")
                        time.sleep(int(sleep_time))
                    if action == "cancel": # Если команда отмены, возвращаем False
                        return False

    # if not command_was_executed: 
    #     response = client.models.generate_content( # Иначе генерируем ответ с помощью genai
    #         model="gemini-2.0-flash", 
    #         contents=f'{quetions.language.join(text.join(load_yaml_file(resource_path("config.yaml"))["ai-data"].split("{text}")).split("{language}"))}'  
    #             # Заменяем {text} на текст, сказанный пользователем и {language} на выбранный язык
    #     )
    #     print(response.text)
    #     text_to_speech(response.text)
    return True

def text_to_speech(text: str) -> None:
    """Преобразует текст в речь и воспроизводит её."""
    with wave.open(resource_path("test.wav"), "wb") as wav_file:  
        quetions.piper_voice.synthesize_wav(text, wav_file)

    winsound.PlaySound(resource_path("test.wav"), winsound.SND_FILENAME)

def translate(text: str) -> str:
    translation_file = load_yaml_file(resource_path("translation.yaml"))
    return translation_file[quetions.language][translation_file["en"].index(text)]

client = genai.Client(api_key=load_yaml_file(resource_path("keys.yaml"))["genai"])
