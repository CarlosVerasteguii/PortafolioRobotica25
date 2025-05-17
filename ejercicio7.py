import cv2
import os

# --- Configuración ---
nombre_carpeta_salida = "fotos_capturadas" # Nombre de la carpeta para guardar las fotos
# La carpeta se creará en el mismo directorio donde se ejecuta el script.
directorio_script = os.path.dirname(os.path.abspath(__file__))
ruta_carpeta_salida = os.path.join(directorio_script, nombre_carpeta_salida)

if not os.path.exists(ruta_carpeta_salida):
    os.makedirs(ruta_carpeta_salida)
    print(f"Carpeta '{nombre_carpeta_salida}' creada en: {ruta_carpeta_salida}")
# --- Fin de la Configuración ---

# Inicializar la cámara web
# El '0' generalmente se refiere a la cámara web predeterminada.
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara web.")
    exit()

print("\nPresiona la BARRA ESPACIADORA para tomar una foto.")
print("Presiona la tecla 'q' para salir.")

contador_fotos = 0

while True:
    # Capturar un frame (imagen) de la cámara
    ret, frame = cap.read()

    if not ret:
        print("Error: No se pudo capturar el frame de la cámara.")
        break

    # Mostrar el frame en una ventana
    cv2.imshow("Camara Principal - Ejercicio 7", frame)

    # Esperar por una tecla presionada (1 milisegundo de espera)
    # El & 0xFF es una máscara que se usa a menudo para asegurar compatibilidad en sistemas de 64 bits.
    key = cv2.waitKey(1) & 0xFF

    # Si se presiona la tecla 'q', salir del bucle
    if key == ord('q'):
        print("Saliendo del programa...")
        break
    # Si se presiona la barra espaciadora, tomar una foto
    elif key == ord(' '): # ord(' ') obtiene el valor ASCII de la barra espaciadora
        contador_fotos += 1
        nombre_foto = f"foto_{contador_fotos}.png"
        ruta_foto_guardada = os.path.join(ruta_carpeta_salida, nombre_foto)
        
        # Guardar el frame actual como una imagen
        cv2.imwrite(ruta_foto_guardada, frame)
        print(f"Foto guardada: {ruta_foto_guardada}")

# Liberar la cámara y cerrar todas las ventanas de OpenCV
cap.release()
cv2.destroyAllWindows()

print(f"Se capturaron {contador_fotos} fotos en la carpeta '{nombre_carpeta_salida}'.")