# Importar las funciones necesarias
from tensorflow.keras.utils import load_img
import matplotlib.pyplot as plt # Para mostrar la imagen
import os # Para manejar rutas de archivo de forma robusta

# --- Configuración ---
# Nombre de la carpeta donde está la imagen (relativa al script)
nombre_carpeta_imagenes = 'imagenes_para_ejercicio1'
nombre_original_imagen = 'miperro.jpeg' # Asegúrate que este sea el nombre exacto

# Obtener la ruta absoluta del directorio donde se encuentra este script
directorio_script = os.path.dirname(os.path.abspath(__file__))

# Construir la ruta absoluta a la imagen
ruta_absoluta_imagen = os.path.join(directorio_script, nombre_carpeta_imagenes, nombre_original_imagen)

# Dimensiones a las que se redimensionará la imagen (ancho, alto)
ancho_deseado = 620
alto_deseado = 350
# --- Fin de la Configuración ---

try:
    # Cargar la imagen desde el archivo
    # - target_size: Redimensiona la imagen a (ancho_deseado, alto_deseado)
    # - color_mode: "grayscale" la convierte a escala de grises
    print(f"Intentando cargar la imagen desde: {ruta_absoluta_imagen}")
    img = load_img(
        ruta_absoluta_imagen,
        target_size=(ancho_deseado, alto_deseado),
        color_mode="grayscale"
    )

    # Mostrar información sobre la imagen procesada
    print(f"Imagen cargada: {nombre_original_imagen}")
    print(f"Dimensiones después de redimensionar (ancho, alto): {img.size}") # img.size devuelve (ancho, alto)
    print(f"Modo de color: {img.mode}") # Debería ser 'L' para escala de grises

    # Mostrar la imagen procesada usando matplotlib
    print("Mostrando la imagen procesada con Matplotlib...")
    plt.imshow(img, cmap='gray') # cmap='gray' es importante para imágenes en escala de grises
    # plt.imshow(img) # Si no se especifica cmap, matplotlib puede usar un mapa de color por defecto que no se vea gris
    
    # Ocultar los ejes y ticks
    plt.xticks([])
    plt.yticks([])
    
    plt.title(f"Imagen Procesada: {nombre_original_imagen}") # Título opcional
    plt.show() # Muestra la figura

except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo en '{ruta_absoluta_imagen}'.")
    print(f"Asegúrate de que la carpeta '{nombre_carpeta_imagenes}' y el archivo '{nombre_original_imagen}' existan en la ubicación correcta.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")