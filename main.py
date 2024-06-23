import speech_recognition as sr
import pyttsx3
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = recognizer.listen(source)
        try:
            print("Reconociendo...")
            text = recognizer.recognize_google(audio, language='es-ES')
            print(f"Usted dijo: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
            return None
        except sr.RequestError as e:
            print(f"Error al solicitar resultados; {e}")
            return None

def max_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(1.0, None)

def mute_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMute(1, None) 

def unmute_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMute(0, None)  # Des-silenciar (0 para des-silenciar)

def increase_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    currentVolumeDb = volume.GetMasterVolumeLevel()
    
    if currentVolumeDb < 0:
        volume.SetMasterVolumeLevel(currentVolumeDb + 1.0, None)
    else:
        speak("Ya estoy al máximo volumen")

def decrease_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    currentVolumeDb = volume.GetMasterVolumeLevel()
    
    if currentVolumeDb > -65:  
        volume.SetMasterVolumeLevel(currentVolumeDb - 1.0, None)
    else:
        speak("Ya estoy en el mínimo volumen o silenciado")

if __name__ == "__main__":
    speak("Hola, soy tu asistente personal. ¿En qué puedo ayudarte?")
    
    while True:
        command = listen()
        if command:
            if "salir" in command:
                speak("Adiós")
                break
            elif "subir al máximo" in command:
                max_volume()
                speak("Volumen al máximo")
            elif "subir volumen" in command:
                increase_volume()
                speak("Volumen subido")
            elif "bajar volumen" in command:
                decrease_volume()
                speak("Volumen bajado")
            elif "silenciar" in command:
                mute_volume()
                speak("Volumen silenciado")
            elif "quitar silencio" in command:
                unmute_volume()
                speak("Volumen restaurado")
            elif "hora" in command:
                from datetime import datetime
                now = datetime.now().strftime("%H:%M")
                speak(f"Son las {now}")
            else:
                speak(f"Lo siento, no entendí el comando: {command}")
