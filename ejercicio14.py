import assemblyai as aai
import os
import time

# --- Configuración ---
directorio_script = os.path.dirname(os.path.abspath(__file__))

ASSEMBLYAI_API_KEY = "dd131db56c334ea1bba23e98ee8dd004"

# Ruta al archivo de audio a transcribir
nombre_carpeta_audio = "audios_grabados"
nombre_archivo_audio_local = "audio_grabado.wav"
ruta_audio_local = os.path.join(directorio_script, nombre_carpeta_audio, nombre_archivo_audio_local)

if ASSEMBLYAI_API_KEY == "TU_API_KEY_DE_ASSEMBLYAI_AQUI":
    print("Error: Por favor, reemplaza 'TU_API_KEY_DE_ASSEMBLYAI_AQUI' con tu API key real de AssemblyAI en el script.")
    exit()

if not os.path.exists(ruta_audio_local):
    print(f"Error: El archivo de audio '{ruta_audio_local}' no fue encontrado.")
    exit()
# --- Fin de la Configuración ---

def transcribir_con_assemblyai(api_key, ruta_archivo_audio):
    """
    Sube un archivo de audio a AssemblyAI y lo transcribe.
    """
    aai.settings.api_key = api_key
    
    transcriber = aai.Transcriber()

    print(f"Subiendo archivo '{ruta_archivo_audio}' a AssemblyAI...")
    try:
        # Sube el archivo local y obtiene una URL de AssemblyAI para ese archivo
        upload_url = transcriber.upload_file(ruta_archivo_audio)
        if not upload_url:
            print("Error: No se pudo subir el archivo a AssemblyAI.")
            return
        print(f"Archivo subido exitosamente. URL de AssemblyAI: {upload_url}")

    except Exception as e:
        print(f"Error durante la subida del archivo: {e}")
        return

    # Configurar la transcripción
 
    config = aai.TranscriptionConfig(language_code="es") # Para español general

    print("Enviando solicitud de transcripción...")
    try:
        transcript = transcriber.transcribe(upload_url, config=config)
        # La llamada a transcribe es asíncrona por defecto, pero el SDK maneja el polling.
        # El objeto 'transcript' se llenará cuando la transcripción esté completa.

        if transcript.status == aai.TranscriptStatus.error:
            print(f"Error en la transcripción: {transcript.error}")
            return
        
        if transcript.text:
            print("\n--- Transcripción de AssemblyAI ---")
            print(transcript.text)
            
            if transcript.confidence:
                 print(f"\nConfianza general de la transcripción: {transcript.confidence:.2f}")


        else:
            print("No se obtuvo texto en la transcripción (puede que el audio esté vacío o no contenga habla).")

    except Exception as e:
        print(f"Ocurrió un error durante la transcripción con AssemblyAI: {e}")


if __name__ == "__main__":
    transcribir_con_assemblyai(ASSEMBLYAI_API_KEY, ruta_audio_local)