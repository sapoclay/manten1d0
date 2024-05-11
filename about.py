import tkinter as tk
import os
import preferencias

def mostrar_about():
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

    about_label = tk.Label(about_window, text="Manten1-d0 de Sistema Ubuntu\nVersión: 0.5.3\nEste programa realiza tareas de mantenimiento básico\nen sistemas Ubuntu.\nNo se dan garantías de ningún tipo.\n")
    about_label.pack(padx=20, pady=20)
    
    if preferencias.tema_seleccionado != "Claro":
            # Aplicar el tema seleccionado al mensaje personalizado
            preferencias.cambiar_tema(about_window, preferencias.tema_seleccionado)