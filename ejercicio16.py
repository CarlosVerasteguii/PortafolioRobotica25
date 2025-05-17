# -*- coding: utf-8 -*-

def exploracion_codificaciones_carlos():
    print("--- Exploración de Codificaciones - Portafolio Robótica UAT ---")
    print("Alumno: Carlos Verástegui Cruz")
    print("¡Apurado con el portafolio final! (quedan ~9 horas)")

    # Escenario 1: Cadena con escapes comunes en registros o logs
    # Aquí \n es nueva línea, y \t es tabulación.
    # Imaginemos que un sistema guardó tu nombre con algún formato de escape.
    registro_con_escapes = "Usuario:\tCarlos Ver\\u00e1stegui Cruz\\nClase:\tRob\\u00f3tica 8 PM"
    print(f"\n--- Escenario 1: Registro con Escapes ---")
    print(f"Registro original: '{registro_con_escapes}'")

    try:
        # Procesar los escapes \uXXXX y también \n, \t
        # unicode_escape maneja \u, \U, \N{NOMBRE}, \x. Para \n, \t, etc., ya son interpretados por Python
        # si la cadena se define así. Si vinieran como '\\n', se necesitaría otro paso.
        # Para este caso, asumimos que \u son los problemáticos y el resto ya están "bien".
        registro_procesado = registro_con_escapes.encode('latin-1', 'backslashreplace').decode('unicode_escape')
        print(f"Registro procesado:\n{registro_procesado}")
    except Exception as e:
        print(f"Error procesando registro: {e}")

    # Escenario 2: Tu nombre y su representación en diferentes codificaciones
    tu_nombre = "Carlos Verástegui Cruz"
    print(f"\n--- Escenario 2: Tu Nombre en Diferentes Codificaciones ---")
    print(f"Nombre completo: '{tu_nombre}'")

    # UTF-8 (estándar moderno, maneja bien todos los caracteres)
    try:
        bytes_nombre_utf8 = tu_nombre.encode('utf-8')
        print(f"Nombre en UTF-8 (bytes): {bytes_nombre_utf8}")
        print(f"  Hexadecimal UTF-8: {bytes_nombre_utf8.hex()}")
        nombre_desde_utf8 = bytes_nombre_utf8.decode('utf-8')
        print(f"  Decodificado de UTF-8: '{nombre_desde_utf8}'")
    except Exception as e:
        print(f"Error con UTF-8 para tu nombre: {e}")

    # Latin-1 (ISO-8859-1, común en sistemas más antiguos, puede tener problemas con algunos caracteres)
    # El carácter 'á' (a con acento agudo) tiene representación en Latin-1.
    try:
        bytes_nombre_latin1 = tu_nombre.encode('latin-1')
        print(f"Nombre en Latin-1 (bytes): {bytes_nombre_latin1}")
        print(f"  Hexadecimal Latin-1: {bytes_nombre_latin1.hex()}")
        nombre_desde_latin1 = bytes_nombre_latin1.decode('latin-1')
        print(f"  Decodificado de Latin-1: '{nombre_desde_latin1}'")
    except UnicodeEncodeError as e:
        print(f"Error codificando a Latin-1: {e}. Algún carácter de tu nombre no está en Latin-1.")
    except Exception as e:
        print(f"Error con Latin-1 para tu nombre: {e}")


    # Escenario 3: Un mensaje para tu clase, simulando envío entre sistemas
    mensaje_clase = "¡Éxito en el portafolio de Robótica, UAT 8PM! La 'ñ' y los acentos como 'ó' son clave."
    print(f"\n--- Escenario 3: Mensaje para la Clase (Latin-1 a UTF-8) ---")
    print(f"Mensaje original: '{mensaje_clase}'")

    try:
        # Simular que el mensaje se guardó o transmitió en Latin-1
        bytes_mensaje_latin1 = mensaje_clase.encode('latin-1')
        print(f"Mensaje como bytes Latin-1: {bytes_mensaje_latin1}")

        # Lo recibimos y necesitamos usarlo en un sistema que espera UTF-8
        cadena_python_intermedia = bytes_mensaje_latin1.decode('latin-1')
        print(f"Mensaje decodificado de Latin-1 a string: '{cadena_python_intermedia}'")

        bytes_mensaje_utf8 = cadena_python_intermedia.encode('utf-8')
        print(f"Mensaje codificado a bytes UTF-8: {bytes_mensaje_utf8}")

        mensaje_final_verificado = bytes_mensaje_utf8.decode('utf-8')
        print(f"Mensaje final verificado (desde UTF-8): '{mensaje_final_verificado}'")
        assert mensaje_clase == mensaje_final_verificado # Pequeña prueba
        print("Conversión del mensaje de clase exitosa.")

    except UnicodeEncodeError as e:
        print(f"Error de codificación en Escenario 3: {e}. El mensaje contiene caracteres no representables en Latin-1.")
    except Exception as e:
        print(f"Error general en Escenario 3: {e}")


    # Escenario 4: El clásico error de interpretar mal los bytes (Mojibake)
    palabra_robotica_utf8 = "Robótica"
    bytes_robotica_utf8 = palabra_robotica_utf8.encode('utf-8') # Ejemplo: b'Rob\xc3\xb3tica'
    print(f"\n--- Escenario 4: Mojibake ---")
    print(f"'{palabra_robotica_utf8}' en bytes UTF-8: {bytes_robotica_utf8}")

    try:
        # Intentar leer esos bytes UTF-8 como si fueran Latin-1
        mojibake_robotica = bytes_robotica_utf8.decode('latin-1')
        print(f"Bytes UTF-8 de '{palabra_robotica_utf8}' decodificados (incorrectamente) como Latin-1: '{mojibake_robotica}'")
    except UnicodeDecodeError as e:
        print(f"Error (esperado) al intentar decodificar '{palabra_robotica_utf8}' (UTF-8) como Latin-1: {e}")


if __name__ == "__main__":
    exploracion_codificaciones_carlos()
    print("\n¡Fin de la demostración de codificaciones! ¡Mucha suerte con el portafolio, Carlos!")