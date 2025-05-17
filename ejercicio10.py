import speech_recognition as sr

def listar_microfonos():
    """
    Lista todos los micrófonos disponibles detectados por la biblioteca SpeechRecognition.
    """
    print("Buscando micrófonos disponibles...")
    try:
        mic_names = sr.Microphone.list_microphone_names()
        
        if not mic_names:
            print("No se encontraron micrófonos disponibles.")
            print("Asegúrate de tener un micrófono conectado y configurado,")
            print("y de que las bibliotecas de audio necesarias (como PyAudio) estén instaladas.")
            return

        print("\nMicrófonos encontrados:")
        for index, name in enumerate(mic_names):
            print(f"  Índice: {index} - Nombre: {name}")
        
        print(f"\nTotal de {len(mic_names)} micrófonos encontrados.")
        print("Puedes usar el 'Índice' en scripts posteriores para seleccionar un micrófono específico.")

    except Exception as e:
        print(f"Ocurrió un error al intentar listar los micrófonos: {e}")
        print("Esto podría indicar un problema con la instalación de SpeechRecognition o sus dependencias de audio (PyAudio).")

if __name__ == "__main__":
    listar_microfonos()