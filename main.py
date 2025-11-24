import quetions
import pvporcupine
from pvrecorder import PvRecorder
from vosk import KaldiRecognizer
import pyaudio
from google import genai
import functions
import openwakeword
import numpy as np

rec = KaldiRecognizer(quetions.vosk_model, 16000)

functions.playRandomSound([functions.translate("Good morning, sir!")])

wakeword_library = quetions.choose_wakeword_library()

if wakeword_library == "openwakewod":
    openwakeword.utils.download_models()
    openwakeword_model = openwakeword.Model(wakeword_models=["jarvis"])
elif wakeword_library == "porcupine":
    access_key = functions.load_yaml_file(functions.resource_path("keys.yaml"))["porcupine"]
    keywords = ["jarvis"]

    porcupine = None
    recorder = None

def main_loop():
    try:
        if wakeword_library == "openwakewod":
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
            while True:
                audio_data = stream.read(1024)
                audio_np = np.frombuffer(audio_data, dtype=np.int16)
                prediction = openwakeword_model.predict(audio_np)

                for model_name, score in prediction.items():
                    if score > 0.5:
                        vosk_listen()
        elif wakeword_library == "porcupine":
            porcupine = pvporcupine.create(access_key=access_key, keywords=keywords)
            recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)
            recorder.start()
            while True:
                pcm = recorder.read()
                keyword_index = porcupine.process(pcm)
                
                if keyword_index >= 0: # Если было произнесено ключевое слово, воспроизводим звук и начинаем слушать команды
                    vosk_listen()

    except KeyboardInterrupt:
        print(functions.translate("Stopping..."))
    except ValueError as e:
        if str(e) =="Failed to read from device.":
            print(functions.translate("Rebooting..."))
            main_loop()
    except genai.errors.ServerError as e:
        print(functions.translate("AI server error. Rebooting..."))
        main_loop()
    except genai.errors.ClientError as e:
        print(functions.translate("AI client error. Rebooting..."))
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

def vosk_listen():
    """Функция прослушивания команд с помощью Vosk."""
    functions.playRandomSound([functions.translate("Yes sir!")])
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2000)
    stream.start_stream()
    counter = 0
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

if __name__ == "__main__":
    main_loop()
