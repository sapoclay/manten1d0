try:
    import subprocess
    import threading
    import time
    import tkinter as tk
    import webbrowser
    from tkinter import messagebox, ttk
    import requests
    from about import mostrar_about
    from cat_informacion import Informacion
    from password import limpiar_archivos_configuracion, obtener_contrasena
    from dependencias import instalar_dependencias, verificar_dependencias
    from menuCategorias import archivos_cat, diccionario_cat, informacion_cat, internet_cat, navegadores_cat, perfil_cat, red_local_cat, sistema_cat, notas_cat
    import preferencias  # Importar el módulo de preferencias para manejar el cambio de tema
except ImportError:
    # Instalar python3-tk automáticamente sin mostrar mensaje al usuario
    proceso_instalacion = subprocess.Popen(
        ["sudo", "apt", "install", "-y", "python3-tk", "python3-pip"],
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    proceso_instalacion.communicate(input="\n")

    # Verificar si ocurrieron errores durante la instalación
    if proceso_instalacion.returncode == 0:
        # Intentar importar las bibliotecas de tkinter nuevamente
        import subprocess
        import threading
        import time
        import tkinter as tk
        import webbrowser
        from tkinter import messagebox, ttk
        import requests
        from about import mostrar_about
        from cat_informacion import Informacion
        from dependencias import instalar_dependencias, verificar_dependencias
        from menuCategorias import archivos_cat, diccionario_cat, informacion_cat, internet_cat, navegadores_cat, perfil_cat, red_local_cat, sistema_cat, notas_cat
        from password import limpiar_archivos_configuracion, obtener_contrasena
        import preferencias  # Importar el módulo de preferencias para manejar el cambio de tema
    else:
        # Salir del programa con código de error 1 si la instalación falla
        exit(1)


def instalar_dependencias_con_progreso():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    progress_window = tk.Toplevel(root)
    progress_window.title("Instalando dependencias")
    progress_window.geometry("300x100")
    progress_window.resizable(False, False)

    progress_label = tk.Label(progress_window, text="Instalando dependencias...")
    progress_label.pack(pady=5)

    progress_bar = ttk.Progressbar(progress_window, length=200, mode="determinate")
    progress_bar.pack(pady=5)
    progress_bar["value"] = 0
    progress_bar["maximum"] = 100

    def update_progress_bar(value):
        progress_bar["value"] = value
        if value < 100:
            root.after(50, update_progress_bar, value + 1)
        else:
            progress_window.destroy()  # Cerrar la ventana de progreso

    threading.Thread(target=instalar_dependencias, args=(progress_bar,)).start()
    update_progress_bar(0)
    root.mainloop()

def main():
    obtener_contrasena()

    root = tk.Tk()
    root.title("Comprobando Dependencias")
    root.resizable(False, False)

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="indeterminate")
    progress_bar.pack(pady=20)
    progress_bar.start()

    label = tk.Label(root, text="Comprobando dependencias...")
    label.pack()

    def update_progress():
        progress_bar["value"] = 0
        for i in range(101):
            time.sleep(0.05)
            progress_bar["value"] = i
            root.update_idletasks()

        root.after(1000, lambda: verificar_dependencias_con_progreso(root, progress_bar, label))

    threading.Thread(target=update_progress).start()
    root.mainloop()

def verificar_dependencias_con_progreso(root, progress_bar, label):
    # Comprobar dependencias
    if not verificar_dependencias():
        # Si hay dependencias faltantes, mostrar ventana emergente para instalarlas
        if messagebox.askyesno(
            "Instalación de dependencias",
            "Las dependencias son imprescindibles ¿Quieres instalarlas ahora?",
        ):
            instalar_dependencias_con_progreso()
            # Verificar dependencias nuevamente después de la instalación
            verificar_dependencias_con_progreso(root, progress_bar, label)
        else:
            # Si el usuario elige no instalar las dependencias, mostrar un mensaje y salir del programa
            messagebox.showinfo(
                "Información", "El programa no puede iniciar sin todas las dependencias instaladas."
            )
            root.destroy()  # Cerrar la ventana de progreso
            exit()
    else:
        # Detener y cerrar la barra de progreso y el mensaje
        close_progress(root, progress_bar, label)

