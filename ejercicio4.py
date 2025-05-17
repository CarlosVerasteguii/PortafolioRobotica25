# Importar las funciones necesarias
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np # Necesario para el arreglo de imagen
import os # Para manejo de rutas
import csv # Para escribir el archivo CSV

# --- Configuración ---
nombre_carpeta_imagenes = 'imagenes_para_ejercicio1'
nombre_original_imagen = 'miperro.jpeg'
nombre_archivo_csv_salida = 'imagen_en_array.csv' # Nombre del archivo CSV a generar

directorio_script = os.path.dirname(os.path.abspath(__file__))
ruta_absoluta_imagen = os.path.join(directorio_script, nombre_carpeta_imagenes, nombre_original_imagen)
ruta_absoluta_csv = os.path.join(directorio_script, nombre_archivo_csv_salida)

# Dimensiones de la imagen (alto, ancho)
alto_deseado = 620
ancho_deseado = 350
# --- Fin de la Configuración ---

try:
    # 1. Cargar la imagen, redimensionar y convertir a escala de grises
    print(f"Cargando imagen: {ruta_absoluta_imagen}")
    img_pil = load_img(
        ruta_absoluta_imagen,
        target_size=(alto_deseado, ancho_deseado), # (alto, ancho)
        color_mode="grayscale" # Importante para que el CSV sea más manejable (1 valor por píxel)
    )

    # 2. Convertir la imagen PIL a un arreglo de NumPy
    imagen_array = img_to_array(img_pil)
    # Para escala de grises, el shape será (alto, ancho, 1)

    print(f"Imagen cargada y convertida a arreglo con forma: {imagen_array.shape}")

    # 3. Escribir el arreglo de la imagen a un archivo CSV
    
    print(f"Guardando los valores de los píxeles en: {ruta_absoluta_csv}")
    with open(ruta_absoluta_csv, mode='w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        
        # Escribir cada fila de píxeles
        for fila_pixeles_con_canal in imagen_array:
            fila_para_escribir = [pixel[0] for pixel in fila_pixeles_con_canal]
            escritor_csv.writerow(fila_para_escribir)
            
    print(f"Archivo CSV '{nombre_archivo_csv_salida}' generado exitosamente.")



except FileNotFoundError:
    print(f"Error: No se pudo encontrar la imagen en '{ruta_absoluta_imagen}'.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")