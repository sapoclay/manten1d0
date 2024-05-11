import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
from cat_diccionario import abrir_ventana_diccionario, cargar_contenido_html
from cat_internet import  reiniciar_tarjeta_red
from cat_internet import hacer_ping
from cat_sistema import actualizar_sistema, limpiar_cache, abrir_gestor_software
from cat_sistema import AplicacionesAutostart
from cat_sistema import AdministrarProcesos
from cat_sistema import AplicacionBuscadorDuplicados
from cat_sistema import Limpieza 
from cat_sistema import Repositorios
from cat_sistema import MonitorizarSistema
from cat_informacion import Informacion
from cat_redLocal import encontrar_dispositivos_en_red, doble_clic
from cat_navegadores import LimpiadorNavegadores
from tooltip import ToolTip    
import preferencias


def informacion_cat(self, mensaje_personalizado):
    # Ocultar todos los elementos en el área central
    for widget in self.area_central.winfo_children():
        widget.pack_forget()

    # Mostrar el contenedor de texto para mostrar información
    self.contenedor_texto.pack(expand=True, fill="both", padx=10, pady=(10, 0))

    if preferencias.tema_seleccionado != "Claro":
        # Aplicar el tema seleccionado a la nueva ventana
        preferencias.cambiar_tema(self.area_central, preferencias.tema_seleccionado)

    # Actualizar el mensaje personalizado si existe
    if mensaje_personalizado:
        label_subcategorias = tk.Label(self.area_central, text=mensaje_personalizado, font=("Arial", 16, "bold"), bg="lightgrey", padx=10, pady=20)
        
        if preferencias.tema_seleccionado != "Claro":
            # Aplicar el tema seleccionado al mensaje personalizado
            preferencias.cambiar_tema(label_subcategorias, preferencias.tema_seleccionado)
            label_subcategorias = tk.Label(self.area_central, text=mensaje_personalizado, font=("Arial", 16, "bold"), bg="black", fg="white", padx=10, pady=20)

        label_subcategorias.pack()
        # Agregar una línea horizontal debajo del botón
        separador = ttk.Separator(self.area_central, orient="horizontal")
        separador.pack(fill="x", pady=10, padx=40)

    # Mostrar la información del sistema
    self.mostrar_informacion_sistema()
    self.texto_informacion.pack(expand=True, fill="both", padx=0, pady=0)
    
# Función para mostrar la pantalla de la categoría DICCIONARIO
def diccionario_cat(self, mensaje_personalizado):
    # Ocultar todos los elementos en el área central
    self.contenedor_texto.pack_forget()
    for widget in self.area_central.winfo_children():
        widget.pack_forget()

    # Actualizar el mensaje personalizado si existe
    if mensaje_personalizado:
        label_subcategorias = tk.Label(self.area_central, text=mensaje_personalizado, font=("Arial", 16, "bold"), bg="lightgrey", padx=10, pady=20)
        label_subcategorias.pack()
         # Agregar una línea horizontal debajo del botón
        separador = ttk.Separator(self.area_central, orient="horizontal")
        separador.pack(fill="x", pady=10, padx=40)
        # Aplicar el tema seleccionado a la nueva ventana
        preferencias.cambiar_tema(self.area_central, preferencias.tema_seleccionado)

    self.root.update_idletasks()  # Actualizar la interfaz gráfica antes de abrir la ventana del diccionario

    # Cargar el contenido HTML
    contenido_html = cargar_contenido_html()
    abrir_ventana_diccionario(contenido_html)  # Abrir la ventana del diccionario después de actualizar la interfaz

