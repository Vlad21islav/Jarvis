import pvporcupine
from pvrecorder import PvRecorder
from vosk import Model, KaldiRecognizer, SpkModel
import pyaudio
from google import genai
import functions

model = Model("vosk-models/small-en-us")
rec = KaldiRecognizer(model, 16000)

access_key = functions.load_yaml_file("keys.yaml")["porcupine"]
keywords = ["jarvis"]

porcupine = None
recorder = None

print("Good morning, sir!")
functions.playRandomSound(["Good morning, sir!"])

def main_loop():
    try:
        porcupine = pvporcupine.create(access_key=access_key, keywords=keywords)
        recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)
        recorder.start()
        while True:
            pcm = recorder.read()
            keyword_index = porcupine.process(pcm)
            
            if keyword_index >= 0: # Если было произнесено ключевое слово, воспроизводим звук и начинаем слушать команды
                print("Yes sir!")
                functions.playRandomSound(["Yes sir"])
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

    except KeyboardInterrupt:
        print("Stopping...")
    except ValueError as e:
        if str(e) =="Failed to read from device.":
            print("Rebooting...")
            main_loop()
    except genai.errors.ServerError as e:
        print("AI server error. Rebooting...")
        main_loop()
    finally:
        if recorder is not None:
            recorder.stop()
            recorder.delete()
        if porcupine is not None:
            porcupine.delete()

if __name__ == "__main__":
    main_loop()
