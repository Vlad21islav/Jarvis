import pvporcupine
from pvrecorder import PvRecorder
from vosk import KaldiRecognizer, Model
import pyaudio
import functions
import openwakeword
import numpy as np
import webview
import yaml
import os
import threading
import shutil
import pystray
from PIL import Image
import winreg
import time


def main_loop():
    global vosk_model
    global rec
    try:
        if wakeword_library == "openwakeword":
            activated = False
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
            while True:
                audio_data = stream.read(1024)
                audio_np = np.frombuffer(audio_data, dtype=np.int16)
                prediction = openwakeword_model.predict(audio_np)

                score = prediction.get("jarvis", 0.0)

                if score > 0.5 and not activated:
                    vosk_listen()
                    activated = True
                elif score < 0.3:  # сброс активации, когда вероятность снова низкая
                    activated = False
  
        elif wakeword_library == "porcupine":
            porcupine = pvporcupine.create(access_key=access_key, keywords=keywords)
            recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)
            recorder.start()
            while True:
                pcm = recorder.read()
                keyword_index = porcupine.process(pcm)
                
                if keyword_index >= 0: # Если было произнесено ключевое слово, воспроизводим звук и начинаем слушать команды
                    vosk_listen()

        elif wakeword_library == "vosk":
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2000)
            stream.start_stream()
            while True:
                if vosk_model != functions.load_yaml_file(functions.resource_path("resources/config.yaml"))["vosk-model"]:
                    vosk_model = functions.load_yaml_file(functions.resource_path("resources/config.yaml"))["vosk-model"]
                    rec = KaldiRecognizer(Model(functions.resource_path(f"vosk-models/{vosk_model}")), 16000)
                data = stream.read(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    text = rec.Result()[14:-3].lower()
                    if functions.translate("jarvis") in text:
                        input_text = text.replace(functions.translate("jarvis"), "")
                        if len(input_text) >= 2:
                            vosk_listen(input_text)
                        else:
                            vosk_listen()
                else:
                    pass

    except KeyboardInterrupt:
        print(functions.translate("Stopping..."))
    except ValueError as e:
        if str(e) =="Failed to read from device.":
            print(functions.translate("Rebooting..."))
            main_loop()
    except OSError:
        print(functions.translate("Rebooting..."))
        main_loop()
    except webview:
        print(functions.translate("Rebooting..."))
        main_loop()
    finally:
        try:
            recorder.stop()
            recorder.delete()
            porcupine.delete()
        except UnboundLocalError:
            pass
        try:
            stream.stop_stream()
            stream.close()
            p.terminate()
        except UnboundLocalError:
            pass

def vosk_listen(input_text: str = None):
    """Функция прослушивания команд с помощью Vosk."""
    global vosk_model
    global rec
    counter = 0
    if input_text:
        if not functions.command(input_text):
            counter = 6
    else:
        functions.playRandomSound([functions.translate("Yes sir!")])
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2000)
    stream.start_stream()
    while True:
        if vosk_model != functions.load_yaml_file(functions.resource_path("resources/config.yaml"))["vosk-model"]:
            vosk_model = functions.load_yaml_file(functions.resource_path("resources/config.yaml"))["vosk-model"]
            rec = KaldiRecognizer(Model(functions.resource_path(f"vosk-models/{vosk_model}")), 16000)
        data = stream.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            counter += 1
            text = rec.Result()[14:-3]
            if text: # Если распознана речь, обрабатываем команду, выполняем её и сбрасываем счётчик
                print(text)
                counter = 0
                if not functions.command(text):
                    counter = 6
            print(counter)
            if counter > 5: # Если в течение определённого времени не было распознано речи, выходим из режима прослушивания команд
                stream.stop_stream()
                break
        else:
            pass

