import os
import subprocess
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import preferencias
from cat_archivos import (
    BulkRenameApp,
    CopiaSeguridad,
    FileSearchApp,
    RestaurarCopiaSeguridad,
    cifrar_archivo,
    descifrar_archivo,
)
from cat_diccionario import abrir_ventana_diccionario, cargar_contenido_html
from cat_editorTexto import EditorTextos
from cat_informacion import Informacion
from cat_internet import RedTools, hacer_ping, reiniciar_tarjeta_red
from cat_navegadores import InstalarNavegadores, LimpiadorNavegadores
from cat_perfil import PerfilUsuario
from cat_redLocal import doble_clic, encontrar_dispositivos_en_red
from cat_sistema import (
    AdministrarProcesos,
    AplicacionBuscadorDuplicados,
    AplicacionesAutostart,
    DebInstalador,
    DesinstalarPaquetes,
    Limpieza,
    MonitorizarSistema,
    Repositorios,
    actualizar_sistema,
    consultaLogs,
    limpiar_cache,
    abrir_gestor_software,
)
from tooltip import ToolTip

def informacion_cat(self, mensaje_personalizado):
    """
Función informacion_cat.

Esta función se encarga de mostrar información en el área central de la interfaz gráfica.

Args:
    self: La instancia de la clase que llama a la función.
    mensaje_personalizado (str): Mensaje opcional que se mostrará en la interfaz.

Returns:
    No retorna ningún valor.

Steps:
    - Oculta todos los elementos en el área central.
    - Muestra el contenedor de texto para mostrar información.
    - Aplica el tema seleccionado a la nueva ventana si no es "Claro".
    - Actualiza el mensaje personalizado si existe, mostrándolo en un label.
    - Agrega una línea horizontal debajo del mensaje personalizado.
    - Muestra la información del sistema llamando a la función mostrar_informacion_sistema().
    - Empaqueta el contenedor de texto en el área central de la interfaz.
"""

    # Ocultar todos los elementos en el área central
    for widget in self.area_central.winfo_children():
        widget.pack_forget()

    # Mostrar el contenedor de texto para mostrar información
    self.contenedor_texto.pack(expand=True, fill="both", padx=10, pady=(20, 10))

    if preferencias.tema_seleccionado != "Claro":
        # Aplicar el tema seleccionado a la nueva ventana
        preferencias.cambiar_tema(self.area_central, preferencias.tema_seleccionado)

    # Actualizar el mensaje personalizado si existe
    if mensaje_personalizado:
        label_subcategorias = tk.Label(self.area_central, text=mensaje_personalizado, font=("Arial", 16, "bold"), bg="lightgrey", padx=10, pady=20)
        
        if preferencias.tema_seleccionado != "Claro":
            # Aplicar el tema seleccionado al mensaje personalizado
            preferencias.cambiar_tema(label_subcategorias, preferencias.tema_seleccionado)
            label_subcategorias.config(bg="black", fg="white")

        label_subcategorias.pack()

        # Dibujar una línea horizontal
        self.canvas = tk.Canvas(self.area_central, width=500, height=2, bg="lightgrey", highlightthickness=0)
        self.canvas.create_line(0, 1, 500, 1, fill="black")
        self.canvas.pack(pady=1) 

    # Mostrar la información del sistema
    self.mostrar_informacion_sistema()

    # Texto de información se muestre justo debajo de la línea
    self.texto_informacion.pack(expand=True, fill="both", padx=10, pady=(1, 30))  

    
def diccionario_cat(self, mensaje_personalizado):
    """
    Muestra la pantalla de la categoría DICCIONARIO en la interfaz gráfica.

    Args:
        self: La instancia de la clase que llama a la función.
        mensaje_personalizado (str): Mensaje opcional que se mostrará en la interfaz.

    Returns:
        No retorna ningún valor.
    """
    
    def aplicar_tema(widget):
        """Aplica el tema seleccionado a un widget si el tema no es 'Claro'."""
        if preferencias.tema_seleccionado != "Claro":
            preferencias.cambiar_tema(widget, preferencias.tema_seleccionado)
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry, tk.Text, tk.Listbox)):
                widget.config(bg="black", fg="white")
            else:
                widget.config(bg="black")

    # Ocultar todos los elementos en el área central
    self.contenedor_texto.pack_forget()
    for widget in self.area_central.winfo_children():
        widget.pack_forget()

    # Actualizar el mensaje personalizado si existe
    if mensaje_personalizado:
        label_subcategorias = tk.Label(
            self.area_central, text=mensaje_personalizado,
            font=("Arial", 16, "bold"), bg="lightgrey", padx=10, pady=20
        )
        aplicar_tema(label_subcategorias)
        label_subcategorias.pack()

        # Dibujar una línea horizontal
        canvas_linea = tk.Canvas(self.area_central, width=500, height=2, bg="lightgrey", highlightthickness=0)
        canvas_linea.create_line(0, 1, 500, 1, fill="black")
        canvas_linea.pack(pady=10)
    
    aplicar_tema(self.area_central)
    
    self.root.update_idletasks()  # Actualizar la interfaz gráfica antes de abrir la ventana del diccionario

    # Cargar el contenido HTML
    contenido_html = cargar_contenido_html()
    abrir_ventana_diccionario(contenido_html)  # Abrir la ventana del diccionario después de actualizar la interfaz

