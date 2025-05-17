import speech_recognition as sr

# --- Configuración ---
PALABRA_CLAVE = "ayuda" # Palabra que activará la acción
IDIOMA_RECONOCIMIENTO = "es-MX" # Lenguaje para la transcripción
# --- Fin de la Configuración ---

def escuchar_y_reaccionar():
    """
    Escucha el micrófono, transcribe el audio y reacciona si encuentra una palabra clave.
    """
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Calibrando para ruido ambiental (1 seg)... Por favor, silencio.")
        try:
            r.adjust_for_ambient_noise(source, duration=1)
            print("Calibración lista. Di algo (ej. 'necesito ayuda')...")
        except Exception as e:
            print(f"Error en calibración: {e}. Intentando continuar...")

        while True: # Bucle para escuchar continuamente hasta que se diga la palabra clave o haya error
            print("\nEscuchando...")
            try:
                # Escuchar audio, con un límite de tiempo para la frase
                audio_data = r.listen(source, phrase_time_limit=5)
                print("Procesando audio...")

                # Transcribir usando Google
                texto_hablado = r.recognize_google(audio_data, language=IDIOMA_RECONOCIMIENTO)
                texto_hablado_minusculas = texto_hablado.lower() # Convertir a minúsculas para la comparación
                print(f"Dijiste: '{texto_hablado}'")

                # Analizar el texto transcrito
                if PALABRA_CLAVE in texto_hablado_minusculas:
                    print(f"¡PALABRA CLAVE '{PALABRA_CLAVE.upper()}' DETECTADA!")
                    print("Acción: ¡Hola! ¿En qué puedo asistirte hoy?")
                    break # Salir del bucle si se detecta la palabra clave (opcional)
                else:
                    print(f"Palabra clave '{PALABRA_CLAVE}' no encontrada. Intenta de nuevo o di 'salir' para terminar.")

                if "salir" in texto_hablado_minusculas:
                    print("Saliendo de la aplicación...")
                    break


            except sr.WaitTimeoutError:
                print("No se detectó habla. ¿Sigues ahí?")
            except sr.UnknownValueError:
                print("No pude entender lo que dijiste. Intenta de nuevo.")
            except sr.RequestError as e:
                print(f"Error con el servicio de Google Speech Recognition; {e}")
                print("Verifica tu conexión a internet. Saliendo...")
                break # Salir si hay problemas de red
            except Exception as e:
                print(f"Error inesperado: {e}")
                break # Salir ante errores inesperados

if __name__ == "__main__":
    escuchar_y_reaccionar()
    print("Aplicación de voz finalizada.")