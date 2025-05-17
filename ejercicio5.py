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

lado_deseado = 256 # Haremos la imagen cuadrada de 256x256
# --- Fin de la Configuración ---

# --- Definición de Kernels ---
# Kernel de Desenfoque (Blur) - Promedio simple
kernel_blur = np.array([
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
]) / 9.0

# Kernel de Realce (Sharpen)
kernel_sharpen = np.array([
    [ 0, -1,  0],
    [-1,  5, -1],
    [ 0, -1,  0]
])

# Kernel de Detección de Bordes (Sobel Horizontal simple)
kernel_edge_h = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]
])
# --- Fin de Definición de Kernels ---

# --- Función para aplicar convolución ---
def aplicar_conv(imagen_gris, kernel):
    """Aplica un kernel de convolución a una imagen en escala de grises."""
    img_alto, img_ancho = imagen_gris.shape
    kernel_alto, kernel_ancho = kernel.shape
    
    # Calculamos cuánto padding se necesita en cada lado
    pad_alto = kernel_alto // 2
    pad_ancho = kernel_ancho // 2
    
    # Crear imagen de salida con ceros
    imagen_salida = np.zeros_like(imagen_gris)
    
    # Aplicar el kernel
    for i in range(pad_alto, img_alto - pad_alto):
        for j in range(pad_ancho, img_ancho - pad_ancho):
            # Extraer la región de la imagen (ROI) del tamaño del kernel
            roi = imagen_gris[i - pad_alto : i + pad_alto + 1, 
                              j - pad_ancho : j + pad_ancho + 1]
            # Aplicar la convolución (multiplicación elemento a elemento y suma)
            valor_pixel = np.sum(roi * kernel)
            imagen_salida[i, j] = valor_pixel
            
    # Ajustar valores para que estén en el rango visible [0, 255]
    imagen_salida = np.clip(imagen_salida, 0, 255)
    return imagen_salida.astype(np.uint8)
# --- Fin de función para aplicar convolución ---

try:
    # 1. Cargar la imagen, redimensionar y convertir a escala de grises
    print(f"Cargando imagen: {ruta_absoluta_imagen}")
    img_pil = load_img(
        ruta_absoluta_imagen,
        target_size=(lado_deseado, lado_deseado),
        color_mode="grayscale"
    )

    # 2. Convertir la imagen PIL a un arreglo de NumPy
    imagen_array_gris = img_to_array(img_pil)
    # img_to_array para grayscale devuelve (alto, ancho, 1), necesitamos (alto, ancho)
    imagen_array_gris_2d = imagen_array_gris.reshape((lado_deseado, lado_deseado))
    
    print(f"Forma del arreglo de imagen en escala de grises: {imagen_array_gris_2d.shape}")

    # 3. Aplicar los kernels de convolución
    print("Aplicando convoluciones...")
    img_blur = aplicar_conv(imagen_array_gris_2d, kernel_blur)
    img_sharpen = aplicar_conv(imagen_array_gris_2d, kernel_sharpen)

    # 4. Mostrar las imágenes
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    axs[0].imshow(imagen_array_gris_2d, cmap='gray')
    axs[0].set_title(f"Original ({lado_deseado}x{lado_deseado})")
    axs[0].axis('off')

    axs[1].imshow(img_blur, cmap='gray')
    axs[1].set_title("Desenfoque (Blur)")
    axs[1].axis('off')

    axs[2].imshow(img_sharpen, cmap='gray')
    axs[2].set_title("Realce (Sharpen)")
    axs[2].axis('off')
    
    plt.tight_layout()
    plt.show()

except FileNotFoundError:
    print(f"Error: No se pudo encontrar la imagen en '{ruta_absoluta_imagen}'.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")