def close_progress(root, progress_bar, label):
    progress_bar.stop()
    progress_bar.destroy()
    label.destroy()

    # Mostrar mensaje de dependencias instaladas
    messagebox.showinfo(
        "Información",
        "¡Todas las dependencias están instaladas! Haz clic en OK para iniciar el programa...",
    )
    # Cerrar la ventana de progreso
    root.destroy()
    # Crear la ventana principal
    main_window = tk.Tk()
    VentanaPrincipal(main_window)
    main_window.mainloop()

##############################################################VENTANA PRINCIPAL##############################################################

class VentanaPrincipal:
    def __init__(self, root):
        from tooltip import ToolTip

        self.root = root
        self.root.title("Manten1-d0")
        self.root.geometry("800x700")  # Tamaño fijo de la ventana
        self.root.resizable(False, False)  # Hacer que la ventana no sea redimensionable
        self.root.protocol(
            "WM_DELETE_WINDOW", self.cerrar_ventana_principal
        )  # Asociar la función al evento de cierre de ventana

        # Cambiar el color de fondo de la ventana
        self.root.config(bg="lightgrey")
        
##############################################################FUNCIONES PARA MENÚ SUPERIOR##########################################################

        # Función para abrir la ventana de Opciones/Personalización
        def abrir_ventana_personalizacion():
            preferencias.abrir_ventana_configuracion(root)
            # Aplicar el tema seleccionado a la nueva ventana
            preferencias.cambiar_tema(self.area_central, preferencias.tema_seleccionado)

        # Función para abrir la ventana de actualizaciones
        def abrir_ventana_actualizaciones():
            # Importar el módulo actualizaciones.py
            import actualizaciones
            # Llamar a la función para mostrar la ventana de actualizaciones
            actualizaciones.mostrar_ventana_actualizaciones()
            # Aplicar el tema seleccionado a la nueva ventana
            preferencias.cambiar_tema(self.area_central, preferencias.tema_seleccionado)

        def abrir_url():

            url = tk.simpledialog.askstring("Abrir URL", "Ingrese la URL que desea abrir:")
            if url:
                webbrowser.open_new(url)

        def abrir_url_github():

            webbrowser.open("https://github.com/sapoclay/manten1d0")
            
        def abrir_terminal():
            try:
                # Comando para abrir la terminal predeterminada en Ubuntu
                subprocess.Popen(["gnome-terminal"])
            except Exception as e:
                # Manejar cualquier excepción que pueda ocurrir al intentar abrir la terminal
                print(f"No se pudo abrir la terminal: {e}")

#################################################### MENÚ SUPERIOR ##############################################################
        def menu():
            # Crear el menú superior
            self.menu_superior = tk.Menu(self.root)
            self.menu_archivo = tk.Menu(self.menu_superior, tearoff=0)
            self.menu_archivo.add_command(label="Abrir Terminal (Ctrl+Alt+T)", command=abrir_terminal)
            self.menu_archivo.add_separator()
            self.menu_archivo.add_command(label="Abrir URL en Navegador", command=abrir_url)
            self.menu_archivo.add_separator()
            self.menu_archivo.add_command(label="Salir", command=self.cerrar_ventana_principal)
            self.menu_superior.add_cascade(label="Archivo", menu=self.menu_archivo)
            # Crear el menú Preferencias
            preferencias_menu = tk.Menu(self.root, tearoff=0)
            preferencias_menu.add_command(label="Repositorio GitHub", command=abrir_url_github)
            preferencias_menu.add_separator()
            preferencias_menu.add_command(
                label="Buscar Actualizaciones", command=abrir_ventana_actualizaciones
            )
            preferencias_menu.add_separator()
            preferencias_menu.add_command(label="Opciones", command=abrir_ventana_personalizacion)
            # Agregar el menú Preferencias como una cascada en el menú principal
            self.menu_superior.add_cascade(label="Preferencias", menu=preferencias_menu)
            # Crear el menú About
            self.menu_superior.add_command(
                label="About", command=mostrar_about
            )  # Llama a mostrar_about cuando se haga clic
            self.root.config(menu=self.menu_superior)

        # Llamamos al menú superior creado con la función menú
        menu()
        
