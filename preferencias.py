"""
Funciones y utilidades para la personalización de la interfaz gráfica de usuario.

Este módulo proporciona funciones y herramientas para cambiar el tema de la interfaz gráfica de usuario (GUI) de tkinter, así como para abrir una ventana de configuración para ajustar diferentes aspectos de la apariencia de la GUI.

Attributos:
    tema_seleccionado (str): Tema actualmente seleccionado para la GUI, que puede ser "Claro" o "Oscuro".
    ventanas_secundarias (list): Lista global para almacenar todas las ventanas secundarias abiertas.

Funciones:
    cambiar_tema(ventana, tema_seleccionado): Cambia el tema de la ventana y todos sus elementos hijos.
    abrir_ventana_configuracion(root): Abre una ventana de configuración para ajustar diferentes aspectos de la apariencia de la GUI. 
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tooltip import ToolTip    


# Variable global para almacenar el tema seleccionado

tema_seleccionado = "Claro"  # Tema predeterminado

def cambiar_tema(ventana, tema_seleccionado):
    """
    Cambia el tema de la ventana y todos sus elementos hijos.

    Args:
        ventana (tk.Tk or tk.Toplevel): Ventana a la que se aplicará el cambio de tema.
        tema_seleccionado (str): Tema seleccionado para aplicar a la ventana. Puede ser "Claro" o "Oscuro".
    """
    if tema_seleccionado == "Claro":
        bg_color = "lightgrey"
        fg_color = "black"
    else:
        bg_color = "black"
        fg_color = "white"

    # Aplicar estilos a los elementos
    for child in ventana.winfo_children():
        if isinstance(child, (tk.Label, tk.Button, tk.Entry, tk.Menu)):
            # Configurar colores directamente para widgets estándar
            child.config(background=bg_color, foreground=fg_color)
        elif isinstance(child, ttk.Widget):  # Manejo de widgets ttk
            # Crear y aplicar estilo personalizado para widgets ttk
            estilo = ttk.Style()
            estilo.configure("Custom.TLabel", background=bg_color, foreground=fg_color)
            estilo.configure("Custom.TButton", background=bg_color, foreground=fg_color)
            estilo.configure("Custom.TEntry", background=bg_color, foreground=fg_color)
            child.config(style="Custom.TLabel")
        elif isinstance(child, (tk.Frame, tk.Toplevel)):  # <-- Usar una tupla para especificar varios tipos
            # Establecer el color de fondo del frame
            child.config(background=bg_color)
            cambiar_tema(child, tema_seleccionado)  # Llamada recursiva para frames
     # Establecer el color de fondo de toda la ventana
    ventana.config(background=bg_color)


# Definir una lista global para almacenar todas las ventanas secundarias
ventanas_secundarias = []

def abrir_ventana_configuracion(root):
    """
    Abre una ventana de configuración para ajustar diferentes aspectos de la apariencia de la GUI.

    Args:
        root (tk.Tk): Ventana principal a la que está asociada la ventana de configuración.
    """
    def actualizar_tamanio_texto():
        size = int(size_spinner.get())
        size_label.config(text=f"Tamaño del Texto: {size}")
        for widget in root.winfo_children():
            actualizar_fuente(widget, size)

    def actualizar_fuente(widget, size):
        try:
            actual_font = str(widget.cget("font"))
            new_font = (actual_font.split()[0], size)
            widget.config(font=new_font)
        except tk.TclError:
            pass
        for child in widget.winfo_children():
            actualizar_fuente(child, size)

    def aplicar_cambios():
        global tema_seleccionado 
        nuevo_tema = tema_selector.get()  # Actualizar el tema seleccionado

        if nuevo_tema:
            # Aplicar el nuevo tema a la ventana principal y a las secundarias
            if root.winfo_exists():
                cambiar_tema(root, nuevo_tema)
            for ventana in ventanas_secundarias:
                if ventana.winfo_exists():
                    cambiar_tema(ventana, nuevo_tema)
            # Actualizar tema_seleccionado solo si se selecciona un nuevo tema
            tema_seleccionado = nuevo_tema
        else:
            messagebox.showwarning("Advertencia", "Debes seleccionar un tema antes de aplicar los cambios.")
        config_window.destroy()


    # Crear una nueva ventana para la configuración
    config_window = tk.Toplevel(root)
    config_window.title("Configuración")
    config_window.geometry("300x150")  # Tamaño personalizado
    config_window.resizable(False, False)
    # Agregar controles para la personalización
    size_frame = tk.Frame(config_window)  # Crear un marco para contener size_label y size_spinner
    size_frame.pack(pady=5)

    size_label = tk.Label(size_frame, text="Tamaño del Texto: 12", pady=10)
    size_label.pack(side="left", padx=10)

    size_spinner = tk.Spinbox(size_frame, from_=12, to=24, width=5, command=actualizar_tamanio_texto)
    size_spinner.pack(side="left", padx=10)

    # Resto de los elementos
    tema_selector = ttk.Combobox(config_window, values=["Claro", "Oscuro"], state="readonly")
    tema_selector.pack()

    apply_button = tk.Button(config_window, text="Aplicar", command=aplicar_cambios)
    apply_button.pack()
    ToolTip(apply_button, "Aplicar todos los cambios realizados")

    # Agregar una función de devolución de llamada para eliminar la ventana de la lista cuando se cierra
    def on_cerrar_ventana():
        ventanas_secundarias.remove(config_window)
        config_window.destroy()

    config_window.protocol("WM_DELETE_WINDOW", on_cerrar_ventana)

    # Agregar la ventana configuración a la lista de ventanas secundarias
    ventanas_secundarias.append(config_window)

