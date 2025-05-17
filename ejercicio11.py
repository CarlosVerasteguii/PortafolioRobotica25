import speech_recognition as sr

def reconocer_voz_desde_microfono():
    """
    Captura audio del micrófono y lo transcribe usando Google Web Speech API.
    """
    # Crear un objeto Recognizer
    r = sr.Recognizer()

    # Usar el micrófono predeterminado como fuente de audio
    with sr.Microphone() as source:
        print("Ajustando el ruido ambiental, por favor espera un momento...")
        # Escucha durante 1 segundo para calibrar
        try:
            r.adjust_for_ambient_noise(source, duration=1)
            print("¡Calibración completada! Di algo...")
        except Exception as e:
            print(f"Error durante la calibración del ruido ambiental: {e}")
            print("Asegúrate de que el micrófono esté funcionando y no esté silenciado.")
            return

        try:
            # Escuchar el audio del micrófono
            # timeout: máximo de segundos que esperará una frase antes de rendirse (None = sin timeout)
            # phrase_time_limit: máximo de segundos que se permitirá que dure una frase
            audio = r.listen(source, timeout=None, phrase_time_limit=5) # Escucha por hasta 5 segundos de habla
            print("Audio capturado, procesando...")

            # Intentar reconocer el habla usando Google Web Speech API
            # Por defecto, reconoce en inglés. Para español de México: language="es-MX"
            texto_reconocido = r.recognize_google(audio, language="es-MX")
            print(f"Google Web Speech API cree que dijiste: '{texto_reconocido}'")

        except sr.WaitTimeoutError:
            print("No se detectó habla dentro del tiempo límite.")
        except sr.UnknownValueError:
            print("Google Web Speech API no pudo entender el audio.")
            print("Intenta hablar más claro o en un ambiente menos ruidoso.")
        except sr.RequestError as e:
            print(f"No se pudieron obtener resultados del servicio de Google Web Speech API; {e}")
            print("Verifica tu conexión a internet o las cuotas de la API.")
        except Exception as e:
            print(f"Ocurrió un error inesperado durante el reconocimiento: {e}")

if __name__ == "__main__":
    reconocer_voz_desde_microfono()