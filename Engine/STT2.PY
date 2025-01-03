import os
import queue
import subprocess

try :
    import sounddevice as sd
    from vosk import Model, KaldiRecognizer
    print("Vosk library is already installed")
except ModuleNotFoundError:
    subprocess.run("pip install vosk", shell=True)
    subprocess.run("pip install sounddevice")
    import sounddevice as sd
    from vosk import Model, KaldiRecognizer
    

model_path = "models/vosk-model-small-en-in-0.4"

if not os.path.exists(model_path):
    print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit(1)    

model = Model(model_path)

rec = KaldiRecognizer(model, 16000)

audio_queue = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    audio_queue.put(bytes(indata))

def process_audio():
    print("Listening for audio....")  
    partial_text = ""
    with sd.RawInputStream(samplerate=16000,blocksize=8000,
                           dtype="int16",channels=1,callback=audio_callback):
        while True:
            data = audio_queue.get()
            if rec.AcceptWaveform(data):
                fr = rec.Result()
                text = eval(fr).get('text','')
                if text :
                    print("\033[92mYou said: \033[0m", text)
                else:
                    partial_result = rec.PartialResult()
                    word = eval(partial_result).get('partial','')
                    if word and word != partial_text:
                        print("\033[92mYou said: \033[0m", word)
                        partial_text = word


process_audio()