def sistema_cat(self, mensaje_personalizado):
    """
    Función sistema_cat.

    Esta función se encarga de realizar diversas tareas en el sistema operativo a través de la interfaz gráfica.

    Args:
        self: La instancia de la clase que llama a la función.
        mensaje_personalizado (str): Mensaje opcional que se mostrará en la interfaz.

    Returns:
        No retorna ningún valor.

    Steps:
        - Oculta el contenedor de texto y destruye los elementos en el área central.
        - Crea un label con el mensaje personalizado o uno predeterminado si no se proporciona.
        - Crea botones para realizar distintas tareas del sistema.
    """

    def aplicar_tema(widget):
        """Aplica el tema seleccionado a un widget si el tema no es 'Claro'."""
        if preferencias.tema_seleccionado != "Claro":
            preferencias.cambiar_tema(widget, preferencias.tema_seleccionado)
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry, tk.Text, tk.Listbox)):
                widget.config(bg="black", fg="white")
            else:
                widget.config(bg="black")

    def crear_boton(contenedor, texto, comando, fila, columna, tooltip):
        boton = tk.Button(contenedor, text=texto, command=comando)
        boton.grid(row=fila, column=columna, padx=10, pady=10)
        ToolTip(boton, tooltip)
        aplicar_tema(boton)
        return boton

    self.contenedor_texto.pack_forget()
    # Ocultar la etiqueta en la que se muestra la información del sistema
    for widget in self.area_central.winfo_children():
        widget.destroy()

    # Crear el label con el mensaje personalizado o un mensaje predeterminado si no se encuentra el mensaje personalizado
    if mensaje_personalizado:
        label_subcategorias = tk.Label(self.area_central, text=mensaje_personalizado, font=("Arial", 16, "bold"), bg="lightgrey", padx=10, pady=20)
    else:
        label_subcategorias = tk.Label(self.area_central, text="SISTEMA OPERATIVO", font=("Arial", 12))

    aplicar_tema(label_subcategorias)
    label_subcategorias.pack()

    # Dibujar una línea horizontal
    canvas_linea = tk.Canvas(self.area_central, width=500, height=2, bg="lightgrey", highlightthickness=0)
    canvas_linea.create_line(0, 1, 500, 1, fill="black")
    canvas_linea.pack(pady=10)

    contenedor_botones = tk.Frame(self.area_central, bg="lightgrey")
    contenedor_botones.pack()

    # Creación de botones con sus respectivas funciones y tooltips
    crear_boton(contenedor_botones, "Actualizar Sistema", lambda: actualizar_sistema(self.root), 0, 0, "Instala todas las actualizaciones disponibles para la versión de tu sistema operativo")
    crear_boton(contenedor_botones, "Limpiar Caché", lambda: limpiar_cache(self.root), 0, 1, "Limpia la caché del sistema operativo")
    crear_boton(contenedor_botones, "Abrir Gestor Software", abrir_gestor_software, 0, 2, "Instala o desinstala paquetes snap desde el gestor de software de Ubuntu")

    crear_boton(contenedor_botones, "Aplicaciones Inicio", lambda: AplicacionesAutostart(tk.Toplevel(self.area_central)), 1, 0, "Añade o elimina aplicaciones que se ejecuten al arrancar el equipo. Permite archivos .desktop")
    crear_boton(contenedor_botones, "Eliminar Archivo/s", Limpieza.eliminar_elemento, 1, 1, "Eliminar permanentemente archivos o carpetas del equipo")
    crear_boton(contenedor_botones, "Vaciar Papelera", Limpieza.vaciar_papelera, 1, 2, "Vacía la papelera de reciclaje del equipo")

    crear_boton(contenedor_botones, "Administrar Procesos", lambda: AdministrarProcesos(tk.Toplevel(self.area_central)), 2, 0, "Abre una ventana para administrar los procesos del sistema")
    crear_boton(contenedor_botones, "Buscar Archivos Duplicados", lambda: AplicacionBuscadorDuplicados(tk.Toplevel(self.area_central)), 2, 1, "Abre una ventana buscar archivos duplicados en el sistema")
    crear_boton(contenedor_botones, "Gestiona Repositorios", lambda: Repositorios(tk.Toplevel(self.area_central)), 2, 2, "Gestiona los repositorios del sistema")

    crear_boton(contenedor_botones, "Monitorizar", lambda: MonitorizarSistema(tk.Toplevel(self.area_central)).monitorizar_sistema(), 3, 0, "Genera un gráfico de los recursos del sistema en el momento actual")
    crear_boton(contenedor_botones, "Instalar .deb", lambda: DebInstalador().seleccionar_archivo().instalar_deb(), 3, 1, "Selecciona e instala un paquete .deb usando dpkg")
    crear_boton(contenedor_botones, "Desinstalar Paquetes", lambda: DesinstalarPaquetes(tk.Toplevel(self.area_central)), 3, 2, "Desinstalar paquetes instalados por el usuario")
    crear_boton(contenedor_botones, "Ver logs", lambda: consultaLogs(tk.Toplevel(self.area_central)), 4, 0, "Consulta los registros más importantes del sistema")
    