# Función para realizar tareas en el SISTEMA
def sistema_cat(self, mensaje_personalizado):
    
    self.contenedor_texto.pack_forget()
    # Ocultar la etiqueta en la que se muestra la información del sistema
    for widget in self.area_central.winfo_children():
        widget.destroy()
    
    # Crear el label con el mensaje personalizado o un mensaje predeterminado si no se encuentra el mensaje personalizado
    if mensaje_personalizado:
        label_subcategorias = tk.Label(self.area_central, text=mensaje_personalizado, font=("Arial", 16, "bold"), bg="lightgrey", padx=10, pady=20)
        label_subcategorias.pack()
        # Agregar una línea horizontal debajo del botón
        separador = ttk.Separator(self.area_central, orient="horizontal")
        separador.pack(fill="x", pady=10, padx=40)
    else:
        label_subcategorias = tk.Label(self.area_central, text="SISTEMA OPERATIVO", font=("Arial", 12))
        label_subcategorias.pack()

    contenedor_botones = tk.Frame(self.area_central, bg="lightgrey")
    contenedor_botones.pack()

    boton_actualizar = tk.Button(contenedor_botones, text="Actualizar Sistema", command=lambda: actualizar_sistema(self.root))
    boton_actualizar.grid(row=0, column=0, padx=10, pady=10)
    ToolTip(boton_actualizar, "Instala todos las actualizaciones disponibles para la versión de tu sistema operativo")

    boton_limpiar_cache = tk.Button(contenedor_botones, text="Limpiar Caché", command=lambda: limpiar_cache(self.root))
    boton_limpiar_cache.grid(row=0, column=1, padx=10, pady=10)
    ToolTip(boton_limpiar_cache, "Limpia la caché del sistema operativo")

    boton_abrir_software = tk.Button(contenedor_botones, text="Abrir Gestor Software", command=abrir_gestor_software)
    boton_abrir_software.grid(row=0, column=2, padx=10, pady=10)
    ToolTip(boton_abrir_software, "Instala o desinstala paquetes snap desde el gestor de software de Ubuntu")
    
    

    def abrir_ventana_aplicaciones_autostart():
        if self.area_central.winfo_exists():
            ventana_aplicaciones_autostart = tk.Toplevel(self.area_central)
            aplicaciones_autostart = AplicacionesAutostart(ventana_aplicaciones_autostart)
        else:
            messagebox.showinfo("ERROR!!", "La ventana principal ha sido destruida")

    boton_app_inicio = tk.Button(contenedor_botones, text="Aplicaciones Inicio", command=abrir_ventana_aplicaciones_autostart)
    boton_app_inicio.grid(row=1, column=0, padx=10, pady=10)
    ToolTip(boton_app_inicio, "Añade o elimina aplicaciones que se ejecuten al arrancar el equipo. Permite archivos .desktop")
    
    boton_eliminar_archivo = tk.Button(contenedor_botones, text="Eliminar Archivo/s", command=Limpieza.eliminar_elemento)
    boton_eliminar_archivo.grid(row=1, column=1, padx=10, pady=10)
    ToolTip(boton_eliminar_archivo, "Eliminar permanentemente archivos o carpetas del equipo")
    
    boton_vaciar_papelera = tk.Button(contenedor_botones, text="Vaciar Papelera", command=Limpieza.vaciar_papelera)
    boton_vaciar_papelera.grid(row=1, column=2, padx=10, pady=10)
    ToolTip(boton_vaciar_papelera, "Vacía la papelera de reciclaje del equipo")
    
    def abrir_ventana_administrar_procesos():
        ventana_procesos = tk.Toplevel(self.area_central)
        administrar_procesos = AdministrarProcesos(ventana_procesos)
    
    # Botón para abrir la ventana Administrar Procesos
    boton_administrar_procesos = tk.Button(contenedor_botones, text="Administrar Procesos", command=abrir_ventana_administrar_procesos)
    boton_administrar_procesos.grid(row=2, column=0, padx=10, pady=10)
    ToolTip(boton_administrar_procesos, "Abre una ventana para administrar los procesos del sistema")

    def abrir_ventana_archivos_duplicados():
        ventana_archivos_duplicados = tk.Toplevel(self.area_central)
        buscar_archivos_duplicados = AplicacionBuscadorDuplicados(ventana_archivos_duplicados)
    
    # Botón para abrir la ventana en la que buscar archivos duplicados del sistema
    boton_archivos_duplicados = tk.Button(contenedor_botones, text="Buscar Archivos Duplicados", command=abrir_ventana_archivos_duplicados)
    boton_archivos_duplicados.grid(row=2, column=1, padx=10, pady=10)
    ToolTip(boton_archivos_duplicados, "Abre una ventana buscar archivos duplicados en el sistema")
    
    def abrir_ventana_gestion_repositorios():
        ventana_gestion_repositorios = tk.Toplevel(self.area_central)
        buscar_archivos_duplicados = Repositorios(ventana_gestion_repositorios)
    
    # Botón para abrir la ventana para la gestión de repositorios
    boton_gestion_repositorios = tk.Button(contenedor_botones, text="Gestiona Repositorios", command=abrir_ventana_gestion_repositorios)
    boton_gestion_repositorios.grid(row=2, column=2, padx=10, pady=10)
    ToolTip(boton_gestion_repositorios, "Gestiona los repositorios del sistema")
    

    # Llamada a la función
    def abrir_ventana_monitorizar_sistema():
        ventana_monitorizar = tk.Toplevel(self.area_central)
        monitorizacion = MonitorizarSistema(ventana_monitorizar)
        monitorizacion.monitorizar_sistema()

    boton_monitorizar = tk.Button(contenedor_botones, text="Monitorizar", command=abrir_ventana_monitorizar_sistema)
    boton_monitorizar.grid(row=3, column=0, padx=10, pady=10)


    
