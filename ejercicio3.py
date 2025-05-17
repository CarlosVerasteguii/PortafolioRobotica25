# Importar las funciones necesarias
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np
import os
import matplotlib.pyplot as plt

# --- Configuración ---
nombre_carpeta_imagenes = 'imagenes_para_ejercicio1'
nombre_original_imagen = 'miperro.jpeg'
directorio_script = os.path.dirname(os.path.abspath(__file__))
ruta_absoluta_imagen = os.path.join(directorio_script, nombre_carpeta_imagenes, nombre_original_imagen)

alto_deseado = 620
ancho_deseado = 350
# --- Fin de la Configuración ---

try:
    # 1. Cargar la imagen a color y redimensionarla
    print(f"Cargando imagen: {ruta_absoluta_imagen}")
    img_pil_color = load_img(
        ruta_absoluta_imagen,
        target_size=(alto_deseado, ancho_deseado),
        color_mode="rgb"
    )

    # 2. Convertir a arreglo NumPy
    imagen_array = img_to_array(img_pil_color)

    # 3. Aplicar tinte verdoso
    # Se atenúan los canales rojo y azul para dar predominancia al verde
    # Los valores de los canales están en el rango [0, 255]
    imagen_array[:, :, 0] *= 0.7  # Atenuar canal Rojo (R)
    # imagen_array[:, :, 1] *= 1.0 # Canal Verde (índice 1) se puede dejar o intensificar
    imagen_array[:, :, 2] *= 0.7  # Atenuar canal Azul (B)

    # Asegurar que los valores estén en el rango [0, 255] y sean enteros para visualización
    imagen_array_verdosa = np.clip(imagen_array, 0, 255).astype(np.uint8)

    # 4. Mostrar la imagen con tinte verdoso
    print(f"Mostrando imagen con tinte verdoso...")
    plt.imshow(imagen_array_verdosa)
    plt.title(f"Imagen con Tinte Verdoso ({ancho_deseado}x{alto_deseado})")
    plt.axis('off') # Ocultar ejes
    plt.show()

except FileNotFoundError:
    print(f"Error: No se pudo encontrar '{ruta_absoluta_imagen}'.")
except Exception as e:
    print(f"Error inesperado: {e}")