# Función para mostrar la categoría INTERNET
def internet_cat(self, mensaje_personalizado, entry_url=None):
    
    """
Función internet_cat.

Esta función se encarga de mostrar la categoría "Internet" en la interfaz gráfica, permitiendo al usuario realizar acciones relacionadas con la configuración de redes y la conectividad a internet.

Args:
    self: La instancia de la clase que llama a la función.
    mensaje_personalizado (str): Mensaje opcional que se mostrará en la interfaz.
    entry_url (tk.Entry, opcional): Objeto Entry para la entrada de la URL a la que hacer ping.

Returns:
    No retorna ningún valor.

Steps:
    - Oculta el contenedor de texto y destruye los elementos en el área central.
    - Crea un label con el mensaje personalizado o uno predeterminado si no se proporciona.
    - Obtiene las interfaces de red disponibles y muestra un Combobox para seleccionar una.
    - Crea un botón para reiniciar la tarjeta de red seleccionada.
    - Crea una caja de texto para escribir una URL y un botón para hacer ping a dicha URL.
    - Todos los botones tienen asociadas funciones para ejecutar las tareas correspondientes.
"""
    
    self.contenedor_texto.pack_forget()
    # Ocultar la etiqueta en la que se muestra la información del sistema
    for widget in self.area_central.winfo_children():
        widget.destroy()
    
    # Crear el label con el mensaje personalizado o un mensaje predeterminado si no se encuentra el mensaje personalizado
    if mensaje_personalizado:
        label_subcategorias = tk.Label(self.area_central, text=mensaje_personalizado, font=("Arial", 16, "bold"), bg="lightgrey", padx=10, pady=20)
        label_subcategorias.pack()
        # Dibujar una línea horizontal
        self.canvas = tk.Canvas(self.area_central, width=500, height=2, bg="lightgrey", highlightthickness=0)
        self.canvas.create_line(0, 1, 500, 1, fill="black")
        self.canvas.pack(pady=10)
    else:
        label_subcategorias = tk.Label(self.area_central, text="INTERNET", font=("Arial", 12))
        label_subcategorias.pack()

    # Obtener las interfaces de red disponibles
    informacion = Informacion()
    interfaces_red = informacion.obtener_interfaces_red()

    if not interfaces_red:
        # Si no se encontraron interfaces de red, mostrar un mensaje
        label_no_interfaces = tk.Label(self.area_central, text="No se encontraron interfaces de red disponibles.", font=("Arial", 14,"bold"))
        label_no_interfaces.pack(pady=20)
        # Aplicar el tema seleccionado a la nueva ventana
        preferencias.cambiar_tema(self.area_central, preferencias.tema_seleccionado)
        return

    # Crear un Combobox para seleccionar la interfaz de red
    label_selector = tk.Label(self.area_central, text="Seleccionar interfaz de red:", font=("Arial", 12, "bold"))
    label_selector.pack()

    seleccion_interfaz = tk.StringVar()
    combobox_interfaz = ttk.Combobox(self.area_central, textvariable=seleccion_interfaz, values=interfaces_red, state="readonly")
    combobox_interfaz.pack(pady=10)

    # Función para reiniciar la tarjeta de red seleccionada
    def reiniciar_tarjeta_seleccionada():
        interfaz_seleccionada = seleccion_interfaz.get()
        
        # Obtener las nuevas direcciones IP después de reiniciar la tarjeta de red
        informacion = Informacion()
        nueva_ip_local = informacion.obtener_direccion_ip_local()
        nueva_ip_publica = informacion.obtener_direccion_ip_publica()

        # Llamar a la función para reiniciar la tarjeta de red seleccionada
        reiniciar_tarjeta_red(interfaz_seleccionada, nueva_ip_local, nueva_ip_publica)


    # Botón para reiniciar la tarjeta de red seleccionada
    boton_reiniciar = tk.Button(self.area_central, text="Reiniciar Tarjeta de Red", command=reiniciar_tarjeta_seleccionada)
    boton_reiniciar.pack(pady=10)
    ToolTip(boton_reiniciar, "Reinicia la tarjeta de red. Tras unos segundos se volverá a iniciar automáticamente")
    
    # Dibujar una línea horizontal
    self.canvas = tk.Canvas(self.area_central, width=500, height=2, bg="lightgrey", highlightthickness=0)
    self.canvas.create_line(0, 1, 500, 1, fill="black")
    self.canvas.pack(pady=10)
    
    # Caja de texto para escribir la URL web
    label_url = tk.Label(self.area_central, text="Escribe una URL a la que hacer ping:", font=("Arial", 12, "bold"))
    label_url.pack()
    entry_url = tk.Entry(self.area_central, width=50)
    entry_url.pack(pady=5)
    # Botón para hacer ping a la URL ingresada
    boton_ping = tk.Button(self.area_central, text="Hacer Ping", command=lambda: hacer_ping(entry_url))
    boton_ping.pack(pady=10)
    ToolTip(boton_ping, "Hacer ping a una URL")
    # Dibujar una línea horizontal
    self.canvas = tk.Canvas(self.area_central, width=500, height=2, bg="lightgrey", highlightthickness=0)
    self.canvas.create_line(0, 1, 500, 1, fill="black")
    self.canvas.pack(pady=10)

    # Instanciar la clase RedTools y establecer el área central
    red_tools = RedTools(self.root)
    red_tools.set_area_central(self.area_central)

    # Botón para escanear puertos
    boton_escanear_puertos = tk.Button(self.area_central, text="Escanear Puertos", width=20, command=lambda: red_tools.escanear_puertos())    
    boton_escanear_puertos.pack(side=tk.LEFT, padx=10, pady=(0, 10), anchor="n")
    ToolTip(boton_escanear_puertos, "Escanea los puertos de una IP específica")

    # Botón para test de velocidad de internet
    boton_test_velocidad = tk.Button(self.area_central, text="Test Velocidad", width=20, command=red_tools.test_velocidad)
    boton_test_velocidad.pack(side=tk.LEFT, padx=10, pady=(0, 10), anchor="n")
    ToolTip(boton_test_velocidad, "Mide la velocidad de descarga y carga de la conexión a Internet")

    # Botón para diagnóstico de red
    boton_diagnostico_red = tk.Button(self.area_central, text="Diagnóstico Red", width=20, command=red_tools.diagnostico_red)
    boton_diagnostico_red.pack(side=tk.LEFT, padx=10, pady=(0, 10), anchor="n")
    ToolTip(boton_diagnostico_red, "Diagnostica problemas de conectividad de red con traceroute y netstat")


