import speech_recognition as sr
import os

# --- Configuración ---
directorio_script = os.path.dirname(os.path.abspath(__file__))
nombre_carpeta_audio_salida = "audios_grabados"
ruta_carpeta_audio = os.path.join(directorio_script, nombre_carpeta_audio_salida)

# Crear la carpeta de salida si no existe
if not os.path.exists(ruta_carpeta_audio):
    os.makedirs(ruta_carpeta_audio)
    print(f"Carpeta '{nombre_carpeta_audio_salida}' creada en: {ruta_carpeta_audio}")

nombre_archivo_audio = "audio_grabado.wav" # Nombre del archivo a guardar
ruta_completa_audio_wav = os.path.join(ruta_carpeta_audio, nombre_archivo_audio)
# --- Fin de la Configuración ---

def grabar_y_guardar_audio():
    """
    Captura audio del micrófono y lo guarda en un archivo WAV.
    """
    r = sr.Recognizer()

    with sr.Microphone() as source: # Usar el micrófono predeterminado
        print("Ajustando para ruido ambiental (1 segundo)... Por favor, guarda silencio.")
        try:
            r.adjust_for_ambient_noise(source, duration=1)
            print("Calibración completada. ¡Comienza a hablar ahora!")
        except Exception as e:
            print(f"Error durante la calibración del ruido: {e}. Usando umbral por defecto.")
            # No es crítico no calibrar, pero puede afectar la calidad de r.listen()
        
        print("Escuchando...")
        try:
            # Escuchar el audio del micrófono
            # phrase_time_limit: duración máxima de la grabación después de que comience el habla
            audio_data = r.listen(source, phrase_time_limit=10) # Graba hasta 10 segundos de audio
            print("Grabación completada.")

            # Guardar el audio en un archivo WAV
            print(f"Guardando audio en '{ruta_completa_audio_wav}'...")
            with open(ruta_completa_audio_wav, "wb") as f:
                f.write(audio_data.get_wav_data())
            print("¡Audio guardado exitosamente como archivo WAV!")

        except sr.WaitTimeoutError: # Si r.listen() tuviera un 'timeout' y no se detectara habla
            print("No se detectó habla para grabar.")
        except Exception as e:
            print(f"Ocurrió un error durante la grabación o guardado: {e}")

if __name__ == "__main__":
    grabar_y_guardar_audio()