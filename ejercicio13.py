import speech_recognition as sr
import os

# --- Configuración ---
directorio_script = os.path.dirname(os.path.abspath(__file__))
nombre_carpeta_audio = "audios_grabados" # Carpeta donde está el archivo WAV
nombre_archivo_wav = "audio_grabado.wav" # Nombre del archivo WAV a transcribir

ruta_completa_archivo_wav = os.path.join(directorio_script, nombre_carpeta_audio, nombre_archivo_wav)

if not os.path.exists(ruta_completa_archivo_wav):
    print(f"Error: El archivo de audio '{ruta_completa_archivo_wav}' no fue encontrado.")
    print("Asegúrate de haber grabado un audio (Ejercicio 12) o de tener un archivo WAV en la ubicación correcta.")
    exit()
# --- Fin de la Configuración ---

def transcribir_audio_desde_archivo(ruta_archivo):
    """
    Transcribe un archivo de audio WAV usando Google Web Speech API.
    """
    r = sr.Recognizer()

    # Cargar el archivo de audio
    # Usamos sr.AudioFile como fuente, similar a como usamos sr.Microphone
    with sr.AudioFile(ruta_archivo) as source:
        print(f"Cargando archivo de audio: {ruta_archivo}")
        try:
            # Leer el contenido completo del archivo de audio
            audio_data = r.record(source) # 'record' lee toda la duración del archivo
            print("Audio cargado, procesando para reconocimiento...")

            # Intentar reconocer el habla usando Google Web Speech API
            texto_reconocido = r.recognize_google(audio_data, language="es-MX")
            print(f"Google Web Speech API cree que el audio dice: '{texto_reconocido}'")

        except sr.UnknownValueError:
            print("Google Web Speech API no pudo entender el audio del archivo.")
        except sr.RequestError as e:
            print(f"No se pudieron obtener resultados del servicio de Google Web Speech API; {e}")
            print("Verifica tu conexión a internet o las cuotas de la API.")
        except Exception as e:
            print(f"Ocurrió un error inesperado durante el procesamiento del archivo: {e}")

if __name__ == "__main__":
    transcribir_audio_desde_archivo(ruta_completa_archivo_wav)