# Función para mostrar la pantalla de la categoría RED LOCAL
def red_local_cat(self, mensaje_personalizado):
    
    """
Función red_local_cat.

Esta función muestra la pantalla de la categoría "Red Local" en la interfaz gráfica, permitiendo al usuario buscar dispositivos en la red local y establecer conexiones con ellos, en caso de ser posible.

Args:
    self: La instancia de la clase que llama a la función.
    mensaje_personalizado (str): Mensaje opcional que se mostrará en la interfaz.

Returns:
    No retorna ningún valor.

Steps:
    - Limpia el área central de la interfaz gráfica.
    - Crea un label con el mensaje personalizado o uno predeterminado si no se proporciona.
    - Define una función interna para buscar equipos en la red local al hacer clic en un botón.
    - Al hacer clic en el botón, se muestra un mensaje temporal de búsqueda y luego se muestran los dispositivos encontrados en la red local.
    - Los dispositivos encontrados se muestran en una lista, permitiendo al usuario seleccionarlos para establecer conexiones.
"""

    # Limpiar el área central
    self.contenedor_texto.pack_forget()
    for widget in self.area_central.winfo_children():
        widget.destroy()

    # Crear el label con el mensaje personalizado o un mensaje predeterminado
    if mensaje_personalizado:
        label_subcategorias = tk.Label(self.area_central, text=mensaje_personalizado, font=("Arial", 16, "bold"), bg="lightgrey", padx=10, pady=20)
        label_subcategorias.pack()
        # Dibujar una línea horizontal
        self.canvas = tk.Canvas(self.area_central, width=500, height=2, bg="lightgrey", highlightthickness=0)
        self.canvas.create_line(0, 1, 500, 1, fill="black")
        self.canvas.pack(pady=10)
    else:
        label_subcategorias = tk.Label(self.area_central, text="RED LOCAL", font=("Arial", 12))
        label_subcategorias.pack()

    def buscar_equipos_red_local():
        # Deshabilitamos el botón de búsqueda
        boton_buscar.config(state="disabled")

        # Limpiar lista de dispositivos si ya existe
        if hasattr(self, "lista_dispositivos"):
            self.lista_dispositivos.pack_forget()
            self.lista_dispositivos.destroy()
            del self.lista_dispositivos

        # Limpiar mensaje de búsqueda si ya existe
        if hasattr(self, "mensaje_busqueda"):
            self.mensaje_busqueda.pack_forget()
            self.mensaje_busqueda.destroy()
            del self.mensaje_busqueda

        # Limpiar texto de dispositivos encontrados si ya existe
        if hasattr(self, "label_dispositivos"):
            self.label_dispositivos.pack_forget()
            self.label_dispositivos.destroy()
            del self.label_dispositivos

        # Limpiar aviso de conexión con Samba si ya existe
        if hasattr(self, "aviso_samba"):
            self.aviso_samba.pack_forget()
            self.aviso_samba.destroy()
            del self.aviso_samba

        # Mostrar mensaje temporal "Buscando equipos"
        self.mensaje_busqueda = tk.Label(self.area_central, text="Buscando equipos...")
        self.mensaje_busqueda.pack()
        # Aplicar el tema seleccionado a la nueva ventana
        preferencias.cambiar_tema(self.area_central, preferencias.tema_seleccionado)
        self.area_central.update()  # Actualizar la interfaz gráfica para mostrar el mensaje
        time.sleep(4)
        self.mensaje_busqueda.pack_forget()

        # Agregar el texto "Dispositivos en la red local:"
        self.label_dispositivos = tk.Label(self.area_central, text="Dispositivos encontrados en la red local:", font=("Arial", 12, "bold"))
        self.label_dispositivos.pack()

        dispositivos = encontrar_dispositivos_en_red()

        if dispositivos:
            # Crear lista de dispositivos
            self.lista_dispositivos = tk.Listbox(self.area_central, width=50, height=10)
            self.lista_dispositivos.pack()

            # Insertar dispositivos en la lista
            for dispositivo in dispositivos:
                self.lista_dispositivos.insert(tk.END, dispositivo)

            boton_buscar.config(state="normal")

            # Vincular función de doble clic
            self.lista_dispositivos.bind("<Double-1>", lambda event: doble_clic(event, self.lista_dispositivos))
        else:
            # No se encontraron dispositivos
            messagebox.showinfo("Buscar Equipos", "No se encontraron dispositivos en la red local.")

        # Aviso de conexión con Samba
        self.aviso_samba = tk.Label(self.area_central, text="Haz doble clic para establecer una conexión con Samba. Si es posible.", font=("Arial", 8))
        self.aviso_samba.pack()
        # Aplicar el tema seleccionado a la nueva ventana
        preferencias.cambiar_tema(self.area_central, preferencias.tema_seleccionado)

    # Crear el botón para buscar equipos en la red local
    boton_buscar = tk.Button(self.area_central, text="Buscar Equipos en Red Local", command=buscar_equipos_red_local)
    boton_buscar.pack(pady=10)
    ToolTip(boton_buscar, "Busca equipos conectados a tu red local (192.168.X.X)")



