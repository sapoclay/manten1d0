"""
Función 'mostrar_about'.

Imports:
    - tkinter as tk: Para la creación de interfaces gráficas.
    - os: Para realizar operaciones relacionadas con el sistema operativo.
    - preferencias: Para ajustar las preferencias de la interfaz.

Function:
    - mostrar_about(): Abre una ventana que muestra información sobre el programa. La ventana incluye un logotipo, la versión del programa y un 
    mensaje informativo. Además, si se ha seleccionado un tema oscuro en las preferencias, aplica el tema oscuro a las ventanas del proyecto.

"""

import tkinter as tk
import os
import preferencias

import os
import configparser

def obtener_version_actual():
    # Obtener el directorio del archivo que llama a la función
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    # Combinar el directorio con el nombre del archivo config.ini
    ruta_config = os.path.join(directorio_actual, 'config.ini')
    
    config = configparser.ConfigParser()
    config.read(ruta_config)
    return config['Version']['actual']



def mostrar_about():
     # Obtener la versión actual del programa desde el archivo de configuración
    version_actual = obtener_version_actual()
    
    about_window = tk.Toplevel()
    about_window.title("Acerca de")
    about_window.geometry("400x250")
    about_window.resizable(False, False)
    
    
    # Obtener la ruta absoluta del directorio del script
    dir_actual = os.path.dirname(os.path.realpath(__file__))
    ruta_imagen = os.path.join(dir_actual, "logo.png")

    # Cargar la imagen
    img = tk.PhotoImage(file=ruta_imagen)

    # Mostrar la imagen en un Label
    img_label = tk.Label(about_window, image=img)
    img_label.image = img  # Mantener una referencia para evitar que la imagen sea eliminada por el recolector de basura
    img_label.pack(pady=10)

    about_label = tk.Label(about_window, text=f"Manten1-d0 de Sistema Ubuntu\nVersión: {version_actual}\nEste programa realiza tareas de mantenimiento básico\nen sistemas Ubuntu.\nNo se dan garantías de ningún tipo.\n")
    about_label.pack(padx=20, pady=20)
    
    if preferencias.tema_seleccionado != "Claro":
            # Aplicar el tema seleccionado al mensaje personalizado
            preferencias.cambiar_tema(about_window, preferencias.tema_seleccionado)