from piper import PiperVoice
from vosk import Model
import os
import functions

def choose_language() -> str:
    """Выбор языка"""
    configured_language = functions.load_yaml_file(functions.resource_path("config.yaml")).get("language", "auto")
    if configured_language != "auto":
        return configured_language
    else:
        languages = list(functions.load_yaml_file(functions.resource_path("translation.yaml")).keys())
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
    
def choose_wakeword_library() -> str:
    """Выбор библиотеки для распознования слова Jarvis"""
    configured_library = functions.load_yaml_file(functions.resource_path("config.yaml")).get("wakeword-library", "auto")
    if configured_library != "auto":
        return configured_library
    else:
        print(f"Which library do you want to use?\n" + 
            "1. Openwakeword (Only English)\n" +
            "2. Porcupine (Only in python, doesn't work in exe)\n")
        choice = int(input("Enter the number of the language: "))
        return "openwakewod" if choice == 1 else "porcupine"

def choose_model(folder: str, model_name: str) -> str:
    """Выбор модели для распознования голоса"""
    configured_model = functions.load_yaml_file(functions.resource_path("config.yaml")).get(f"{model_name}-model", "auto")
    if configured_model != "auto":
        return configured_model
    else:
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

piper_voice = PiperVoice.load(functions.resource_path(f"piper-models/{choose_model(functions.resource_path('piper-models'), 'piper')}/voice.onnx"))
vosk_model = Model(functions.resource_path(f"vosk-models/{choose_model(functions.resource_path('vosk-models'), 'vosk')}"))
language = choose_language()