# Define la función para mostrar la pantalla de la categoría NAVEGADORES
def navegadores_cat(self, mensaje_personalizado):
    
    """
Función navegadores_cat.

Esta función muestra la pantalla de la categoría "Navegadores" en la interfaz gráfica, proporcionando opciones para limpiar la caché y el historial de los navegadores instalados.

Args:
    self: La instancia de la clase que llama a la función.
    mensaje_personalizado (str): Mensaje opcional que se mostrará en la interfaz.

Returns:
    No retorna ningún valor.

Steps:
    - Limpia el área central de la interfaz gráfica.
    - Crea un label con el mensaje personalizado o uno predeterminado si no se proporciona, seguido de una línea horizontal.
    - Crea un contendor Fram para organizar los botones de instalación de navegadores
    - Crea botones para instalar los navegadores
    - Crea un contenedor Frame para organizar los botones de limpieza de caché.
    - Crea botones para limpiar la caché de los navegadores Chrome, Firefox y Edge, si están instalados.
    - Crea un nuevo contenedor Frame para organizar los botones de limpieza de historial.
    - Crea botones para limpiar el historial de los navegadores Chrome, Firefox y Edge, si están instalados.
"""
    
    # Limpiar el área central
    self.contenedor_texto.pack_forget()
    for widget in self.area_central.winfo_children():
        widget.destroy()
    
    # Crear el label con el mensaje personalizado o un mensaje predeterminado
    if mensaje_personalizado:
        label_subcategorias = tk.Label(self.area_central, text=mensaje_personalizado, font=("Arial", 16, "bold"), bg="lightgrey", padx=10, pady=20)
        label_subcategorias.pack()
        # Dibujar una línea horizontal
        self.canvas = tk.Canvas(self.area_central, width=500, height=2, bg="lightgrey", highlightthickness=0)
        self.canvas.create_line(0, 1, 500, 1, fill="black")
        self.canvas.pack(pady=10)
    else:
        label_subcategorias = tk.Label(self.area_central, text="NAVEGADORES", font=("Arial", 12))
        label_subcategorias.pack()
        # Dibujar una línea horizontal
        self.canvas = tk.Canvas(self.area_central, width=500, height=2, bg="lightgrey", highlightthickness=0)
        self.canvas.create_line(0, 1, 500, 1, fill="black")
        self.canvas.pack(pady=10)
        
    # Contenedor para los botones de abrir navegadores
    frame_botones_abrir = tk.Frame(self.area_central)
    frame_botones_abrir.pack(pady=10)

    def abrir_chrome():
        try:
            subprocess.run(['google-chrome'])
        except Exception as e:
            print(f"Error al abrir Chrome: {e}")
            
    # Botón para abrir Chrome
    boton_abrir_chrome = tk.Button(frame_botones_abrir, text="Abrir Navegador Chrome", command=abrir_chrome)
    boton_abrir_chrome.pack(side="left", padx=5, pady=10)
    ToolTip(boton_abrir_chrome, "Abrir Google Chrome")
    
    def abrir_firefox():
        try:
            subprocess.run(['firefox'])
        except Exception as e:
            print(f"Error al abrir Firefox: {e}")

    # Botón para abrir Firefox
    boton_abrir_firefox = tk.Button(frame_botones_abrir, text="Abrir Navegador Firefox", command=abrir_firefox)
    boton_abrir_firefox.pack(side="left", padx=5, pady=10)
    ToolTip(boton_abrir_firefox, "Abrir Mozilla Firefox")
        
    def abrir_edge():
        try:
            subprocess.run(['microsoft-edge'])
        except Exception as e:
            print(f"Error al abrir Edge: {e}")

    # Botón para abrir Edge
    boton_abrir_edge = tk.Button(frame_botones_abrir, text="Abrir Navegador Edge", command=abrir_edge)
    boton_abrir_edge.pack(side="left", padx=5, pady=10)
    ToolTip(boton_abrir_edge, "Abrir Microsoft Edge")
    
    # Dibujar una línea horizontal
    self.canvas = tk.Canvas(self.area_central, width=500, height=2, bg="lightgrey", highlightthickness=0)
    self.canvas.create_line(0, 1, 500, 1, fill="black")
    self.canvas.pack(pady=10)
    
    # Contenedor para los botones de abrir navegadores
    frame_botones_abrir_incognito = tk.Frame(self.area_central)
    frame_botones_abrir_incognito.pack(pady=10)
    
    def abrir_chrome_incognito():
        try:
            subprocess.run(['google-chrome', '--incognito'])
        except Exception as e:
            print(f"Error al abrir Chrome: {e}")
    
    # Botón para abrir Chrome en modo incognito
    boton_abrir_chrome_incognito = tk.Button(frame_botones_abrir_incognito, text="Abrir Chrome Incognito", command=abrir_chrome_incognito)
    boton_abrir_chrome_incognito.pack(side="left", padx=5, pady=10)
    ToolTip(boton_abrir_chrome_incognito, "Abrir Google Chrome en modo incógnito")
    
    def abrir_firefox_incognito():
        try:
            subprocess.run(['firefox', '--private-window'])
        except Exception as e:
            print(f"Error al abrir Firefox: {e}")

    # Botón para abrir Firefox
    boton_abrir_firefox_incognito = tk.Button(frame_botones_abrir_incognito, text="Abrir Firefox Incognito", command=abrir_firefox_incognito)
    boton_abrir_firefox_incognito.pack(side="left", padx=5, pady=10)
    ToolTip(boton_abrir_firefox_incognito, "Abrir Mozilla Firefox en modo privado")

    def abrir_edge_incognito():
        try:
            subprocess.run(['microsoft-edge', '--inprivate'])
        except Exception as e:
            print(f"Error al abrir Edge: {e}")
            
    # Botón para abrir Edge
    boton_abrir_edge = tk.Button(frame_botones_abrir_incognito, text="Abrir Edge Incognito", command=abrir_edge_incognito)
    boton_abrir_edge.pack(side="left", padx=5, pady=10)
    ToolTip(boton_abrir_edge, "Abrir Microsoft Edge en modo InPrivate")
    
    # Dibujar una línea horizontal
    self.canvas = tk.Canvas(self.area_central, width=500, height=2, bg="lightgrey", highlightthickness=0)
    self.canvas.create_line(0, 1, 500, 1, fill="black")
    self.canvas.pack(pady=10)
    
    # Crear un contenedor Frame para los botones
    frame_botones_instalacion = tk.Frame(self.area_central)
    frame_botones_instalacion.pack()

    # Botones para instalar Chrome
    boton_chrome = tk.Button(frame_botones_instalacion, text="Instalar Chrome", command=InstalarNavegadores.instalar_chrome)
    boton_chrome.pack(side="left", padx=5, pady=10)
    ToolTip(boton_chrome, "Instalar Google Chrome)")
    
    # Botones para instalar Firefox
    boton_firefox = tk.Button(frame_botones_instalacion, text="Instalar Firefox", command=InstalarNavegadores.instalar_firefox)
    boton_firefox.pack(side="left", padx=5, pady=10)
    ToolTip(boton_firefox, "Instalar Mozilla Firefox)")

    # Botones para instalar Edge
    boton_edge = tk.Button(frame_botones_instalacion, text="Instalar Edge", command=InstalarNavegadores.instalar_edge)
    boton_edge.pack(side="left", padx=5, pady=10)
    ToolTip(boton_edge, "Instalar Microsoft Edge)")
    
    # Dibujar una línea horizontal
    self.canvas = tk.Canvas(self.area_central, width=500, height=2, bg="lightgrey", highlightthickness=0)
    self.canvas.create_line(0, 1, 500, 1, fill="black")
    self.canvas.pack(pady=10)
        
    # Crear un contenedor Frame para los botones
    frame_botones = tk.Frame(self.area_central)
    frame_botones.pack()

    # Botones para limpiar la caché
    boton_chrome = tk.Button(frame_botones, text="Limpiar Caché Chrome", command=lambda: LimpiadorNavegadores.limpiar_cache_chrome(self, boton_chrome, lambda mensaje: messagebox.showinfo("Resultado", mensaje)))
    boton_chrome.pack(side="left", padx=5, pady=10)
    ToolTip(boton_chrome, "Limpia la caché de Chrome (si está instalado)")

    boton_firefox = tk.Button(frame_botones, text="Limpiar Caché Firefox", command=lambda: LimpiadorNavegadores.limpiar_cache_firefox(self, boton_firefox, lambda mensaje: messagebox.showinfo("Resultado", mensaje)))
    boton_firefox.pack(side="left", padx=5, pady=10)
    ToolTip(boton_firefox, "Limpia la caché de Firefox (si está instalado)")

    boton_edge = tk.Button(frame_botones, text="Limpiar Caché Edge", command=lambda: LimpiadorNavegadores.limpiar_cache_edge(self, boton_edge, lambda mensaje: messagebox.showinfo("Resultado", mensaje)))
    boton_edge.pack(side="left", padx=5, pady=10)
    ToolTip(boton_edge, "Limpia la caché de Edge (si está instalado)")
    
    # Dibujar una línea horizontal
    self.canvas = tk.Canvas(self.area_central, width=500, height=2, bg="lightgrey", highlightthickness=0)
    self.canvas.create_line(0, 1, 500, 1, fill="black")
    self.canvas.pack(pady=10)

    # Crear una nueva fila para los botones de limpiar historial
    frame_botones_historial = tk.Frame(self.area_central)
    frame_botones_historial.pack()

    # Botones para limpiar el historial
    boton_chrome_historial = tk.Button(frame_botones_historial, text="Limpiar Historial Chrome", command=LimpiadorNavegadores.limpiar_historial_chrome)
    boton_chrome_historial.pack(side="left", padx=5, pady=10)
    ToolTip(boton_chrome_historial, "Limpia el historial de Chrome (si está instalado)")

    boton_firefox_historial = tk.Button(frame_botones_historial, text="Limpiar Historial Firefox", command=LimpiadorNavegadores.limpiar_historial_firefox)
    boton_firefox_historial.pack(side="left", padx=5, pady=10)
    ToolTip(boton_firefox_historial, "Limpia el historial de Firefox (si está instalado)")

    boton_edge_historial = tk.Button(frame_botones_historial, text="Limpiar Historial Edge", command=LimpiadorNavegadores.limpiar_historial_edge)
    boton_edge_historial.pack(side="left", padx=5, pady=10)
    ToolTip(boton_edge_historial, "Limpia el historial de Edge (si está instalado)")
    
