import cv2
import os
import numpy as np

# --- Configuración ---
directorio_script = os.path.dirname(os.path.abspath(__file__))

# Ruta al modelo LBPH entrenado con famosos
nombre_modelo = 'modeloLBPHFace.xml'
ruta_modelo_entrenado = os.path.join(directorio_script, 'modelo_entrenado', nombre_modelo)

# Ruta a la carpeta de datos de entrenamiento (para obtener los nombres de los famosos)
nombre_carpeta_datos_famosos = 'fotos_famosos_entrenamiento'
dataPathFamosos = os.path.join(directorio_script, nombre_carpeta_datos_famosos)

# Ruta al archivo Haar Cascade
ruta_haar_cascade = os.path.join(directorio_script, 'haarcascade_frontalface_default.xml')

# Dimensiones a las que se redimensionaron los rostros durante el entrenamiento
rostro_ancho_prediccion = 150
rostro_alto_prediccion = 150

# Umbral de confianza para LBPH (valores más bajos son mejores coincidencias)
umbral_confianza = 80 


if not os.path.exists(ruta_modelo_entrenado):
    print(f"Error: No se encontró el modelo entrenado en '{ruta_modelo_entrenado}'.")
    print("Ejecuta primero el script de entrenamiento para famosos.")
    exit()

if not os.path.exists(dataPathFamosos):
    print(f"Error: La carpeta de datos de famosos '{dataPathFamosos}' no existe.")
    print("Esta carpeta es necesaria para obtener los nombres de los famosos.")
    exit()
    
if not os.path.exists(ruta_haar_cascade):
    print(f"Error: No se encontró el archivo Haar Cascade en '{ruta_haar_cascade}'.")
    exit()

# Obtener la lista de nombres de los famosos (de las carpetas de entrenamiento)
# Debe coincidir con el orden de entrenamiento (usar sorted es una buena práctica)
lista_famosos_original = os.listdir(dataPathFamosos)
lista_famosos_filtrada = [famoso for famoso in lista_famosos_original if os.path.isdir(os.path.join(dataPathFamosos, famoso))]
if not lista_famosos_filtrada:
    print(f"Error: No se encontraron subcarpetas de famosos en '{dataPathFamosos}'.")
    exit()
lista_nombres_famosos = sorted(lista_famosos_filtrada)

print(f"Modelo a usar: {nombre_modelo}")
print(f"Famosos en el modelo: {lista_nombres_famosos}")
# --- Fin de la Configuración ---

# Cargar el modelo de reconocimiento facial LBPH
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read(ruta_modelo_entrenado)
print("Modelo LBPH de famosos cargado.")

# Cargar el clasificador Haar Cascade
face_cascade = cv2.CascadeClassifier(ruta_haar_cascade)
if face_cascade.empty():
    print("Error al cargar el clasificador Haar Cascade.")
    exit()
print("Clasificador Haar Cascade cargado.")

# Inicializar la cámara web
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara web.")
    exit()

print("\nMostrando video. Presiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer el frame. Saliendo...")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

    for (x, y, w, h) in faces:
        rostro_roi_gris = gray[y:y+h, x:x+w]
        
        # Redimensionar el rostro detectado al mismo tamaño que se usó en el entrenamiento
        rostro_para_prediccion = cv2.resize(
            rostro_roi_gris,
            (rostro_ancho_prediccion, rostro_alto_prediccion),
            interpolation=cv2.INTER_AREA
        )

        label, confidence = face_recognizer.predict(rostro_para_prediccion)

        nombre_predicho = "Desconocido"
        color_texto = (0, 0, 255) # Rojo

        if confidence < umbral_confianza: # Para LBPH, menor confianza es mejor
            if 0 <= label < len(lista_nombres_famosos):
                nombre_predicho = lista_nombres_famosos[label]
                color_texto = (0, 255, 0) # Verde
            else:
                # Esto no debería ocurrir si el entrenamiento y la lista de nombres son consistentes
                nombre_predicho = f"Etiqueta Fuera Rango ({label})" 
        
        # Mostrar nombre y confianza
        texto_mostrar = f"{nombre_predicho} ({confidence:.0f})"
        cv2.putText(frame, texto_mostrar, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_texto, 2)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color_texto, 2)

    cv2.imshow('Reconocimiento de Famosos - Ejercicio 9', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Programa de predicción finalizado.")