class API:
    def submit(self, file_path: str, text: str) -> None:
        with open(functions.resource_path(file_path), 'w', encoding='utf-8') as file:
            file.write(text)
    
    def get_file_content(self, file_path: str) -> str:
        with open(functions.resource_path(file_path), 'r', encoding='utf-8') as file:
            content = file.read()
        return content

    def get_extentions(self) -> list[str]:
        path = functions.resource_path('extentions')
        items = os.listdir(path)
        return items
    
    def add_extention(self, name: str) -> None:
        dir_path = functions.resource_path(f'extentions/{name}')
        path = dir_path + "/command.yaml"
        os.makedirs(dir_path, exist_ok=True)
        with open(path, 'w') as f:
            pass
    
    def delete_extention(self, name: str) -> None:
        path = functions.resource_path(f'extentions/{name}')
        shutil.rmtree(path)
    
    def get_config(self) -> dict:
        config_path = functions.resource_path('resources/config.yaml')
        config = functions.load_yaml_file(config_path)
        config = functions.edit_config(config)
        return config
    
    def change_config(self, key: str, value: str) -> None:
        config_path = functions.resource_path('resources/config.yaml')
        config = functions.load_yaml_file(config_path)
        config[key] = value
        with open(config_path, 'w', encoding='utf-8') as file:
            yaml.dump(config, file)

    def send_command(self, text: str) -> None:
        print(text)
        functions.command(text)

    def get_keys(self) -> dict:
        keys_path = functions.resource_path('resources/keys.yaml')
        keys = functions.load_yaml_file(keys_path)
        keys = {
            "genai": keys.get("genai", ""),
            "porcupine": keys.get("porcupine", ""),
            "gigachat": keys.get("gigachat", ""),
        }
        return keys
    
    def change_keys(self, key: str, value: str) -> None:
        keys_path = functions.resource_path('resources/keys.yaml')
        keys = functions.load_yaml_file(keys_path)
        keys[key] = value
        with open(keys_path, 'w', encoding='utf-8') as file:
            yaml.dump(keys, file)

def create_tray_icon(window):
    global icon

    def on_show(icon, item):
        window.show()
        window.restore()

    def on_quit(icon, item):
        icon.stop()
        window.destroy()
        os._exit(0)

    image = Image.open("images/dark icon.ico")
    menu = pystray.Menu(
        pystray.MenuItem("Open Jarvis", on_show),
        pystray.MenuItem("Exit", on_quit),
    )

    icon = pystray.Icon("Jarvis", image, "Jarvis", menu)
    icon.run()

def watch_theme():
    def is_light_theme():
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                "Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            )
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return value == 1
        except:
            return True
        
    last = None
    while True:
        time.sleep(1)
        now = is_light_theme()
        if now != last:
            icon.icon = Image.open("images/dark icon.ico" if now else "images/light icon.ico")
            last = now

if __name__ == "__main__":
    vosk_model = functions.load_yaml_file(functions.resource_path("resources/config.yaml"))["vosk-model"]
    rec = KaldiRecognizer(Model(functions.resource_path(f"vosk-models/{vosk_model}")), 16000)

    wakeword_library = functions.load_yaml_file(functions.resource_path("resources/config.yaml"))["wakeword-library"]

    if wakeword_library == "openwakeword": # Проверяем какая библиотека выбрана
        openwakeword.utils.download_models()
        openwakeword_model = openwakeword.Model(wakeword_models=["jarvis"])
    elif wakeword_library == "porcupine":
        access_key = functions.load_yaml_file(functions.resource_path("resources/keys.yaml"))["porcupine"]
        keywords = ["jarvis"]

        porcupine = None
        recorder = None

    functions.playRandomSound([functions.translate("Good morning, sir!")])

    api = API()

    threading.Thread(target=main_loop, daemon=True).start()

    window = webview.create_window("Jarvis", functions.resource_path("visual/index.html"), js_api=api, width=0, height=0, min_size=(576, 585))
    window.events.closing += lambda: (window.hide(), False)[1]

    threading.Thread(target=create_tray_icon, args=(window,), daemon=True).start()

    threading.Thread(target=watch_theme, daemon=True).start()

    functions.set_window(window)
    webview.start(debug=True)
