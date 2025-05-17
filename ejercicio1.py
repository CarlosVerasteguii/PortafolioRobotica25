# Importar la función necesaria de TensorFlow Keras
from tensorflow.keras.utils import load_img

# --- Configuración ---
nombre_carpeta_imagenes = 'imagenes_para_ejercicio1'
nombre_original_imagen = 'miperro.jpeg' 

ruta_relativa_imagen = f"{nombre_carpeta_imagenes}/{nombre_original_imagen}"

# Dimensiones a las que se redimensionará la imagen (ancho, alto)
ancho_deseado = 100
alto_deseado = 177
# --- Fin de la Configuración ---

try:
    # Cargar la imagen desde el archivo usando la ruta relativa
    # - target_size: Redimensiona la imagen a (ancho_deseado, alto_deseado)
    # - color_mode: "grayscale" la convierte a escala de grises
    print(f"Intentando cargar la imagen desde: {ruta_relativa_imagen}")
    img = load_img(
        ruta_relativa_imagen,
        target_size=(ancho_deseado, alto_deseado),
        color_mode="grayscale"
    )

    # Mostrar información sobre la imagen procesada
    print(f"Imagen cargada: {nombre_original_imagen}")
    print(f"Dimensiones después de redimensionar (ancho, alto): {img.size}")
    print(f"Modo de color: {img.mode}")

    # Mostrar la imagen procesada
    print("Mostrando la imagen procesada...")
    img.show()

except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo en '{ruta_relativa_imagen}'.")
    print(
        f"Asegúrate de que la carpeta '{nombre_carpeta_imagenes}' exista dentro de 'Ejercicios' "
        f"y que '{nombre_original_imagen}' esté dentro de ella."
    )
    print(f"La ruta completa que se intentó cargar es relativa a la ubicación del script.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")