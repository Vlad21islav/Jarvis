import winsound
import random
import yaml
import subprocess
import os
from google import genai
import wave
from piper import PiperVoice

def load_yaml_file(file_path: str) -> dict:
    """Загружает содержимое yaml файла и возвращает его как словарь."""
    with open(file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return data

def choose_language() -> str:
    languages = list(load_yaml_file("translation.yaml").keys())
    if len(languages) == 0:
        print(f"You have no languages in the 'translation.yaml' file.")
        exit(1)
    if len(languages) == 1:
        print(f"Using language: {languages[0]}")
        return languages[0]
    if len(languages) > 1:
        print(f"Which language do you want to use?" + "\n" + "\n".join([f"{i+1}. {lang}" for i, lang in enumerate(languages)]))
        choice = int(input("Enter the number of the language: "))
        return languages[choice - 1]

language = choose_language()

def translate(text: str) -> str:
    translation_file = load_yaml_file("translation.yaml")
    return translation_file[language][translation_file["en"].index(text)]

translate("Yes sir!")

def choose_model(folder: str, model_name: str) -> str:
    models = os.listdir(folder)
    if len(models) == 0:
        print(f"Please download a {model_name.capitalize()} model and place it in the '{folder}' folder.")
        exit(1)
    if len(models) == 1:
        print(f"Using {model_name.capitalize()} model: {models[0]}")
        return models[0]
    if len(models) > 1:
        print(f"Which {model_name.capitalize()} model do you want to use?" + "\n" + "\n".join([f"{i+1}. {model}" for i, model in enumerate(models)]))
        choice = int(input("Enter the number of the model: "))
        return models[choice - 1]

voice = PiperVoice.load(f"piper-models/{choose_model('piper-models', 'piper')}/voice.onnx")

def load_yaml_file(file_path: str) -> dict:
    """Загружает содержимое yaml файла и возвращает его как словарь."""
    with open(file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return data

client = genai.Client(api_key=load_yaml_file("keys.yaml")["genai"])

def playRandomSound(list: list[str]) -> None:
    """Проигрывает случайный звук из списка."""
    choice = random.choice(list)
    print(choice)
    text_to_speech(choice)

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
                    playRandomSound(data.get("voice", {}).get(language, [])) # Проигрываем звук, если он есть
                except IndexError:
                    pass
                for action in data.get("actions", []): # Выполняем действия из расширения
                    if action.startswith("sp/run"): # Если sp/run - запуск команды в терминале
                        command = action.replace("sp/run ", "")
                        subprocess.run(command, shell=True)
                    if action == "cancel": # Если команда отмены, возвращаем False
                        return False

    if not command_was_executed: 
        response = client.models.generate_content( # Иначе генерируем ответ с помощью genai
            model="gemini-2.0-flash", 
            contents=f"You are the voice assistant Jarvis from the movie Iron Man. {text}, say this as short as possible, in one monolithic text. Speak {language} language."
        )
        print(response.text)
        text_to_speech(response.text)
    return True

def text_to_speech(text: str) -> None:
    """Преобразует текст в речь и воспроизводит её."""
    with wave.open("test.wav", "wb") as wav_file:  
        voice.synthesize_wav(text, wav_file)

    winsound.PlaySound("test.wav", winsound.SND_FILENAME)
