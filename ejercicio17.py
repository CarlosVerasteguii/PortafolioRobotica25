import cv2
import os
import numpy as np

# --- Configuración ---
directorio_script = os.path.dirname(os.path.abspath(__file__))

# Adaptamos dataPath para usar nuestra carpeta de famosos
nombre_carpeta_datos = 'fotos_famosos_entrenamiento' 
dataPath = os.path.join(directorio_script, nombre_carpeta_datos)

# Ruta donde se guardará el modelo entrenado
ruta_modelo_salida = os.path.join(directorio_script, 'modelo_entrenado')
nombre_modelo_xml = 'modeloOpenCV_Ej17.xml' # Nombre específico para este modelo
ruta_completa_modelo_xml = os.path.join(ruta_modelo_salida, nombre_modelo_xml)

# Si el detector Haar se usa, estas serían para redimensionar el rostro detectado.
# Si no se usa detector, serían para redimensionar la imagen completa.
rostro_ancho_entrenamiento = 150
rostro_alto_entrenamiento = 150


if not os.path.exists(dataPath):
    print(f"Error: La carpeta de datos '{dataPath}' no existe.")
    exit()

if not os.path.exists(ruta_modelo_salida):
    os.makedirs(ruta_modelo_salida)
    print(f"Carpeta '{ruta_modelo_salida}' creada para guardar el modelo.")

peopleList = os.listdir(dataPath) # En el doc se llama peopleList
# Filtrar para asegurar que solo procesamos directorios
peopleList_filtrada = [person for person in peopleList if os.path.isdir(os.path.join(dataPath, person))]
if not peopleList_filtrada:
    print(f"Error: No se encontraron subcarpetas de personas en '{dataPath}'.")
    exit()
peopleList = sorted(peopleList_filtrada) # Usar la lista filtrada y ordenada

print(f"Personas encontradas para entrenamiento: {peopleList}")
# --- Fin de la Configuración ---

labels = []
facesData = []
label_counter = 0 

print("\nProcesando imágenes para entrenamiento...")

for nameDir in peopleList: # Itera sobre los nombres de las carpetas (personas)
    personPath = os.path.join(dataPath, nameDir)
    print(f"Leyendo imágenes de: {personPath} (Etiqueta: {label_counter})")
    
    rostros_persona_actual = 0
    for fileName in os.listdir(personPath): # Itera sobre los archivos en la carpeta de la persona
        imagePath = os.path.join(personPath, fileName)
        
        try:
            image = cv2.imread(imagePath)
            if image is None:
                print(f"  Advertencia: No se pudo leer '{fileName}'. Omitiendo.")
                continue

            # Convertir a escala de grises, como se muestra en el documento
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                       
            resized_gray_image = cv2.resize(gray_image, 
                                            (rostro_ancho_entrenamiento, rostro_alto_entrenamiento),
                                            interpolation=cv2.INTER_AREA)

            facesData.append(resized_gray_image)
            labels.append(label_counter)
            rostros_persona_actual += 1

        except Exception as e:
            print(f"  Error procesando '{fileName}': {e}")
            continue
            
    print(f"  Se procesaron {rostros_persona_actual} imágenes para {nameDir}.")
    label_counter += 1

if not facesData:
    print("Error: No se prepararon datos de rostros para el entrenamiento.")
    exit()

print(f"\nTotal de {len(facesData)} imágenes procesadas.")
print(f"Total de {len(labels)} etiquetas generadas para {label_counter} personas.")

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
print(f"\nUsando reconocedor: LBPH")

print("Entrenando el modelo...")
face_recognizer.train(facesData, np.array(labels))

# Guardar el modelo
face_recognizer.write(ruta_completa_modelo_xml)
print(f"Modelo entrenado y guardado en: {ruta_completa_modelo_xml}")

print("\nEntrenamiento completado (Ejercicio 17).")