##################################################################################################################################
##############################################MENÚ LATERAL########################################################################
        def menu_lateral():
            # Crear el menú lateral con categorías
            self.menu_lateral = tk.Frame(self.root, width=200, bg="lightgrey")
            self.menu_lateral.pack(side="left", fill="y")

            # Categorías para el menú lateral
            self.categorias = [
                "Perfil Usuario",
                "Información",
                "Sistema",
                "Archivos",
                "Internet",
                "Red Local",
                "Navegadores",
                "Diccionario",
                "Notas",
            ]
            self.botones_categorias = []
            for categoria in self.categorias:
                boton = tk.Button(
                    self.menu_lateral,
                    text=categoria,
                    width=20,
                    command=lambda c=categoria: self.mostrar_subcategorias(c),
                )
                boton.pack(pady=5)
                ToolTip(boton, f"Categoría {categoria}")
                self.botones_categorias.append(boton)
            # Dibujar una línea horizontal
            self.canvas = tk.Canvas(self.menu_lateral, width=50, height=2, bg="lightgrey", highlightthickness=0)
            self.canvas.create_line(0, 1, 50, 1, fill="black")
            self.canvas.pack(pady=10)        
            # Crear indicador de conexión a Internet
            self.indicador_internet = tk.Label(
                self.menu_lateral,
                text="Estado de la conexión",
                bg="red",
                fg="white",
                width=20,
                height=1,
            )
            
            self.indicador_internet.pack(pady=20)
            ToolTip(self.indicador_internet, "Estado de la conexión a internet del equipo")
            # Iniciar la verificación de conexión a Internet
            self.check_connection()

        menu_lateral()
