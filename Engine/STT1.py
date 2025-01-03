import subprocess
try:
    import speech_recognition as sr
    from mtranslate import translate
except ModuleNotFoundError:
    subprocess.run("pip install SpeechRecognition", shell=True)
    subprocess.run("pip install pyaudio", shell=True)    


def STT():
    r = sr.Recognizer()
    r.dynamic_energy_adjustment_damping = 0.8
    r.energy_threshold = 500
    r.dynamic_energy_threshold = False
    r.dynamic_energy_ratio = 0.9
    r.pause_threshold = 0.5
    r.operation_timeout = None
    r.non_speaking_duration = 0.5
    

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("\033[93mListening...\033[0m", flush=True)
        try:
            audio = r.listen(source,timeout=None)
            print("processing...", flush=True)
            text = r.recognize_google(audio, language='en-IN')
            print("\033[92mYou said: \033[0m", text)
        except sr.UnknownValueError:
            print("Could not understand audio", flush=True)    
        finally:
            print("\r", flush=True)   

    return text
while True:
    STT()
    