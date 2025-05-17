# Importar las funciones necesarias
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np
import os
import matplotlib.pyplot as plt

# --- Configuración ---
nombre_carpeta_imagenes = 'imagenes_para_ejercicio1'
nombre_original_imagen = 'miperro.jpeg' # O la foto de un integrante
directorio_script = os.path.dirname(os.path.abspath(__file__))
ruta_absoluta_imagen = os.path.join(directorio_script, nombre_carpeta_imagenes, nombre_original_imagen)

lado_deseado = 256 # Imagen cuadrada de 256x256
# --- Fin de la Configuración ---

# --- Definición de 6 Kernels ---
kernels = {
    "Desenfoque (Blur)": np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) / 9.0,
    "Realce (Sharpen)": np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]),
    "Detección Bordes H (Sobel)": np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]),
    "Detección Bordes V (Sobel)": np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]]),
    "Repujado (Emboss)": np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]]),
    "Desenfoque Gaussiano (Aprox)": np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]) / 16.0
}
kernel_nombres = list(kernels.keys())
# --- Fin de Definición de Kernels ---

# --- Función para aplicar convolución ---
def aplicar_conv(imagen_gris, kernel):
    img_alto, img_ancho = imagen_gris.shape
    kernel_alto, kernel_ancho = kernel.shape
    pad_alto = kernel_alto // 2
    pad_ancho = kernel_ancho // 2
    imagen_salida = np.zeros_like(imagen_gris)
    
    for i in range(pad_alto, img_alto - pad_alto):
        for j in range(pad_ancho, img_ancho - pad_ancho):
            roi = imagen_gris[i - pad_alto : i + pad_alto + 1, 
                              j - pad_ancho : j + pad_ancho + 1]
            valor_pixel = np.sum(roi * kernel)
            imagen_salida[i, j] = valor_pixel
            
    imagen_salida = np.clip(imagen_salida, 0, 255)
    return imagen_salida.astype(np.uint8)
# --- Fin de función para aplicar convolución ---

try:
    # 1. Cargar y preparar la imagen
    print(f"Cargando imagen: {ruta_absoluta_imagen}")
    img_pil = load_img(
        ruta_absoluta_imagen,
        target_size=(lado_deseado, lado_deseado),
        color_mode="grayscale"
    )
    imagen_array_gris = img_to_array(img_pil)
    imagen_array_gris_2d = imagen_array_gris.reshape((lado_deseado, lado_deseado))
    print(f"Forma de imagen procesada: {imagen_array_gris_2d.shape}")

    # 2. Aplicar los 6 kernels
    imagenes_convolucionadas = []
    print("Aplicando convoluciones...")
    for nombre in kernel_nombres:
        kernel = kernels[nombre]
        img_conv = aplicar_conv(imagen_array_gris_2d, kernel)
        imagenes_convolucionadas.append(img_conv)

    # 3. Mostrar las imágenes (Original + 6 convolucionadas)
    fig, axs = plt.subplots(2, 4, figsize=(20, 10)) # 2 filas, 4 columnas
    
    # Imagen Original
    axs[0, 0].imshow(imagen_array_gris_2d, cmap='gray')
    axs[0, 0].set_title(f"Original ({lado_deseado}x{lado_deseado})")
    axs[0, 0].axis('off')

    # Imágenes Convolucionadas
    idx_conv = 0 # Índice para las imágenes convolucionadas
    for i in range(2): # Filas de subplots
        for j in range(4): # Columnas de subplots
            if i == 0 and j == 0: # Ya pusimos la original
                continue
            if idx_conv < len(imagenes_convolucionadas):
                axs[i, j].imshow(imagenes_convolucionadas[idx_conv], cmap='gray')
                axs[i, j].set_title(kernel_nombres[idx_conv])
                axs[i, j].axis('off')
                idx_conv += 1
            else:
                axs[i, j].axis('off') # Ocultar subplots vacíos si los hay

    plt.tight_layout()
    plt.show()

except FileNotFoundError:
    print(f"Error: No se pudo encontrar la imagen en '{ruta_absoluta_imagen}'.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")