# Función para mostrar la categoría INTERNET
def internet_cat(self, mensaje_personalizado, entry_url=None):
    self.contenedor_texto.pack_forget()
    # Ocultar la etiqueta en la que se muestra la información del sistema
    for widget in self.area_central.winfo_children():
        widget.destroy()
    
    # Crear el label con el mensaje personalizado o un mensaje predeterminado si no se encuentra el mensaje personalizado
    if mensaje_personalizado:
        label_subcategorias = tk.Label(self.area_central, text=mensaje_personalizado, font=("Arial", 16, "bold"), bg="lightgrey", padx=10, pady=20)
        label_subcategorias.pack()
        # Agregar una línea horizontal debajo del botón
        separador = ttk.Separator(self.area_central, orient="horizontal")
        separador.pack(fill="x", pady=10, padx=40)
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
    
    # Agregar una línea horizontal debajo del botón
    separador = ttk.Separator(self.area_central, orient="horizontal")
    separador.pack(fill="x", pady=10, padx=40)
    
    # Caja de texto para escribir la URL web
    label_url = tk.Label(self.area_central, text="Escribe una URL a la que hacer ping:", font=("Arial", 12, "bold"))
    label_url.pack()
    entry_url = tk.Entry(self.area_central, width=50)
    entry_url.pack(pady=5)
    # Botón para hacer ping a la URL ingresada
    boton_ping = tk.Button(self.area_central, text="Hacer Ping", command=lambda: hacer_ping(entry_url))
    boton_ping.pack(pady=10)
    ToolTip(boton_ping, "Hacer ping a una URL")
    # Agregar una línea horizontal debajo del botón
    separador = ttk.Separator(self.area_central, orient="horizontal")
    separador.pack(fill="x", pady=10, padx=40)

# Función para mostrar la pantalla de la categoría RED LOCAL
def red_local_cat(self, mensaje_personalizado):

    # Limpiar el área central
    self.contenedor_texto.pack_forget()
    for widget in self.area_central.winfo_children():
        widget.destroy()

    # Crear el label con el mensaje personalizado o un mensaje predeterminado
    if mensaje_personalizado:
        label_subcategorias = tk.Label(self.area_central, text=mensaje_personalizado, font=("Arial", 16, "bold"), bg="lightgrey", padx=10, pady=20)
        label_subcategorias.pack()
        # Agregar una línea horizontal debajo del botón
        separador = ttk.Separator(self.area_central, orient="horizontal")
        separador.pack(fill="x", pady=10, padx=40)
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
    # Limpiar el área central
    self.contenedor_texto.pack_forget()
    for widget in self.area_central.winfo_children():
        widget.destroy()
    
    # Crear el label con el mensaje personalizado o un mensaje predeterminado
    if mensaje_personalizado:
        label_subcategorias = tk.Label(self.area_central, text=mensaje_personalizado, font=("Arial", 16, "bold"), bg="lightgrey", padx=10, pady=20)
        label_subcategorias.pack()
        # Agregar una línea horizontal debajo del botón
        separador = ttk.Separator(self.area_central, orient="horizontal")
        separador.pack(fill="x", pady=10, padx=40)
    else:
        label_subcategorias = tk.Label(self.area_central, text="NAVEGADORES", font=("Arial", 12))
        label_subcategorias.pack()
        # Agregar una línea horizontal debajo del botón
        separador = ttk.Separator(self.area_central, orient="horizontal")
        separador.pack(fill="x", pady=10, padx=40)
        
    # Crear un contenedor Frame para los botones
    frame_botones = tk.Frame(self.area_central)
    frame_botones.pack()

    
    # Botón para limpiar la caché de Chrome
    boton_chrome = tk.Button(frame_botones, text="Limpiar Caché Chrome", command=lambda: LimpiadorNavegadores.limpiar_cache_chrome(self, boton_chrome, lambda mensaje: messagebox.showinfo("Resultado", mensaje)))
    boton_chrome.pack(side="left", padx=5)
    ToolTip(boton_chrome, "Limpia la caché de Chrome (si está instalado)")


    # Botón para limpiar la caché de Firefox
    boton_firefox = tk.Button(frame_botones, text="Limpiar Caché Firefox", command=lambda: LimpiadorNavegadores.limpiar_cache_firefox(self, boton_firefox, lambda mensaje: messagebox.showinfo("Resultado", mensaje)))
    boton_firefox.pack(side="left", padx=5)
    ToolTip(boton_firefox, "Limpia la caché de Firefox (si está instalado)")

    # Botón para limpiar la caché de Edge
    boton_edge = tk.Button(frame_botones, text="Limpiar Caché Edge", command=lambda: LimpiadorNavegadores.limpiar_cache_edge(self, boton_edge, lambda mensaje: messagebox.showinfo("Resultado", mensaje)))
    boton_edge.pack(side="left", padx=5)
    ToolTip(boton_edge, "Limpia la caché de Edge (si está instalado)")

    # Agregar una línea horizontal debajo del botón
    separador = ttk.Separator(self.area_central, orient="horizontal")
    separador.pack(fill="x", pady=10, padx=40) 
    


    