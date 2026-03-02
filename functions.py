import random
import yaml
import subprocess
import os
import wave
import sys
import keyboard
from threading import Timer
from piper import PiperVoice
import requests
import sounddevice as sd
import soundfile as sf
import numpy as np
import time
import json


def resource_path(relative_path: str) -> str:
    """Функция для получения абсолютного пути к файлам (учитывает как режим разработки, так и работу через PyInstaller)"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))  # Проверка, что мы не в PyInstaller
    return os.path.join(base_path, relative_path)

def load_yaml_file(file_path: str) -> dict:
    """Загружает содержимое yaml файла и возвращает его как словарь."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
        return data
    except FileNotFoundError:
        with open(file_path, "w", encoding="utf-8") as file:
            pass
        return {}
    
def add_to_history(role: str, text: str) -> None:
    """Добавляет текст к истории"""
    history = load_yaml_file(resource_path("resources/history.yaml"))
    if history == {} or history == None:
        history = []
    history.append({
        "role": role,
        "text": text,
    })
    with open("resources/history.yaml", "w", encoding="utf-8") as file:
        yaml.dump(history, file)
    if window:
        window.evaluate_js(f'update_history()')


def playRandomSound(list: list[str]) -> None:
    """Проигрывает случайный звук из списка."""
    choice = random.choice(list)
    text_to_speech(choice)

def run_action(action: str) -> bool:
    """Выполняет команду из .yaml файла"""
    if action.startswith("sp/run"): # Если sp/run - запуск команды в терминале
        command = action.replace("sp/run ", "")
        subprocess.run(command, shell=True)
    if action.startswith("keyboard"): # Если keyboard.что-то, выполняется что-то с клавиатурой
        action = action.replace("keyboard.", "")
        if action.startswith("send"):
            button = action.replace("send ", "")
            keyboard.send(button)
        if action.startswith("write"):
            text = action.replace("write ", "")
            keyboard.write(text)
    if action.startswith("plan"): # Если plan, планируем команду через какое-то время
        delay, *action = action.replace("plan ", "").split(" ")
        delay, action = int(delay), " ".join(action)
        Timer(delay, lambda: run_action(action)).start()
    if action == "cancel": # Если команда отмены, возвращаем False
        return False
    return True

def use_gemini(text: str) -> str:
    """Генерирует ответ с помощью gemini."""
    response = requests.get("https://Vlad21islav.pythonanywhere.com/ask", params={
        "query": text,
        "api_key": load_yaml_file(resource_path("resources/keys.yaml"))["genai"], 
        "model_version": load_yaml_file(resource_path("resources/config.yaml"))["genai-version"]
    }).json()["answer"]
    return response

def use_gigachat(text: str) -> str:
    """Генерирует ответ с помощью gigachat."""
    key = load_yaml_file(resource_path("resources/keys.yaml"))["gigachat"]
    model = load_yaml_file(resource_path("resources/config.yaml"))["gigachat-version"]
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    payload={'scope': 'GIGACHAT_API_PERS'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json', 'RqUID': '6c442f3d-9bf1-4e87-bc4f-64a60a6d2f5f', 'Authorization': f'Basic {key}'}
    token = requests.request("POST", url, headers=headers, data=payload, verify=False).json()['access_token']
    payload = {"model": model, "messages": [{"role": "user", "content": text}]}
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False).json()['choices'][0]['message']['content']
    return response