def archivos_cat(self, mensaje_personalizado):
    """
    Actualiza el área central con un conjunto de botones y acciones asociadas para realizar operaciones
    de copia de seguridad, restauración de copia de seguridad, cifrado y descifrado de archivos.

    Parámetros:
        mensaje_personalizado (str): Un mensaje personalizado opcional que se muestra en lugar del mensaje predeterminado.

    Retorna:
        None

    Acciones:
        - Limpia el área central de cualquier widget previo.
        - Crea un label con un mensaje personalizado o un mensaje predeterminado.
        - Crea botones para realizar copia de seguridad, restaurar copia de seguridad, cifrar archivos y descifrar archivos.
        - Muestra ventanas de diálogo para seleccionar archivos o directorios según la acción requerida.
        - Realiza las operaciones correspondientes (copia de seguridad, restauración, cifrado o descifrado) cuando se hace clic en los botones.
        - Muestra mensajes de éxito o error en ventanas emergentes según el resultado de las operaciones.
    """
    # Limpiar el área central
    self.contenedor_texto.pack_forget()
    for widget in self.area_central.winfo_children():
        widget.destroy()
    
    # Crear el label con el mensaje personalizado o un mensaje predeterminado
    if mensaje_personalizado:
        label_subcategorias = tk.Label(self.area_central, text=mensaje_personalizado, font=("Arial", 16, "bold"), bg="lightgrey", padx=10, pady=20)
        label_subcategorias.pack()
        # Dibujar una línea horizontal
        self.canvas = tk.Canvas(self.area_central, width=500, height=2, bg="lightgrey", highlightthickness=0)
        self.canvas.create_line(0, 1, 500, 1, fill="black")
        self.canvas.pack(pady=10)
    else:
        label_subcategorias = tk.Label(self.area_central, text="ARCHIVOS", font=("Arial", 12))
        label_subcategorias.pack()
        # Dibujar una línea horizontal
        self.canvas = tk.Canvas(self.area_central, width=500, height=2, bg="lightgrey", highlightthickness=0)
        self.canvas.create_line(0, 1, 500, 1, fill="black")
        self.canvas.pack(pady=10)
        
    # Botón para realizar la copia de seguridad
    def realizar_copia_seguridad():
        # Obtener el directorio home del usuario
        directorio_home = os.path.expanduser("~")
        # Mostrar cuadros de diálogo para seleccionar origen y destino
        origen = filedialog.askdirectory(title="Seleccionar carpeta de origen", initialdir=directorio_home)
        # Si el usuario cancela la selección de carpeta, salimos de la función
        if not origen:
            # Mostrar mensaje de advertencia si falta alguna ruta
            messagebox.showwarning("Advertencia", "Al no seleccionar la carpeta de origen, se aborta la copia de seguridad.")
            return
        destino = filedialog.asksaveasfilename(title="Guardar como archivo .gz", initialdir=directorio_home, filetypes=(("Archivos comprimidos", "*.gz"), ("Todos los archivos", "*.*")))
        # Si el usuario cancela la selección de carpeta, salimos de la función
        if not destino:
            # Mostrar mensaje de advertencia si falta alguna ruta
            messagebox.showwarning("Advertencia", "Al escribir el nombre de un archivo .gz, se aborta la copia de seguridad.")
            return
        # Verificar que se hayan seleccionado el origen y el destino
        if origen and destino:
            # Crear una instancia de la clase CopiaSeguridad y realizar la copia de seguridad
            copia_seguridad = CopiaSeguridad(origen, destino)
            if copia_seguridad.realizar_copia_seguridad():
                # Mostrar mensaje de éxito al usuario
                messagebox.showinfo("Copia de seguridad", "Copia de seguridad realizada con éxito.")
            else:
                # Mostrar mensaje de error al usuario
                messagebox.showerror("Error", "Error al realizar la copia de seguridad.")
        else:
            # Mostrar mensaje de advertencia si falta alguna ruta
            messagebox.showwarning("Advertencia", "Por favor, seleccione el directorio de origen y destino.")
    
    # Función para restaurar la copia de seguridad
    def restaurar_copia_seguridad():
        # Obtener el directorio home del usuario
        directorio_home = os.path.expanduser("~")
        
        # Mostrar cuadro de diálogo para seleccionar carpeta de destino
        destino = filedialog.askdirectory(title="Seleccionar carpeta de destino", initialdir=directorio_home)
        
        # Si el usuario cancela la selección de carpeta, salimos de la función
        if not destino:
            # Mostrar mensaje de advertencia si falta alguna ruta
            messagebox.showwarning("Advertencia", "Al no seleccionar la carpeta de destino, se aborta la restauración de la copia de seguridad.")
            return
        
        # Seleccionar el archivo de copia de seguridad
        origen = filedialog.askopenfilename(title="Seleccionar archivo de copia de seguridad", initialdir=directorio_home, filetypes=(("Archivos comprimidos", "*.gz"), ("Todos los archivos", "*.*")))
        # Si el usuario cancela la selección de carpeta, salimos de la función
        if not origen:
            # Mostrar mensaje de advertencia si falta alguna ruta
            messagebox.showwarning("Advertencia", "Al no seleccionar el archivo .gz a restaurar, se aborta la restauración de la copia de seguridad.")
            return
        
        # Verificar que se hayan seleccionado el origen y el destino
        if origen and destino:
            # Crear una instancia de la clase RestaurarCopiaSeguridad y restaurar la copia de seguridad
            restaurar = RestaurarCopiaSeguridad(origen, destino)
            if restaurar.restaurar_copia_seguridad():
                # Mostrar mensaje de éxito al usuario
                messagebox.showinfo("Restaurar Copia de Seguridad", "Copia de seguridad restaurada con éxito.")
            else:
                # Mostrar mensaje de error al usuario
                messagebox.showerror("Error", "Se ha producido un Error al restaurar la copia de seguridad.")
        else:
            # Mostrar mensaje de advertencia si falta alguna ruta
            messagebox.showwarning("Advertencia", "Por favor, seleccione el directorio de origen y destino.")
    
    # Crear un frame para los botones y usar pack dentro de este frame
    frame_botones = tk.Frame(self.area_central)
    frame_botones.pack()

    # Botón para realizar la copia de seguridad
    boton_copia_seguridad = tk.Button(frame_botones, text="Copia de Seguridad", width=20, command=realizar_copia_seguridad)
    boton_copia_seguridad.pack(side=tk.LEFT, padx=5, pady=5)
    ToolTip(boton_copia_seguridad, "Realizar una copia de seguridad")

    # Botón para restaurar la copia de seguridad
    boton_restaurar_copia_seguridad = tk.Button(frame_botones, text="Restaurar Copia de Seguridad", width=30, command=restaurar_copia_seguridad)
    boton_restaurar_copia_seguridad.pack(side=tk.LEFT, padx=5, pady=5)
    ToolTip(boton_restaurar_copia_seguridad, "Restaurar una copia de seguridad")
    
    # Dibujar una línea horizontal
    self.canvas = tk.Canvas(self.area_central, width=500, height=2, bg="lightgrey", highlightthickness=0)
    self.canvas.create_line(0, 1, 500, 1, fill="black")
    self.canvas.pack(pady=10)
    
    # Crear un frame para los botones y usar pack dentro de este frame
    frame_botones_cifrado = tk.Frame(self.area_central)
    frame_botones_cifrado.pack()

    # Crear botones para cifrar y descifrar
    boton_cifrar = tk.Button(frame_botones_cifrado, text="Cifrar Archivos", width=20, command=cifrar_archivo)
    boton_cifrar.pack(side=tk.LEFT, padx=5, pady=5)
    ToolTip(boton_cifrar, "Cifrar Archivos")

    boton_descifrar = tk.Button(frame_botones_cifrado, text="Descifrar Archivos", width=20, command=descifrar_archivo)
    boton_descifrar.pack(side=tk.LEFT, padx=5, pady=5)
    ToolTip(boton_descifrar, "Descifrar Archivos")
    
    # Dibujar una línea horizontal
    self.canvas = tk.Canvas(self.area_central, width=500, height=2, bg="lightgrey", highlightthickness=0)
    self.canvas.create_line(0, 1, 500, 1, fill="black")
    self.canvas.pack(pady=10)
    
    # Función para abrir la ventana desde la que buscar archivos en el sistema
    def abrir_ventana_busqueda():
        ventana_busqueda = tk.Toplevel()
        FileSearchApp(ventana_busqueda)
    
    # Crear un frame para el botón de buscar archivo en el sistema
    frame_botones_archivos = tk.Frame(self.area_central)
    frame_botones_archivos.pack()

    # Crearmos el botón para abrir la ventana desde la que buscar archivos en el sistema
    boton_busqueda = tk.Button(frame_botones_archivos, text="Busca archivos", width=20, command=abrir_ventana_busqueda)
    boton_busqueda.pack(side=tk.LEFT, padx=5, pady=5)
    ToolTip(boton_busqueda, "Busca archivos en el sistema")
    
    # Función para abrir la ventana desde la que renombrar archivos de forma masiva
    def abrir_ventana_renombrado():
        ventana_renombrado = tk.Toplevel()
        BulkRenameApp(ventana_renombrado)

    # Crearmos el botón para abrir la ventana desde la que buscar archivos en el sistema
    boton_renombrado = tk.Button(frame_botones_archivos, text="Renombrar archivos", width=20, command=abrir_ventana_renombrado)
    boton_renombrado.pack(side=tk.LEFT, padx=5, pady=5)
    ToolTip(boton_renombrado, "Renombrar archivos de forma masiva")
    
