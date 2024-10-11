import pyttsx3 as voz
import speech_recognition as sr
import subprocess as sub
from datetime import datetime
from pydub import AudioSegment
import pyaudio
import wave
import time

# Configuración de la voz
voice = voz.init()
voices = voice.getProperty('voices')
voice.setProperty('voice', voices[0].id)
voice.setProperty('rate', 140)

# Función para que el asistente hable
def say(text):
    voice.say(text)
    voice.runAndWait()

# Función para grabar audio
def grabar_audio(archivo):
    chunk = 1024
    formato = pyaudio.paInt16
    canales = 1  # Mono
    tasa_muestreo = 44100

    p = pyaudio.PyAudio()
    stream = p.open(format=formato, channels=canales,
                    rate=tasa_muestreo, input=True,
                    frames_per_buffer=chunk)

    print("Grabando... (di 'detener' para parar)")

    frames = []

    recognizer = sr.Recognizer()
    
    while True:
        data = stream.read(chunk)
        frames.append(data)

        # Convertir la data a texto para comprobar si se dijo 'detener'
        try:
            comando = recognizer.recognize_google(data, language='es-MX')
            if 'detener' in comando:
                break
        except sr.UnknownValueError:
            continue  # Ignorar si no se entiende lo que se dijo

    print("Grabación terminada.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(archivo, 'wb') as wf:
        wf.setnchannels(canales)
        wf.setsampwidth(p.get_sample_size(formato))
        wf.setframerate(tasa_muestreo)
        wf.writeframes(b''.join(frames))

    # Convertir WAV a MP3
    audio = AudioSegment.from_wav(archivo)
    archivo_mp3 = archivo.replace('.wav', '.mp3')
    audio.export(archivo_mp3, format='mp3')

    print(f'Audio guardado como {archivo_mp3}')

while True:
    recognizer = sr.Recognizer()

    # Activar micrófono
    with sr.Microphone() as source:
        print('Escuchando ....')
        audio = recognizer.listen(source, phrase_time_limit=3)

    try:
        comando = recognizer.recognize_google(audio, language='es-MX')
        print(f'Creo que dijiste "{comando}"')

        comando = comando.lower()
        comando = comando.split(' ')
        print(f'comando: {comando}')

        if 'amigo' in comando:
            if 'grabar' in comando:
                grabar_audio('grabacion.wav')
            
            elif 'abre' in comando or 'abrir' in comando:
                sites = {
                    'google': 'https://www.google.com',
                    'youtube': 'https://www.youtube.com',
                    'instagram': 'https://www.instagram.com'
                }
                
                for i in sites.keys():
                    if i in comando:
                        sub.call(f'start edge.exe {sites[i]}', shell=True)
                        say(f'Abriendo {i}')
                        break
                    
            elif 'hora' in comando:
                time = datetime.now().strftime('%H:%M')
                say(f'Son las {time}')
                
            elif 'estoy' in comando:
                if 'triste' in comando:
                    say('¿Qué pasó? Te recomiendo bailar, no te preocupes, yo te quiero.')
                elif 'feliz' in comando:
                    say('¡Me alegro mucho! :)')
                elif 'asustado' in comando:
                    say('No tengas miedo, ¡abrázame!')
            
            elif 'termina' in comando or 'salir' in comando:
                say('Gracias')
                break
        
    except sr.UnknownValueError:
        print('No te entendí, por favor vuelve a intentarlo')
        say('No te entendí, por favor vuelve a intentarlo')
    except sr.RequestError as e:
        print(f'Error con el servicio de reconocimiento de voz: {e}')
    except Exception as e:
        print(f'Ocurrió un error: {e}')