############################################################################################################################################        
        
        # Crear el área central para mostrar subcategorías
        self.area_central = tk.Frame(self.root, bg="lightgrey", borderwidth=0)  # Eliminar el borde
        self.area_central.pack(side="top", fill="both", expand=True)  # Ajustar el área central

        # Mensaje de bienvenida
        self.label_bienvenida = tk.Label(
            self.area_central,
            text="¡Bienvenid@!\n Comienza haciendo clic\n en una categoría del menú lateral.",
            font=("Arial", 18, "bold"),
            bg="lightgrey",
        )
        self.label_bienvenida.pack(pady=50)

        # Contenedor para el label de subcategorías
        self.frame_subcategorias = tk.Frame(
            self.area_central, bg="lightgrey", padx=10, pady=10
        )  # Ajustar el espaciado interno
        self.frame_subcategorias.pack(
            anchor="n", pady=(0, 20)
        )  # Espaciado en la parte superior y anclar al norte

        self.label_subcategorias = tk.Label(
            self.area_central, text="", font=("Arial", 12), bg="lightgrey", padx=10, pady=0
        )
        self.label_subcategorias.pack()

        # Crear el contenedor para el widget Text y la barra de desplazamiento para mostrar la categoría Información
        self.contenedor_texto = tk.Frame(self.root)
        # Contenedor Deshabilitado al inicio
        self.contenedor_texto.pack_forget()

        # Crear el widget Text para mostrar la información del sistema (inicialmente deshabilitado)
        self.texto_informacion = tk.Text(
            self.contenedor_texto, wrap=tk.WORD, font=("Arial", 12), state=tk.DISABLED
        )
        self.texto_informacion.pack(expand=True, fill="both", side="left")
        self.texto_informacion.pack_forget()  # Ocultar el widget Text

        # Agregar barra de desplazamiento vertical
        self.scrollbar_vertical = ttk.Scrollbar(
            self.contenedor_texto, orient="vertical", command=self.texto_informacion.yview
        )
        self.scrollbar_vertical.pack(side="right", fill="y")
        self.texto_informacion.config(yscrollcommand=self.scrollbar_vertical.set)

        # Mensajes personalizados para cada categoría
        self.mensajes_personalizados = {
            "Información": "Información sobre el Sistema Operativo",
            "Perfil Usuario": "Modifica los datos de tu perfil de usuario en el sistema",
            "Sistema": "Configuraciones y detalles del Sistema Operativo.",
            "Archivos": "Opciones sobre archivos del Sistema Operativo",
            "Internet": "Configuraciones y detalles sobre la conexión a Internet.",
            "Red Local": "Configuraciones y acciones sobre la red local.",
            "Navegadores": "Acciones con los navegadores web.",
            "Diccionario": "Diccionario sobre comandos Gnu/Linux",
            "Notas": "Escribe tus apuntes y notas rápidas",
        }

        # Llenar el área de texto con la información inicial
        self.mostrar_informacion_sistema()  # Llama a la función para mostrar la información del sistema

    # Función para mostrar u ocultar elementos en el área principal según la categoría seleccionada. También se hacen las llamadas a funciones
    def mostrar_subcategorias(self, categoria):
        mensaje_personalizado = self.mensajes_personalizados.get(categoria, None)

        if categoria == "Información":

            informacion_cat(self, mensaje_personalizado)

        elif categoria == "Diccionario":

            diccionario_cat(self, mensaje_personalizado)
            
        elif categoria == "Notas":

            notas_cat(self, mensaje_personalizado)

        elif categoria == "Perfil Usuario":

            perfil_cat(self, mensaje_personalizado)

        elif categoria == "Sistema":

            sistema_cat(self, mensaje_personalizado)
            if preferencias.tema_seleccionado == "Claro":
                return
            preferencias.cambiar_tema(self.area_central, preferencias.tema_seleccionado)

        elif categoria == "Archivos":

            archivos_cat(self, mensaje_personalizado)
            # Aplicar el tema seleccionado a la nueva ventana
            preferencias.cambiar_tema(self.area_central, preferencias.tema_seleccionado)

        elif categoria == "Internet":

            internet_cat(self, mensaje_personalizado)
            # Aplicar el tema seleccionado a la nueva ventana
            preferencias.cambiar_tema(self.area_central, preferencias.tema_seleccionado)

        elif categoria == "Red Local":

            red_local_cat(self, mensaje_personalizado)
            # Aplicar el tema seleccionado a la nueva ventana
            preferencias.cambiar_tema(self.area_central, preferencias.tema_seleccionado)

        elif categoria == "Navegadores":

            navegadores_cat(self, mensaje_personalizado)
            # Aplicar el tema seleccionado a la nueva ventana
            preferencias.cambiar_tema(self.area_central, preferencias.tema_seleccionado)

        else:
            self.contenedor_texto.pack_forget()  # Deshabilitar contenedor categoría Información
            self.texto_informacion.pack_forget()  # Ocultar el widget Text
            self.texto_informacion.delete('1.0', tk.END)  # Borrar el contenido del widget Text
            self.label_bienvenida.pack_forget()  # Ocultar el mensaje de bienvenida
            if mensaje_personalizado:
                self.label_subcategorias.config(
                    text=mensaje_personalizado, font=("Arial", 14, "bold")
                )  # Ajustar el texto al mensaje personalizado
            else:
                self.label_subcategorias.config(
                    text=f"Subcategorías de {categoria}", font=("Arial", 12)
                )  # Restaurar el texto original
            self.label_subcategorias.pack()  # Mostrar la etiqueta de subcategorías
            # Aplicar el tema seleccionado a la nueva ventana
            preferencias.cambiar_tema(self.area_central, preferencias.tema_seleccionado)

    # Función para mostrar la información del sistema dentro de la categoría información. Toma los datos de información.py
    def mostrar_informacion_sistema(self):
        def obtener_temperatura_cpu():
            try:
                with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
                    temperatura_miligrados = int(file.read().strip())
                    return temperatura_miligrados / 1000.0
            except FileNotFoundError:
                return None

        # Obtener la información del sistema utilizando la clase Informacion
        info_completa = Informacion.obtener_informacion_completa()
        usuario = info_completa["Usuario"]
        sistema_operativo = info_completa["Sistema Operativo"]
        version_sistema = info_completa["Versión de Sistema"]
        version_ubuntu = info_completa["Versión de Ubuntu"]
        tipo_escritorio = info_completa["Tipo de Escritorio"]
        tiempo_actividad = info_completa["Tiempo de Actividad"]
        tarjeta_grafica = info_completa["Información de la Tarjeta Gráfica"]
        interfaces_red = ", ".join(
            info_completa["Interfaces de Red"]
        )  # Convertir la lista a cadena separada por comas
        ip_local = info_completa["Dirección IP Local"]
        ip_publica = info_completa["Dirección IP Pública"]
        dns_local = info_completa["dns local"]
        dns_publico = info_completa["dns publico"]
        zona_horaria = info_completa["Zona Horaria"]
        procesador = Informacion.obtener_informacion_procesador()
        memoria = Informacion.obtener_informacion_memoria()

        # Obtener la temperatura del procesador
        temperatura_cpu = obtener_temperatura_cpu()

        # Crear el texto con la información del sistema
        texto_info = [
            ("Usuario:", usuario),
            ("Sistema Operativo:", sistema_operativo),
            ("Versión del Sistema:", version_sistema),
            ("Versión de Ubuntu:", version_ubuntu),
            ("Tipo Escritorio:", tipo_escritorio),
            ("Tiempo de actividad:", tiempo_actividad),
            ("-" * 110, ""),
            ("Interfaces de Red:", interfaces_red),
            ("IP Local:", ip_local),
            ("IP Pública:", ip_publica),
            ("DNS Local:", dns_local),
            ("DNS Público:", dns_publico),
            ("Zona Horaria:", zona_horaria),
            (
                "Temperatura CPU:",
                f"{temperatura_cpu} °C" if temperatura_cpu is not None else "No disponible",
            ),
            ("-" * 110, ""),
        ]

        # Insertar el texto en el widget Text
        self.texto_informacion.config(state=tk.NORMAL)  # Habilitar la edición
        self.texto_informacion.delete(
            '1.0', tk.END
        )  # Borrar todo el contenido existente en el widget Text

        for label, value in texto_info:
            self.texto_informacion.insert(
                tk.END, f"{label} ", "bold"
            )  # Insertar texto estático con negrita
            self.texto_informacion.insert(tk.END, f"{value}\n")  # Insertar valor de la variable
            self.texto_informacion.tag_configure(
                "bold", font=("Arial", 12, "bold")
            )  # Aplicar estilo de texto negrita al texto estático

        self.texto_informacion.insert(
            tk.END, "\nInformación de la tarjeta gráfica:\n", "bold"
        )  # Texto "Información de la tarjeta gráfica" en negrita
        for key, value in tarjeta_grafica.items():
            self.texto_informacion.insert(tk.END, f"{key}: {value}\n")

        self.texto_informacion.insert(tk.END, "-" * 110 + "\n")  # Línea horizontal

        self.texto_informacion.insert(
            tk.END, "\nInformación del Procesador:\n", "bold"
        )  # Texto "Información del Procesador" en negrita
        for item in procesador:
            self.texto_informacion.insert(tk.END, f"{item[0]}: {item[1]}\n")

        self.texto_informacion.insert(tk.END, "-" * 110 + "\n")  # Línea horizontal

        self.texto_informacion.insert(
            tk.END, "\nInformación de la Memoria:\n", "bold"
        )  # Texto "Información de la Memoria" en negrita
        for key, value in memoria.items():
            self.texto_informacion.insert(tk.END, f"{key}: {value}\n")

        self.texto_informacion.config(state=tk.DISABLED)  # Deshabilitar la edición

    def cerrar_ventana_principal(self):
        # Llamar a la función para limpiar los archivos de configuración
        limpiar_archivos_configuracion()
        # Cerrar la ventana principal
        self.root.destroy()

    # Función para verificar si la conexión a internet está establecida o no
    def check_connection(self):
        self.internet_status_thread = threading.Thread(target=self.update_internet_status, daemon=True)
        self.internet_status_thread.start()
        
    def update_internet_status(self):
        while True:
            try:
                requests.get("https://www.google.com", timeout=3)
                self.indicador_internet.config(bg="green", text="Conexión establecida")
            except requests.RequestException:
                self.indicador_internet.config(bg="red", text="Sin conexión")
            time.sleep(10)

if __name__ == "__main__":
    main()