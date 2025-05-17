import cv2
import os
import numpy as np

# --- Configuración ---
directorio_script = os.path.dirname(os.path.abspath(__file__))

nombre_modelo_entrenado = 'modeloOpenCV_Ej17.xml' # O 'modeloLBPHFamosos.xml'
ruta_modelo_xml = os.path.join(directorio_script, 'modelo_entrenado', nombre_modelo_entrenado)

nombre_carpeta_datos_ref = 'fotos_famosos_entrenamiento' 
dataPathReferencia = os.path.join(directorio_script, nombre_carpeta_datos_ref)

ruta_haar_cascade = os.path.join(directorio_script, 'haarcascade_frontalface_default.xml')

rostro_ancho_referencia = 150
rostro_alto_referencia = 150
umbral_confianza_lbph = 85 

INDICE_CAMARA_OBS = 1 


if not os.path.exists(ruta_modelo_xml): 
    print(f"Error: Modelo '{ruta_modelo_xml}' no encontrado.")
    exit()
if not os.path.exists(dataPathReferencia):
    print(f"Error: Carpeta de datos de referencia '{dataPathReferencia}' no encontrada.")
    exit()
if not os.path.exists(ruta_haar_cascade):
    print(f"Error: Archivo Haar Cascade '{ruta_haar_cascade}' no encontrado.")
    exit()

lista_nombres_original = os.listdir(dataPathReferencia)
lista_nombres_filtrada = [nombre for nombre in lista_nombres_original if os.path.isdir(os.path.join(dataPathReferencia, nombre))]
if not lista_nombres_filtrada:
    print(f"Error: No se encontraron subcarpetas de personas en '{dataPathReferencia}'.")
    exit()
lista_nombres_personas = sorted(lista_nombres_filtrada)

print(f"Usando modelo: {nombre_modelo_entrenado}")
print(f"Personas en el modelo de referencia: {lista_nombres_personas}")

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read(ruta_modelo_xml)
print("Modelo de reconocimiento facial cargado.")

face_cascade = cv2.CascadeClassifier(ruta_haar_cascade)
if face_cascade.empty():
    print("Error al cargar el clasificador Haar Cascade.")
    exit()
print("Clasificador Haar Cascade cargado.")

print(f"Intentando abrir cámara con índice: {INDICE_CAMARA_OBS} (Esperando OBS Virtual Camera)")
cap = cv2.VideoCapture(INDICE_CAMARA_OBS, cv2.CAP_DSHOW) # Usar CAP_DSHOW en Windows

if not cap.isOpened():
    print(f"Error: No se pudo abrir la cámara con índice {INDICE_CAMARA_OBS}.")
    print("Posibles soluciones:")
    print("1. Asegúrate de que OBS Studio esté abierto.")
    print("2. Asegúrate de que la 'Cámara Virtual' esté INICIADA en OBS.")
    print("3. Verifica que el INDICE_CAMARA_OBS sea el correcto (usa el script listar_camaras_obs.py).")
    print("4. Intenta quitar ', cv2.CAP_DSHOW' de VideoCapture si no estás en Windows o si causa problemas.")
    exit()
print("Cámara virtual de OBS abierta exitosamente.")
# --- FIN DE MODIFICACIÓN ---

print("\nIniciando reconocimiento en tiempo real. Presiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer el frame de la cámara virtual. ¿OBS sigue transmitiendo?")
        break # Salir si no hay frame

    # Asegurarse de que el frame no esté vacío
    if frame is None or frame.size == 0:
        print("Frame vacío recibido de la cámara virtual.")
        continue

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detected_faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(60,60))

    for (x, y, w, h) in detected_faces:
        rostro_capturado_gris = gray_frame[y:y+h, x:x+w]
        rostro_preparado = cv2.resize(rostro_capturado_gris, 
                                      (rostro_ancho_referencia, rostro_alto_referencia), 
                                      interpolation=cv2.INTER_AREA)

        label_predicha, confianza = face_recognizer.predict(rostro_preparado)

        nombre_identificado = "Desconocido"
        color_display = (0, 0, 255) 

        if confianza < umbral_confianza_lbph:
            if 0 <= label_predicha < len(lista_nombres_personas):
                nombre_identificado = lista_nombres_personas[label_predicha]
                color_display = (0, 255, 0) 
            else:
                nombre_identificado = f"Etiqueta_Err({label_predicha})"
        
        texto_resultado = f"{nombre_identificado} ({confianza:.0f})"
        cv2.putText(frame, texto_resultado, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_display, 2)
        cv2.rectangle(frame, (x,y), (x+w, y+h), color_display, 2)

    cv2.imshow('Reconocimiento Facial con OBS - Ej18', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Programa de reconocimiento finalizado.")