def perfil_cat(self, mensaje_personalizado):
    """
    Función perfil_cat.

    Esta función se encarga de mostrar la pantalla de perfil de usuario en la interfaz gráfica.

    Args:
        self: La instancia de la clase que llama a la función.
        mensaje_personalizado (str): Mensaje opcional que se mostrará en la interfaz.

    Returns:
        No retorna ningún valor.

    Steps:
        - Oculta el contenedor de texto y destruye los elementos en el área central.
        - Crea un label con el mensaje personalizado o uno predeterminado si no se proporciona.
        - Crea un botón para modificar el perfil de usuario.
        - Aplica el tema seleccionado a los elementos creados.
    """

    def aplicar_tema(widget):
        """Aplica el tema seleccionado a un widget si el tema no es 'Claro'."""
        if preferencias.tema_seleccionado != "Claro":
            preferencias.cambiar_tema(widget, preferencias.tema_seleccionado)
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry, tk.Text, tk.Listbox)):
                widget.config(bg="black", fg="white")
            else:
                widget.config(bg="black")

    def crear_label_y_linea(mensaje, font_size, padding):
        """Crea un label con un mensaje y dibuja una línea horizontal."""
        label = tk.Label(self.area_central, text=mensaje, font=("Arial", font_size, "bold"), bg="lightgrey", padx=10, pady=padding)
        aplicar_tema(label)
        label.pack()
        
        canvas_linea = tk.Canvas(self.area_central, width=500, height=2, bg="lightgrey", highlightthickness=0)
        canvas_linea.create_line(0, 1, 500, 1, fill="black")
        aplicar_tema(canvas_linea)
        canvas_linea.pack(pady=10)

    def abrir_ventana_perfil():
        ventana_perfil = tk.Toplevel(self.area_central)
        PerfilUsuario(ventana_perfil)
        aplicar_tema(ventana_perfil)

    # Limpiar el área central
    self.contenedor_texto.pack_forget()
    for widget in self.area_central.winfo_children():
        widget.destroy()

    # Crear el label con el mensaje personalizado o un mensaje predeterminado
    if mensaje_personalizado:
        crear_label_y_linea(mensaje_personalizado, 16, 20)
    else:
        crear_label_y_linea("PERFIL USUARIO", 12, 0)

    # Crear un frame para los botones relacionados con el perfil de usuario
    frame_botones_perfil = tk.Frame(self.area_central, bg="lightgrey")
    aplicar_tema(frame_botones_perfil)
    frame_botones_perfil.pack()

    # Crear el botón para abrir la ventana desde la que modificar el perfil de usuario
    boton_perfil = tk.Button(frame_botones_perfil, text="Modificar Perfil Usuario", width=20, command=abrir_ventana_perfil)
    aplicar_tema(boton_perfil)
    boton_perfil.pack(side=tk.LEFT, padx=5, pady=5)
    ToolTip(boton_perfil, "Modifica tu perfil de usuario")
    