def command(text: str) -> bool:
    """Обрабатывает команду пользователя: если такая команда есть в расширениях, выполняет её, если команда - отмена, возвращает False, иначе генерирует ответ с помощью gemai."""
    add_to_history("You", text)
    command_was_executed = False
    extentions = os.listdir(resource_path("extentions")) # Получаем список расширений
    for folder in extentions:
        with open(resource_path(f"extentions/{folder}/command.yaml"), "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            if any(phrase in text for phrase in data.get("phrases", [])): # Проверяем, есть ли в тексте команды фразы из расширения
                command_was_executed = True
                try:
                    playRandomSound(data.get("voice", {}).get(load_yaml_file(resource_path("resources/config.yaml"))["language"], [])) # Проигрываем звук, если он есть
                except IndexError:
                    pass
                for action in data.get("actions", []): # Выполняем действия из расширения
                    if not run_action(action):
                        return False

    if not command_was_executed and load_yaml_file(resource_path("resources/config.yaml"))["gpt-model"].lower() != "don't use gpt": # Иначе генерируем ответ с помощью gpt
        text = load_yaml_file(resource_path("resources/config.yaml"))["ai-data"].replace("{language}", load_yaml_file(resource_path("resources/config.yaml"))["language"]).replace("{text}", text)
                # Заменяем {text} на текст, сказанный пользователем и {language} на выбранный язык 
        gpt_model = load_yaml_file(resource_path("resources/config.yaml"))["gpt-model"]
        if gpt_model == "gemini":
            response = use_gemini(text)
        elif gpt_model == "gigachat":
            response = use_gigachat(text)
        text_to_speech(response)
    return True

def set_window(w: object) -> None:
    global window
    window = w

def text_to_speech(text: str) -> None:
    """Преобразует текст в речь и воспроизводит её."""
    if window:
        window.evaluate_js(f'update_output_text("{text}")')
    add_to_history("Jarvis", text)
    global piper_model
    new_piper_model = load_yaml_file(resource_path("resources/config.yaml"))["piper-model"]
    if piper_model != new_piper_model:
        global piper_voice
        piper_model = new_piper_model
        piper_voice = PiperVoice.load(resource_path(f"piper-models/{new_piper_model}/voice.onnx"))
    with wave.open(resource_path("resources/test.wav"), "wb") as wav_file:
        piper_voice.synthesize_wav(text, wav_file)

    data, samplerate = sf.read(resource_path("resources/test.wav"))
    sd.play(data, samplerate)
    chunk_size = 2048
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        if len(chunk) < chunk_size:
            break
        if chunk.ndim == 1:
            mono = chunk
        else:
            mono = chunk[:, 0]
        spectrum = np.abs(np.fft.rfft(mono))
        spectrum = spectrum[:128]
        spectrum = spectrum / np.max(spectrum)
        spectrum = spectrum.tolist()
        time.sleep(chunk_size / samplerate)
    sd.wait()

def translate(text: str) -> str:
    translation_file = load_yaml_file(resource_path("resources/translation.yaml"))
    return translation_file[load_yaml_file(resource_path("resources/config.yaml"))["language"]][translation_file["en"].index(text)]

def edit_config(config: dict) -> dict:
    config["vosk-model"] = {
        "options": os.listdir(resource_path("vosk-models")), 
        "selected": config["vosk-model"],
        "type": "select",
        "name": "Vosk model",
        "description": "Vosk model for speech recognition",
    }
    config["piper-model"] = {
        "options": os.listdir(resource_path("piper-models")), 
        "selected": config["piper-model"],
        "type": "select",
        "name": "Piper model",
        "description": "Piper model for generation voice",
    }
    config["wakeword-library"] = {
        "options": ["openwakeword", "porcupine", "vosk"],
        "selected": config["wakeword-library"],
        "type": "select",
        "name": "WakeWord library",
        "description": "Library for listening to a wakeword like 'Jarvis'",
    }
    config["language"] = {
        "options": list(load_yaml_file(resource_path("resources/translation.yaml")).keys()),
        "selected": config["language"],
        "type": "select",
        "name": "Language",
        "description": "Language Jarvis would listen and speek",
    }
    config["gpt-model"] = {
        "options": ["don't use gpt", "gemini", "gigachat"],
        "selected": config["gpt-model"],
        "type": "select",
        "name": "Text generation model",
        "description": "AI model for generating a text response",
    }
    config["ai-data"] = {
        "value": config["ai-data"],
        "type": "input",
        "name": "Base data for text generation model",
        "description": "Base text for generationg a response",
    }
    config["genai-version"] = {
        "options": ["gemini-2.5-flash", "gemini-2.5"],
        "selected": config["genai-version"],
        "type": "select",
        "name": "Google gemini version",
        "description": "Version of Google AI",
    }
    config["gigachat-version"] = {
        "options": ["GigaChat-2-Max", "GigaChat-2"],
        "selected": config["gigachat-version"],
        "type": "select",
        "name": "Sber GigaChat version",
        "description": "Version of Sber AI",
    }
    config["app-theme"] = {
        "options": ["Auto", "Dark", "Light"],
        "selected": config["app-theme"],
        "type": "select",
        "name": "App theme",
        "description": "Theme of this application",
    }
    return config

piper_model = None
piper_voice = None
window = None
output_text = ""
