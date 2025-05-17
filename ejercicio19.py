import cv2
import os
import imutils # Para redimensionar manteniendo aspecto, como en el doc

# --- Configuración ---
directorio_script = os.path.dirname(os.path.abspath(__file__))

# Lista de personas para las cuales capturar rostros
nombres_personas_a_capturar = ["Carlos_Verastegui", "Otra_Persona"] 

# Carpeta principal donde se guardarán las subcarpetas con rostros
nombre_carpeta_dataset = "fotos_dataset_ej19" 
dataPath = os.path.join(directorio_script, nombre_carpeta_dataset)

# Ruta al archivo Haar Cascade
ruta_haar_cascade = os.path.join(directorio_script, 'haarcascade_frontalface_default.xml')

# Número de rostros a capturar por persona
num_rostros_a_capturar = 50
                            

# Dimensiones a las que se guardarán los rostros recortados
rostro_guardado_ancho = 150
rostro_guardado_alto = 150

# Índice de la cámara virtual de OBS
INDICE_CAMARA_OBS = 1 
if not os.path.exists(ruta_haar_cascade):
    print(f"Error: Archivo Haar Cascade '{ruta_haar_cascade}' no encontrado.")
    exit()

# Cargar el clasificador Haar Cascade
face_cascade = cv2.CascadeClassifier(ruta_haar_cascade)
if face_cascade.empty():
    print("Error al cargar el clasificador Haar Cascade.")
    exit()
print("Clasificador Haar Cascade cargado.")
# --- Fin de la Configuración ---

# Iniciar captura de video
print(f"Intentando abrir cámara con índice: {INDICE_CAMARA_OBS} (Esperando OBS Virtual Camera)")
cap = cv2.VideoCapture(INDICE_CAMARA_OBS, cv2.CAP_DSHOW)
if not cap.isOpened():
    print(f"Error: No se pudo abrir la cámara con índice {INDICE_CAMARA_OBS}.")
    exit()
print("Cámara virtual de OBS abierta.")

# Crear la carpeta principal del dataset si no existe
if not os.path.exists(dataPath):
    os.makedirs(dataPath)
    print(f"Carpeta principal del dataset '{dataPath}' creada.")


for nombre_persona in nombres_personas_a_capturar:
    ruta_persona = os.path.join(dataPath, nombre_persona)
    print(f"\nPreparando para capturar rostros de: {nombre_persona}")
    
    if not os.path.exists(ruta_persona):
        os.makedirs(ruta_persona)
        print(f"Carpeta creada para '{nombre_persona}' en: {ruta_persona}")
    else:
        print(f"Carpeta para '{nombre_persona}' ya existe en: {ruta_persona}")

    contador_rostros_guardados = 0
    print(f"Por favor, mira a la cámara (virtual). Se capturarán {num_rostros_a_capturar} imágenes.")
    print("Presiona 's' para iniciar/pausar la captura para esta persona, o 'q' para salir del todo.")
    
    capturando = False # Bandera para controlar la captura

    while contador_rostros_guardados < num_rostros_a_capturar:
        ret, frame = cap.read()
        if not ret or frame is None or frame.size == 0:
            print("Error al leer frame de la cámara.")
            break
        
        frame_resized = imutils.resize(frame, width=640)
        gray_frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
        
        frame_display = frame_resized.copy()

        detected_faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(60,60))

        for (x,y,w,h) in detected_faces:
            cv2.rectangle(frame_display, (x,y), (x+w,y+h), (0,255,0), 2)
            
            if capturando:
                rostro_recortado = gray_frame[y:y+h, x:x+w] # Recortar de la imagen gris
                rostro_guardar = cv2.resize(rostro_recortado, 
                                            (rostro_guardado_ancho, rostro_guardado_alto), 
                                            interpolation=cv2.INTER_AREA)
                
                nombre_archivo_rostro = f"rostro_{contador_rostros_guardados}.png"
                ruta_completa_rostro = os.path.join(ruta_persona, nombre_archivo_rostro)
                cv2.imwrite(ruta_completa_rostro, rostro_guardar)
                
                # Mostrar el número de foto guardada en el frame
                cv2.putText(frame_display, f"{contador_rostros_guardados+1}/{num_rostros_a_capturar}", 
                            (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0),2)

                contador_rostros_guardados += 1
                print(f"Guardado: {ruta_completa_rostro} ({contador_rostros_guardados}/{num_rostros_a_capturar})")
            
            break # Procesar solo el primer rostro detectado para simplificar esta captura

        # Mostrar estado de captura
        estado_texto = f"Capturando para {nombre_persona}: {contador_rostros_guardados}/{num_rostros_a_capturar}"
        if not capturando and contador_rostros_guardados < num_rostros_a_capturar:
            estado_texto += " (Pausado - Presiona 's')"
        elif capturando:
             estado_texto += " (Capturando...)"


        cv2.putText(frame_display, estado_texto, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
        cv2.imshow(f"Captura de Rostros - {nombre_persona}", frame_display)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Saliendo del programa...")
            cap.release()
            cv2.destroyAllWindows()
            exit()
        elif key == ord('s'):
            capturando = not capturando # Alternar estado de captura
            if capturando:
                print("Captura iniciada/reanudada.")
            else:
                print("Captura pausada.")
        
        if contador_rostros_guardados >= num_rostros_a_capturar: # Salir del while interno si ya se capturaron las fotos
            break 
            
    if contador_rostros_guardados < num_rostros_a_capturar and key != ord('q'):
        print(f"Advertencia: Solo se capturaron {contador_rostros_guardados} de {num_rostros_a_capturar} para {nombre_persona}.")
    elif contador_rostros_guardados >= num_rostros_a_capturar:
        print(f"Captura completada para {nombre_persona}.")


cap.release()
cv2.destroyAllWindows()
print("Proceso de captura de rostros finalizado para todas las personas.")