import cv2
import os
import numpy as np

directorio_script = os.path.dirname(os.path.abspath(__file__))
nombre_carpeta_datos = 'fotos_famosos_entrenamiento' # Apunta a la carpeta de los famosos
dataPath = os.path.join(directorio_script, nombre_carpeta_datos)

# Ruta donde se guardará el modelo entrenado
ruta_modelo = os.path.join(directorio_script, 'modelo_entrenado')
nombre_modelo_xml = 'modeloLBPHFace.xml'
ruta_completa_modelo_xml = os.path.join(ruta_modelo, nombre_modelo_xml)

if not os.path.exists(dataPath):
    print(f"Error: La carpeta de datos '{dataPath}' no existe.")
    print(f"Crea la carpeta '{nombre_carpeta_datos}' y subcarpetas por famoso con sus imágenes.")
    exit()

if not os.path.exists(ruta_modelo):
    os.makedirs(ruta_modelo)
    print(f"Carpeta '{ruta_modelo}' creada para guardar el modelo.")

# Obtener la lista de nombres de las personas (nombres de las subcarpetas)
lista_personas = os.listdir(dataPath)
if not lista_personas:
    print(f"Error: No se encontraron subcarpetas de personas en '{dataPath}'.")
    exit()

print(f"Lista de personas encontradas: {lista_personas}")
# --- Fin de la Configuración ---
labels = [] # Etiquetas numéricas para cada rostro
facesData = [] # Arreglos NumPy de los rostros
label = 0 # Contador para asignar una etiqueta numérica única a cada persona

print("\nLeyendo imágenes y preparando datos para el entrenamiento...")

for nombre_persona in lista_personas:
    ruta_persona = os.path.join(dataPath, nombre_persona)
    print(f"Leyendo imágenes de: {nombre_persona}")

    if not os.path.isdir(ruta_persona): # Omitir archivos si los hay, solo directorios
        continue

    for nombre_archivo in os.listdir(ruta_persona):
        # Construir la ruta completa a la imagen
        ruta_imagen = os.path.join(ruta_persona, nombre_archivo)
        
        # Leer la imagen
        imagen = cv2.imread(ruta_imagen)
        if imagen is None:
            print(f"  No se pudo leer la imagen: {nombre_archivo}")
            continue
        imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        
       
        facesData.append(imagen_gris)
        labels.append(label) # Asignar la etiqueta numérica actual a este rostro
    
    label += 1 # Incrementar la etiqueta para la siguiente persona

if not facesData:
    print("Error: No se encontraron datos de rostros para entrenar.")
    exit()

print(f"\nTotal de {len(labels)} etiquetas leídas.")
print(f"Total de {len(facesData)} imágenes de rostros procesadas.")

# Crear el reconocedor facial LBPH
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

print("\nEntrenando el reconocedor facial LBPH...")
face_recognizer.train(facesData, np.array(labels))

face_recognizer.write(ruta_completa_modelo_xml)
print(f"Modelo LBPH entrenado y guardado en: {ruta_completa_modelo_xml}")

print("\nEntrenamiento completado.")