def notas_cat(self, mensaje_personalizado):
    """
    Función notas_cat.

    Esta función muestra la pantalla de la categoría "Notas" en la interfaz gráfica.

    Args:
        self: La instancia de la clase que llama a la función.
        mensaje_personalizado (str): Mensaje opcional que se mostrará en la interfaz.

    Returns:
        No retorna ningún valor.

    Steps:
        - Limpia el área central de la interfaz gráfica.
        - Crea un label con el mensaje personalizado o uno predeterminado si no se proporciona, seguido de una línea horizontal.
        - Crea un botón para lanzar el editor de texto desde cat_editorTexto.py
    """

    def aplicar_tema(widget):
        """Aplica el tema seleccionado a un widget si el tema no es 'Claro'."""
        if preferencias.tema_seleccionado != "Claro":
            preferencias.cambiar_tema(widget, preferencias.tema_seleccionado)
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry, tk.Text, tk.Listbox)):
                widget.config(bg="black", fg="white")
            else:
                widget.config(bg="black")

    def crear_label_y_linea(mensaje, font_size, padding):
        """Crea un label con un mensaje y dibuja una línea horizontal."""
        label = tk.Label(self.area_central, text=mensaje, font=("Arial", font_size, "bold"), bg="lightgrey", padx=10, pady=padding)
        aplicar_tema(label)
        label.pack()
        
        canvas_linea = tk.Canvas(self.area_central, width=500, height=2, bg="lightgrey", highlightthickness=0)
        canvas_linea.create_line(0, 1, 500, 1, fill="black")
        aplicar_tema(canvas_linea)
        canvas_linea.pack(pady=10)

    def abrir_ventana_toma_notas():
        ventana_notas = tk.Toplevel(self.area_central)
        toma_notas = EditorTextos(ventana_notas)

    # Limpiar el área central
    self.contenedor_texto.pack_forget()
    for widget in self.area_central.winfo_children():
        widget.destroy()

    # Crear el label con el mensaje personalizado o un mensaje predeterminado
    if mensaje_personalizado:
        crear_label_y_linea(mensaje_personalizado, 16, 20)
    else:
        crear_label_y_linea("TOMA NOTAS", 12, 0)

    # Crear un frame para los botones
    frame_botones_notas = tk.Frame(self.area_central)
    aplicar_tema(frame_botones_notas)
    frame_botones_notas.pack()

    # Botón para abrir la ventana para la toma de notas
    boton_tomar_notas = tk.Button(frame_botones_notas, text="Abrir Editor Texto", command=abrir_ventana_toma_notas)
    aplicar_tema(boton_tomar_notas)
    boton_tomar_notas.pack(padx=10, pady=10)
    ToolTip(boton_tomar_notas, "Abrir el Editor de Texto para tomar Notas")
    