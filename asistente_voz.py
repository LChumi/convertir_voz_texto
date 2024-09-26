import pyttsx3 as voz
import speech_recognition as sr
import subprocess as sub
from datetime import datetime

# Configuración de la voz
voice = voz.init()  # Inicialización de Voz
voices = voice.getProperty('voices')  # Acceder a la lista de voces disponibles 
voice.setProperty('voice', voices[0].id)  # Escoger la voz de la lista
voice.setProperty('rate', 140)  # Velocidad del asistente 

# Función para que el asistente hable
def say(text):
    voice.say(text)
    voice.runAndWait()
    
while True:
    recognizer = sr.Recognizer()
    
    # Activar micrófono
    with sr.Microphone() as source:
        print('Escuchando ....')
        audio = recognizer.listen(source, phrase_time_limit=3)  # Escucha el micrófono por 3 segundos
        
    try:  # Si entiende la petición entra a la lógica principal 
        comando = recognizer.recognize_google(audio, language='es-MX')
        print(f'Creo que dijiste "{comando}"')
        
        comando = comando.lower()
        comando = comando.split(' ')
        print(f'comando: {comando}')
        
        if 'amigo' in comando:
            if 'abre' in comando or 'abrir' in comando:
                sites = {
                    'google': 'google.com',
                    'youtube': 'youtube.com',  # Corrección aquí
                    'instagram': 'instagram.com'
                }
                
                for i in sites.keys():
                    if i in comando:
                        sub.call(f'start edge.exe {sites[i]}', shell=True)
                        say(f'Abriendo {i}')
                        break  # Salir después de abrir el sitio
                    
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
            
            elif 'termina' in comando or 'salir' in comando:  # Corrección aquí
                say('Gracias')
                break
        
    except sr.UnknownValueError:
        print('No te entendí, por favor vuelve a intentarlo')
        say('No te entendí, por favor vuelve a intentarlo')
    except sr.RequestError as e:
        print(f'Error con el servicio de reconocimiento de voz: {e}')
    except Exception as e:
        print(f'Ocurrió un error: {e}')
