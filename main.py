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

def main_loop():
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
    def submit(self, file_path, text):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
    
    def get_file_content(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

    def get_extentions(self):
        path = functions.resource_path('extentions')
        items = os.listdir(path)
        return items
    
    def add_extention(self, name):
        path = functions.resource_path(f'extentions/{name}')
        with open(path, 'w') as f:
            pass
    
    def delete_extention(self, name):
        path = functions.resource_path(f'extentions/{name}')
        os.remove(path)
    
    def get_config(self):
        config_path = functions.resource_path('config.yaml')
        config = functions.load_yaml_file(config_path)
        config = functions.edit_config(config)
        return config
    
    def change_config(self, key, value):
        config_path = functions.resource_path('config.yaml')
        config = functions.load_yaml_file(config_path)
        config[key] = value
        with open(config_path, 'w', encoding='utf-8') as file:
            yaml.dump(config, file)

    def send_command(self, text):
        print(text)
        functions.command(text)

    def get_keys(self):
        keys_path = functions.resource_path('keys.yaml')
        keys = functions.load_yaml_file(keys_path)
        return keys
    
    def change_keys(self, key, value):
        keys_path = functions.resource_path('keys.yaml')
        keys = functions.load_yaml_file(keys_path)
        keys[key] = value
        with open(keys_path, 'w', encoding='utf-8') as file:
            yaml.dump(keys, file)

    def get_last_displayed_text(self):
        with open("resources/output.txt", "r", encoding="utf-8") as file:
            text = file.read()
        return text
    
if __name__ == "__main__":
    rec = KaldiRecognizer(Model(functions.resource_path(f"vosk-models/{functions.load_yaml_file(functions.resource_path('config.yaml'))['vosk-model']}")), 16000)

    wakeword_library = functions.load_yaml_file(functions.resource_path("config.yaml"))["wakeword-library"]

    if wakeword_library == "openwakeword": # Проверяем какая библиотека выбрана
        openwakeword.utils.download_models()
        openwakeword_model = openwakeword.Model(wakeword_models=["jarvis"])
    elif wakeword_library == "porcupine":
        access_key = functions.load_yaml_file(functions.resource_path("keys.yaml"))["porcupine"]
        keywords = ["jarvis"]

        porcupine = None
        recorder = None

    functions.playRandomSound([functions.translate("Good morning, sir!")])

    api = API()

    thread = threading.Thread(target=main_loop, daemon=True).start()

    window = webview.create_window("Jarvis", functions.resource_path("visual/index.html"), js_api=api)
    webview.start(debug=True)
