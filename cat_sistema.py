import subprocess
from password import obtener_contrasena
import threading
import time
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import os
from tkinter import filedialog
import psutil
from tkinter import font
import tkinter.messagebox as messagebox
import hashlib
from datetime import datetime, timezone
import platform
from tooltip import ToolTip    
import subprocess
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Clase para generar la ventana de barra de progreso
class ProgresoVentana(tk.Toplevel):
    """
Clase 'ProgresoVentana'.

Class:
    - ProgresoVentana(tk.Toplevel): Clase para generar la ventana de barra de progreso.

Attributes:
    - master: El widget principal al que pertenece la ventana.
    - accion: La acción que se está realizando y se muestra en la ventana.

Methods:
    - __init__(self, master, accion): Constructor de la clase. Inicializa la ventana de progreso con una barra de progreso indeterminada y un mensaje indicando la acción en curso.
        - master: El widget principal al que pertenece la ventana.
        - accion: La acción que se está realizando y se muestra en la ventana.

Raises:
    - No hay excepciones especificadas en la clase.
"""
    def __init__(self, master, accion):
        super().__init__(master)
        self.title("Progreso")
        self.geometry("300x100")
        self.progressbar = ttk.Progressbar(self, orient="horizontal", mode="indeterminate")
        self.progressbar.pack(pady=20)
        self.label = tk.Label(self, text=f"Ejecutando {accion}...", font=("Arial", 12))
        self.label.pack()
        self.progressbar.start()
        self.grab_set()
        self.resizable(False, False)  # Hacer que la ventana no sea redimensionable

'''
Función para ejecutar cualquier comando que necesite sudo y la contraseña
'''
def ejecutar_comando_con_sudo(comando, accion, master, callback=None):
    contrasena = obtener_contrasena()
    ventana_progreso = ProgresoVentana(master, accion)

    proceso = subprocess.Popen(f"echo {contrasena} | sudo -S {comando}", shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while proceso.poll() is None:
        output = proceso.stdout.readline().strip()
        if output:
            ventana_progreso.label.config(text=output)
        ventana_progreso.update_idletasks()
        time.sleep(0.1)  # Espera corta para no sobrecargar el procesador
    
    ventana_progreso.destroy()
    if callback:
        callback()

def actualizar_sistema(master):
    comando = "apt-get update && apt-get upgrade -y"
    threading.Thread(target=ejecutar_comando_con_sudo, args=(comando, "Actualización del sistema", master, lambda: messagebox.showinfo("Información", "Actualización completada"))).start()

def limpiar_cache(master):
    comando = "apt-get clean && apt-get autoremove -y"
    threading.Thread(target=ejecutar_comando_con_sudo, args=(comando, "Limpieza de caché", master, lambda: messagebox.showinfo("Información", "Limpieza de caché completada"))).start()

def abrir_gestor_software():
        try:
            # Verificar si Snap Store está instalado
            snap_store_instalado = subprocess.run(["which", "snap-store"], stdout=subprocess.PIPE).returncode == 0

            # Si Snap Store no está instalado, mostrar un mensaje de advertencia en una ventana emergente
            if not snap_store_instalado:
                messagebox.showwarning("Snap Store no está instalado", "Snap Store no está instalado en el sistema.")
                return

            # Abrir Snap Store
            subprocess.Popen("snap-store", shell=True)
        except Exception as e:
            # Mostrar el mensaje de error en una ventana emergente
            messagebox.showerror("Error al abrir Snap Store", f"Error: {e}")

""" 
Clase para realizar tareas de limpieza:
    - Vaciar la papelera
    - Eliminar archivos y carpetas sin pasar por la papelera
"""

class Limpieza:
    @staticmethod
    def vaciar_papelera():
        try:
            confirmacion = messagebox.askyesno("Confirmar vaciado", "¿Estás seguro de que quieres vaciar la papelera de reciclaje?")
            if confirmacion:
                os.system("gio trash --empty")
                messagebox.showinfo("Éxito", "La papelera de reciclaje se ha vaciado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo vaciar la papelera de reciclaje. Error: {e}")

    @staticmethod
    def eliminar_elemento():
        try:
            elemento = filedialog.askdirectory(title="Seleccionar elemento para eliminar")
            
            if elemento:
                confirmacion = messagebox.askyesno("Confirmar eliminación", f"¿Estás seguro de que quieres eliminar el elemento seleccionado:\n{elemento}?")
                if confirmacion:
                    if os.path.isfile(elemento):
                        os.remove(elemento)
                    elif os.path.isdir(elemento):
                        os.rmdir(elemento)
                    messagebox.showinfo("Éxito", "El elemento seleccionado se ha eliminado correctamente.")
            else:
                messagebox.showwarning("Advertencia", "No se seleccionó ningún elemento para eliminar.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el elemento seleccionado. Error: {e}")


# Clase para crear la ventana y gestionar la aplicaciones al Inicio
class AplicacionesAutostart:
    
    """
Clase 'AplicacionesAutostart'.

Class:
    - AplicacionesAutostart: Clase para crear la ventana y gestionar las aplicaciones al Inicio.

Attributes:
    - master: El widget principal al que pertenece la ventana.

Methods:
    - __init__(self, master): Constructor de la clase. Inicializa la ventana y sus componentes.
        - master: El widget principal al que pertenece la ventana.
    - actualizar_lista_aplicaciones(self): Actualiza la lista de aplicaciones de autostart en el Treeview.
    - obtener_aplicaciones_autostart(self): Obtiene la lista de aplicaciones de autostart.
    - agregar_aplicacion(self): Permite al usuario seleccionar y agregar una aplicación al autostart.
    - eliminar_aplicacion(self): Elimina una aplicación seleccionada del autostart.
    - abrir_ventana_aplicaciones_autostart(self): Abre una nueva ventana para la configuración de aplicaciones de autostart.

Raises:
    - No hay excepciones especificadas en la clase.
"""

    def __init__(self, master):
        self.master = master
        self.master.title("Configuración de Aplicaciones de Autostart")

        # Crear un Treeview para mostrar las aplicaciones de autostart
        self.treeview = ttk.Treeview(master, columns=("Aplicación"))
        self.treeview.heading("#0", text="ID")
        self.treeview.heading("#1", text="Aplicación")
        self.treeview.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Obtener la lista de aplicaciones de autostart
        self.actualizar_lista_aplicaciones()

        # Botones para agregar y eliminar aplicaciones
        self.btn_agregar = tk.Button(master, text="Agregar", command=self.agregar_aplicacion)
        self.btn_agregar.grid(row=1, column=0, padx=5, pady=5)

        self.btn_eliminar = tk.Button(master, text="Eliminar", command=self.eliminar_aplicacion)
        self.btn_eliminar.grid(row=1, column=1, padx=5, pady=5)

    def actualizar_lista_aplicaciones(self):
        # Limpiar el Treeview antes de actualizar
        for i in self.treeview.get_children():
            self.treeview.delete(i)

        # Obtener la lista de aplicaciones de autostart
        aplicaciones_autostart = self.obtener_aplicaciones_autostart()

        # Agregar las aplicaciones al Treeview
        for i, app in enumerate(aplicaciones_autostart, start=1):
            self.treeview.insert("", "end", text=str(i), values=(app,))

    def obtener_aplicaciones_autostart(self):
        aplicaciones_autostart = []

        # Leer el contenido del directorio autostart
        autostart_dir = os.path.expanduser("~/.config/autostart/")
        if os.path.exists(autostart_dir):
            for filename in os.listdir(autostart_dir):
                if filename.endswith(".desktop"):
                    aplicaciones_autostart.append(filename[:-8])  # Eliminar la extensión .desktop

        return aplicaciones_autostart

    def agregar_aplicacion(self):
        # Permitir al usuario seleccionar un archivo .desktop para agregarlo al autostart
        archivo_desktop = tk.filedialog.askopenfilename(title="Seleccionar Aplicación",
                                                        filetypes=[("Archivos Desktop", "*.desktop")])
        if archivo_desktop:
            nombre_aplicacion = os.path.basename(archivo_desktop)
            destino = os.path.expanduser("~/.config/autostart/") + nombre_aplicacion
            os.system(f"cp {archivo_desktop} {destino}")
            self.actualizar_lista_aplicaciones()

    def eliminar_aplicacion(self):
        # Obtener el ID de la fila seleccionada en el Treeview
        seleccion = self.treeview.selection()
        if seleccion:
            id_fila = self.treeview.index(seleccion)
            aplicacion = self.treeview.item(seleccion)["values"][0]

            # Eliminar la aplicación del autostart
            ruta_aplicacion = os.path.expanduser(f"~/.config/autostart/{aplicacion}.desktop")
            os.remove(ruta_aplicacion)
            self.actualizar_lista_aplicaciones()

    def abrir_ventana_aplicaciones_autostart(self):
        # Crear una nueva ventana de tkinter
        ventana_aplicaciones_autostart = tk.Toplevel(self.master)
        # Instanciar la clase AplicacionesAutostart en la nueva ventana
        aplicaciones_autostart = AplicacionesAutostart(ventana_aplicaciones_autostart)


class AdministrarProcesos:
    
    """
Clase 'AdministrarProcesos'.

Class:
    - AdministrarProcesos: Clase para crear y gestionar la ventana de administración de procesos.

Attributes:
    - root: El widget principal al que pertenece la ventana.

Methods:
    - __init__(self, root): Constructor de la clase. Inicializa la ventana y sus componentes.
        - root: El widget principal al que pertenece la ventana.
    - on_entry_focus_in(self, event): Método para manejar el evento de enfoque en la entrada de búsqueda.
        - event: El evento que desencadena la función.
    - on_entry_focus_out(self, event): Método para manejar el evento de desenfoque en la entrada de búsqueda.
        - event: El evento que desencadena la función.
    - load_processes(self): Carga la lista de procesos en el Treeview.
    - close_process(self): Cierra el proceso seleccionado después de la confirmación del usuario.
    - filter_processes(self, event): Filtra los procesos en función de la entrada de búsqueda.
        - event: El evento que desencadena la función.
    - sort_column(self, column): Ordena los elementos en función de la columna seleccionada.
        - column: La columna seleccionada para ordenar.
    - update_cpu_usage_single(self, pid): Actualiza el uso de CPU para un proceso específico.
        - pid: El PID del proceso para el que se actualizará el uso de la CPU.
    - update_tree(self, pid, cpu_percent): Actualiza el Treeview con el uso de CPU actualizado para un proceso específico.
        - pid: El PID del proceso.
        - cpu_percent: El uso de CPU actualizado para el proceso.

Raises:
    - No hay excepciones especificadas en la clase.
"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Administrar Procesos")
        self.column_sort_order = {}  # Diccionario para guardar el orden de clasificación de las columnas
        
        self.tree = ttk.Treeview(self.root, columns=("PID", "Nombre", "Uso de CPU"))
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("#1", text="PID", anchor=tk.W, command=lambda: self.sort_column("#1"))
        self.tree.heading("#2", text="Nombre", anchor=tk.W, command=lambda: self.sort_column("#2"))
        self.tree.heading("#3", text="Uso de CPU", anchor=tk.W, command=lambda: self.sort_column("#3"))
        self.tree.column("#0", stretch=tk.NO, width=0)
        self.tree.column("#1", stretch=tk.YES, width=100)
        self.tree.column("#2", stretch=tk.YES, width=200)
        self.tree.column("#3", stretch=tk.YES, width=100)
        self.tree.pack(expand=True, fill=tk.BOTH)
        
        self.scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)  # Mover el árbol a la izquierda
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Colocar la barra de desplazamiento a la derecha

        # Crear una fuente en negrita
        bold_font = font.Font(weight="bold")

        # Crear la etiqueta con el texto "Opciones" en negrita
        label = tk.Label(self.root, text="Opciones", font=bold_font)
        label.pack(side=tk.TOP, pady=(0, 5))  # Ajustar el relleno superior según sea necesario

        
        self.search_entry_var = tk.StringVar()
        self.search_entry_var.set("Buscar por nombre o PID")
        self.search_entry = tk.Entry(self.root, textvariable=self.search_entry_var, fg="grey")
        self.search_entry.pack(side=tk.TOP, fill=tk.X)
        self.search_entry.bind("<FocusIn>", self.on_entry_focus_in)
        self.search_entry.bind("<FocusOut>", self.on_entry_focus_out)
        self.search_entry.bind("<KeyRelease>", self.filter_processes)
        
        self.close_button = tk.Button(self.root, text="Cerrar Proceso", command=self.close_process)
        self.close_button.pack(side=tk.TOP)
        
        self.load_processes()

    def on_entry_focus_in(self, event):
        if self.search_entry_var.get() == "Buscar por nombre o PID":
            self.search_entry_var.set("")
            self.search_entry.config(fg="black")

    def on_entry_focus_out(self, event):
        if not self.search_entry_var.get():
            self.search_entry_var.set("Buscar por nombre o PID")
            self.search_entry.config(fg="grey")
            
    def load_processes(self):
        self.tree.delete(*self.tree.get_children())
        for proc in psutil.process_iter(['pid', 'name']):
            proc_info = proc.info
            try:
                self.tree.insert("", "end", text="", values=(proc_info['pid'], proc_info['name'], "Calculando..."))
                threading.Thread(target=self.update_cpu_usage_single, args=(proc_info['pid'],)).start()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                self.tree.insert("", "end", text="", values=(proc_info['pid'], proc_info['name'], "N/A"))

    def close_process(self):
        selected_item = self.tree.selection()
        if selected_item:
            pid = self.tree.item(selected_item)["values"][0]
            name = self.tree.item(selected_item)["values"][1]
            confirm = messagebox.askyesno("Confirmar cierre", f"¿Estás seguro de que quieres cerrar el proceso {name} (PID: {pid})?")
            if confirm:
                try:
                    process = psutil.Process(pid)
                    process.terminate()
                except psutil.NoSuchProcess:
                    pass
                self.load_processes()
            
    def filter_processes(self, event):
        query = self.search_entry_var.get().lower()
        for item in self.tree.get_children():
            pid = str(self.tree.item(item)["values"][0])  # Convertir el PID a cadena
            name = self.tree.item(item)["values"][1].lower()
            if query in pid or query in name:
                self.tree.selection_set(item)
                self.tree.see(item)
            else:
                self.tree.selection_remove(item)
                
    def sort_column(self, column):
        column_index = int(column[1:]) - 1
        current_sort_order = self.column_sort_order.get(column, "asc")  # Obtener el orden actual de clasificación de la columna
        items = [(self.tree.set(child, column_index), child) for child in self.tree.get_children('')]

        if column_index == 0:  # Verificar si la columna es PID
            items.sort(key=lambda x: int(x[0]), reverse=current_sort_order == "desc")  # Convertir a entero antes de ordenar
        elif column_index == 1:  # Verificar si la columna es Nombre
            items.sort(key=lambda x: x[0].lower(), reverse=current_sort_order == "desc")
        elif column_index == 2:  # Verificar si la columna es Uso de CPU
            items.sort(key=lambda x: float(x[0].rstrip("%")) if x[0] != "N/A" else float('inf'), reverse=current_sort_order == "desc")  # Convertir a float antes de ordenar

        for index, (value, child) in enumerate(items):
            self.tree.move(child, '', index)

        self.column_sort_order[column] = "desc" if current_sort_order == "asc" else "asc"
    
    def update_cpu_usage_single(self, pid):
        try:
            process = psutil.Process(pid)
            cpu_percent = process.cpu_percent(interval=0.5)
            self.root.after(100, self.update_tree, pid, f"{cpu_percent:.2f}%")
            print(f"Actualizando uso de CPU para el proceso {pid} a: {cpu_percent:.2f}%")
        except psutil.NoSuchProcess:
            print(f"No se pudo calcular el uso de CPU para el proceso {pid}: process PID not found")
        except Exception as e:
            print(f"No se pudo calcular el uso de CPU para el proceso {pid}: {e}")

    def update_tree(self, pid, cpu_percent):
        for child in self.tree.get_children():
            if self.tree.item(child)["values"][0] == pid:
                self.tree.item(child, values=(pid, self.tree.item(child)["values"][1], cpu_percent))

# Categoría para buscar archivos duplicados en el sistema
class AplicacionBuscadorDuplicados:
    
    """
Clase 'AplicacionBuscadorDuplicados'.

Class:
    - AplicacionBuscadorDuplicados: Clase para buscar archivos duplicados en el sistema.

Attributes:
    - root: El widget principal al que pertenece la ventana.
    - carpeta_seleccionada: La carpeta seleccionada por el usuario para buscar archivos duplicados.
    - archivos_duplicados: Un diccionario que contiene los archivos duplicados encontrados.

Methods:
    - __init__(self, root): Constructor de la clase. Inicializa la ventana y sus componentes.
        - root: El widget principal al que pertenece la ventana.
    - abrir_ventana_carpeta(self): Abre una ventana para que el usuario seleccione una carpeta para buscar archivos duplicados.
    - mostrar_progreso(self): Muestra la barra de progreso y el mensaje de progreso.
    - buscar_archivos_duplicados(self, carpeta): Busca archivos duplicados en la carpeta especificada.
        - carpeta: La carpeta en la que se buscarán archivos duplicados.
    - mostrar_duplicados(self): Muestra los archivos duplicados encontrados en el Treeview.
    - calcular_hash(self, ruta_archivo): Calcula el hash SHA256 de un archivo dado.
        - ruta_archivo: La ruta completa del archivo.
    - obtener_fecha_creacion(self, archivo): Obtiene la fecha de creación de un archivo.
        - archivo: El archivo del que se obtendrá la fecha de creación.
    - seleccionar_todo(self): Selecciona o deselecciona todos los archivos en el Treeview.
    - confirmar_eliminar_seleccionados(self): Muestra un cuadro de diálogo de confirmación antes de eliminar los archivos seleccionados.
    - eliminar_seleccionados(self): Elimina los archivos seleccionados del sistema y del Treeview.
    - configurar_tamano_filas(self, event=None): Ajusta el ancho de las columnas del Treeview para que se adapten al tamaño de la ventana.
        - event: El evento que desencadena la función (por defecto es None).
    - abrir_ubicacion_archivo(self, event): Abre la ubicación del archivo seleccionado en el gestor de archivos por defecto.
        - event: El evento que desencadena la función.

Raises:
    - No se especifican excepciones en la clase.
"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Buscar Archivos Duplicados")
        self.root.geometry("800x600")  # Establecer un tamaño predeterminado para la ventana

        self.carpeta_seleccionada = None
        self.archivos_duplicados = {}

        # Marco para selección de carpeta
        self.marco_carpeta = tk.Frame(self.root)
        self.marco_carpeta.pack(pady=10)

        # Botón para buscar archivos
        self.boton_buscar = tk.Button(self.marco_carpeta, text="Buscar Archivos", command=self.abrir_ventana_carpeta)
        self.boton_buscar.pack(side="left")
        ToolTip(self.boton_buscar, "Selecciona una carpeta para buscar los archivos duplicados")

        # Marco para barra de progreso
        self.marco_progreso = tk.Frame(self.root)

        self.etiqueta_progreso = tk.Label(self.marco_progreso, text="Buscando archivos duplicados ...")
        self.barra_progreso = ttk.Progressbar(self.marco_progreso, orient="horizontal", length=300, mode="determinate")

        # Marco para mostrar archivos duplicados
        self.marco_duplicados = tk.Frame(self.root)
        self.marco_duplicados.pack(pady=10, fill="both", expand=True)

        self.treeview = ttk.Treeview(self.marco_duplicados, columns=("Nombre", "Ubicacion", "Hash", "Fecha"), show="headings", selectmode="extended")

        self.treeview.pack(side="left", fill="both", expand=True)
        self.treeview.heading("Nombre", text="Nombre del Archivo")
        self.treeview.heading("Ubicacion", text="Ubicacion")
        self.treeview.heading("Hash", text="Hash")
        self.treeview.heading("Fecha", text="Fecha de Creación")
        self.treeview.column("#0", width=0, stretch=tk.NO)  # Eliminar espacio para el checkbox

        # Configurar el scroll
        scroll_y = tk.Scrollbar(self.marco_duplicados, orient="vertical", command=self.treeview.yview)
        scroll_y.pack(side="right", fill="y")
        self.treeview.configure(yscrollcommand=scroll_y.set)

        # Checkbox para seleccionar todos los archivos
        self.var_seleccionar_todo = tk.IntVar()
        self.checkbox_seleccionar_todo = tk.Checkbutton(self.root, text="Seleccionar Todos", variable=self.var_seleccionar_todo, command=self.seleccionar_todo)
        self.checkbox_seleccionar_todo.pack(pady=5)
        ToolTip(self.checkbox_seleccionar_todo, "Seleccionar todos los archivos mostrados")


        # Botón para eliminar archivos seleccionados
        self.boton_eliminar = tk.Button(self.root, text="Eliminar Seleccionados", command=self.confirmar_eliminar_seleccionados)
        self.boton_eliminar.pack(pady=5)        
        ToolTip(self.boton_eliminar, "Elimina los archivos seleccionados")


        # Configurar el tamaño de las filas después de que la ventana se haya mostrado completamente
        self.root.update_idletasks()
        self.configurar_tamano_filas()

        # Configurar el evento <Configure> para ajustar el tamaño de las filas si la ventana se redimensiona
        self.root.bind("<Configure>", self.configurar_tamano_filas)

        # Enlazar el evento de doble clic en el treeview
        self.treeview.bind("<Double-1>", self.abrir_ubicacion_archivo)

    def abrir_ventana_carpeta(self):
        carpeta_seleccionada = filedialog.askdirectory()
        if carpeta_seleccionada:
            self.carpeta_seleccionada = os.path.abspath(carpeta_seleccionada)
            self.mostrar_progreso()  # Mostrar el mensaje de progreso y la barra
            self.barra_progreso.start()
            self.root.update()

            self.buscar_archivos_duplicados(self.carpeta_seleccionada)

            self.barra_progreso.stop()
            self.barra_progreso["value"] = 100  # Asegurar que la barra de progreso esté al 100%
            self.etiqueta_progreso.config(text="Búsqueda completada.")
            self.mostrar_duplicados()
        else:
            messagebox.showinfo("Información", "No se seleccionó ninguna carpeta.")

    def mostrar_progreso(self):
        self.marco_progreso.pack(pady=10)
        self.etiqueta_progreso.pack()
        self.barra_progreso.pack(padx=10, pady=10, fill="x")

    def buscar_archivos_duplicados(self, carpeta):
        total_archivos = sum(len(files) for _, _, files in os.walk(carpeta))
        progreso = 0
        for carpeta_raiz, _, archivos in os.walk(carpeta):
            for nombre_archivo in archivos:
                ruta_archivo = os.path.join(carpeta_raiz, nombre_archivo)
                hash_archivo = self.calcular_hash(ruta_archivo)
                if hash_archivo in self.archivos_duplicados:
                    self.archivos_duplicados[hash_archivo].append(ruta_archivo)
                else:
                    self.archivos_duplicados[hash_archivo] = [ruta_archivo]
                progreso += 1
                self.barra_progreso["value"] = (progreso / total_archivos) * 100
                self.root.update_idletasks()
        # Verificar si no se encontraron archivos duplicados
        if not self.archivos_duplicados:
            messagebox.showinfo("Información", "No se encontraron archivos duplicados en la carpeta seleccionada.")

    def mostrar_duplicados(self):
        # Eliminar las filas existentes en el treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # Insertar archivos duplicados en el treeview
        for hash_archivo, archivos in self.archivos_duplicados.items():
            if len(archivos) > 1:
                for archivo in archivos:
                    ubicacion = os.path.dirname(archivo)  # Obtener la ubicación del archivo
                    self.treeview.insert("", "end", values=(os.path.basename(archivo), ubicacion, hash_archivo, self.obtener_fecha_creacion(archivo)))

    def calcular_hash(self, ruta_archivo):
        try:
            sha256_hash = hashlib.sha256()
            with open(ruta_archivo, "rb") as f:
                for fragmento in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(fragmento)
            return sha256_hash.digest()
        except FileNotFoundError:
            messagebox.showinfo("Error", "El archivo no se encuentra en la ruta especificada:\n{}".format(ruta_archivo))
            return None

    def obtener_fecha_creacion(self, archivo):
        fecha_creacion = datetime.fromtimestamp(os.path.getctime(archivo), tz=timezone.utc)
        return fecha_creacion.strftime('%d-%m-%Y %H:%M:%S')

    def seleccionar_todo(self):
        if self.var_seleccionar_todo.get() == 1:
            self.treeview.selection_set(*self.treeview.get_children())
        else:
            self.treeview.selection_remove(self.treeview.get_children())

    def confirmar_eliminar_seleccionados(self):
        confirmacion = messagebox.askokcancel("Confirmar", "¿Está seguro de que desea eliminar el/los archivo/s seleccionado/s?")
        if confirmacion:
            self.eliminar_seleccionados()

    def eliminar_seleccionados(self):
        seleccionados = self.treeview.selection()
        
        # Verificar si no hay archivos seleccionados para eliminar
        if not seleccionados:
            messagebox.showinfo("Información", "No hay archivos seleccionados para eliminar.")
            return
        
        for seleccionado in seleccionados:
            archivo = self.treeview.item(seleccionado)["values"][0]  # Obtener el nombre del archivo
            ubicacion = self.treeview.item(seleccionado)["values"][1]  # Obtener la ubicación del archivo
            ruta_archivo = os.path.join(ubicacion, archivo)
            try:
                os.remove(ruta_archivo)  # Eliminar el archivo del sistema
                self.treeview.delete(seleccionado)  # Eliminar el archivo del treeview
                messagebox.showinfo("Información", "Archivo eliminado: {}".format(ruta_archivo))
            except Exception as e:
                messagebox.showerror("Error", "Error al eliminar el archivo: {}".format(e))

    def configurar_tamano_filas(self, event=None):
        # Ajustar el ancho de las columnas al ancho de la ventana
        ancho_ventana = self.root.winfo_width()
        if ancho_ventana > 0:
            ancho_columna = ancho_ventana // 4  # Dividir en 4 columnas
            for col in self.treeview["columns"]:
                self.treeview.column(col, width=ancho_columna)
            # Ajustar el ancho de la primera columna para que ocupe el espacio restante
            self.treeview.column("#0", width=0, stretch=tk.YES)  # Eliminar espacio para el checkbox

    def abrir_ubicacion_archivo(self, event):
        seleccionado = self.treeview.selection()
        if seleccionado:
            archivo = self.treeview.item(seleccionado[0])["values"][0]  # Obtener el nombre del archivo
            ubicacion = self.treeview.item(seleccionado[0])["values"][1]  # Obtener la ubicación del archivo
            ruta_archivo = os.path.join(ubicacion, archivo)
            if os.path.exists(ruta_archivo):
                # Obtener el comando para abrir la ubicación del archivo en el gestor de archivos por defecto
                if platform.system() == "Linux":
                    comando = ['nautilus', os.path.dirname(ruta_archivo)]
                elif platform.system() == "Windows":
                    comando = ['explorer', '/select,', ruta_archivo.replace('/', '\\')]
                else:
                    comando = ['open', '-R', ruta_archivo]  # En macOS, abre la ubicación del archivo en el Finder
                
                try:
                    # Ejecutar el comando del sistema para abrir la ubicación del archivo de manera asíncrona
                    subprocess.Popen(comando)
                except Exception as e:
                    messagebox.showerror("Error", "Error al abrir la ubicación del archivo: {}".format(e))
            else:
                messagebox.showerror("Error", "El archivo ya no existe en la ubicación: {}".format(ruta_archivo))
                
class Repositorios:
    
    """
Clase 'Repositorios'.

Class:
    - Repositorios: Clase para gestionar los repositorios del sistema.

Attributes:
    - master: El widget principal al que pertenece la ventana.

Methods:
    - __init__(self, master): Constructor de la clase. Inicializa la ventana y sus componentes.
        - master: El widget principal al que pertenece la ventana.
    - hacer_backup_sources_list(self): Realiza una copia de seguridad del archivo sources.list.
    - restaurar_backup(self): Restaura la copia de seguridad del archivo sources.list.
    - agregar_repositorio(self): Abre una ventana para que el usuario agregue un nuevo repositorio.
    - mostrar_repositorios(self): Muestra la lista de repositorios instalados.
    - seleccionar_repositorio(self, listbox): Maneja la selección de un repositorio en la lista.
        - listbox: El Listbox que contiene la lista de repositorios.
    - mostrar_ventana_accion_repo(self, repo_seleccionado): Muestra una ventana de diálogo para editar o eliminar un repositorio seleccionado.
        - repo_seleccionado: El repositorio seleccionado.
    - eliminar_repo(self, repo_a_eliminar, ventana_dialogo): Elimina un repositorio seleccionado.
        - repo_a_eliminar: El repositorio a eliminar.
        - ventana_dialogo: La ventana de diálogo asociada.
    - editar_repositorio(self, repo_original, repo_nuevo, ventana_dialogo): Edita un repositorio existente con una nueva URL.
        - repo_original: La URL del repositorio original.
        - repo_nuevo: La nueva URL del repositorio.
        - ventana_dialogo: La ventana de diálogo asociada.
    - obtener_repositorios_instalados(self): Obtiene la lista de repositorios instalados en el sistema.
    - mostrar_advertencia_copia_seguridad(self): Muestra una advertencia sobre la copia de seguridad del archivo sources.list.
    - actualizar_repositorios(self): Actualiza la lista de repositorios mostrada en la interfaz de usuario.

Functions:
    - abrir_administrador_repositorios(): Abre una ventana para administrar los repositorios del sistema.

Raises:
    - No se especifican excepciones en la clase.
"""
    
    def __init__(self, master):
        self.master = master
        master.title("Gestor de Repositorios")

        # Crear un marco para los botones de acción
        self.frame_botones = tk.Frame(master)
        self.frame_botones.pack(padx=10, pady=10)

        # Botones para agregar y restaurar repositorios
        tk.Button(self.frame_botones, text="Añadir Repositorio", command=self.agregar_repositorio).pack(side=tk.LEFT, padx=10)
        tk.Button(self.frame_botones, text="Restaurar sources.list", command=self.restaurar_backup).pack(side=tk.LEFT, padx=10)

        # Crear un marco para mostrar la lista de repositorios
        self.frame_repositorios = tk.Frame(master)
        self.frame_repositorios.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        # Inicializar la contraseña como None
        self.contrasena = None

        # Mostrar la lista de repositorios
        self.mostrar_repositorios()

        # Mostrar una advertencia sobre la copia de seguridad
        self.mostrar_advertencia_copia_seguridad()

    def hacer_backup_sources_list(self):
        contrasena = obtener_contrasena()
        if contrasena is None:
            messagebox.showwarning("Contraseña requerida", "Debes ingresar la contraseña para ejecutar esta acción.")
            return

        try:
            # Ejecutar el comando sudo cp para hacer una copia de seguridad del archivo sources.list
            comando = ['sudo', '-S', 'cp', '/etc/apt/sources.list', '/etc/apt/sources.list.bak']
            proceso = subprocess.run(comando, input=contrasena.encode(), text=True, capture_output=True, check=True)
            messagebox.showinfo("Éxito", "Copia de seguridad de sources.list creada correctamente.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"No se pudo hacer una copia de seguridad de sources.list: {e}")

    def restaurar_backup(self):
        try:
            contrasena = obtener_contrasena()
            if contrasena is None:
                messagebox.showwarning("Contraseña requerida", "Debes ingresar la contraseña para ejecutar esta acción.")
                return

            # Ejecutar el comando sudo cp para restaurar la copia de seguridad del archivo sources.list
            comando = ['sudo', '-S', 'cp', '/etc/apt/sources.list.bak', '/etc/apt/sources.list']
            proceso = subprocess.run(comando, input=contrasena.encode(), text=True, capture_output=True, check=True)
            
            # Verificar si la copia de seguridad se restauró correctamente
            if proceso.returncode == 0:
                messagebox.showinfo("Éxito", "Copia de seguridad restaurada correctamente.")
                # Actualizar la lista de repositorios después de restaurar la copia de seguridad
                self.actualizar_repositorios()
            else:
                messagebox.showerror("Error", "No se pudo restaurar la copia de seguridad.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo restaurar la copia de seguridad: {e}")

    def agregar_repositorio(self):
        # Función interna para manejar el botón de "Guardar" en la ventana de agregar repositorio
        def guardar_repositorio():
            url = entry_url.get()
            if not url:
                messagebox.showerror("Error", "Por favor, ingrese la URL del repositorio.")
                return

            contrasena = obtener_contrasena()
            if not contrasena:
                return
            
            self.hacer_backup_sources_list()  # Hacer una copia de seguridad del archivo sources.list
            
            try:
                subprocess.run(['sudo', '-S', 'add-apt-repository', url], input=contrasena.encode(), check=True)
                messagebox.showinfo("Éxito", f"Repositorio {url} agregado correctamente.")
                ventana_agregar.destroy()
                # Actualizar la lista de repositorios después de agregar uno nuevo
                self.actualizar_repositorios()
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"No se pudo agregar el repositorio: {e}")

        # Crear una nueva ventana para agregar el repositorio
        ventana_agregar = tk.Toplevel(self.master)
        ventana_agregar.title("Agregar Repositorio")

        # Etiqueta y campo de entrada para la URL del repositorio
        tk.Label(ventana_agregar, text="URL del Repositorio:").pack()
        entry_url = tk.Entry(ventana_agregar, width=50)
        entry_url.pack()

        # Botón para guardar el repositorio
        boton_guardar = tk.Button(ventana_agregar, text="Guardar", command=guardar_repositorio)
        boton_guardar.pack(pady=5)

    def mostrar_repositorios(self):
        # Limpiar el contenido del marco antes de mostrar la lista de repositorios
        for widget in self.frame_repositorios.winfo_children():
            widget.destroy()

        # Obtener la lista de repositorios instalados
        lista_repositorios = self.obtener_repositorios_instalados()

        # Crear una barra de desplazamiento vertical
        scrollbar = tk.Scrollbar(self.frame_repositorios, orient=tk.VERTICAL)

        # Crear un Listbox para mostrar los repositorios
        repos_listbox = tk.Listbox(self.frame_repositorios, yscrollcommand=scrollbar.set)

        # Agregar cada repositorio a la Listbox
        for repo in lista_repositorios:
            repos_listbox.insert(tk.END, repo)

        # Configurar la relación entre el Listbox y la barra de desplazamiento
        scrollbar.config(command=repos_listbox.yview)

        # Empacar la barra de desplazamiento y el Listbox en el marco de repositorios
        repos_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Asociar un evento de selección al Listbox para realizar acciones
        repos_listbox.bind('<<ListboxSelect>>', lambda event: self.seleccionar_repositorio(repos_listbox))

        # Configurar el tamaño de la ventana secundaria
        self.master.geometry("600x400")

        # Centrar la ventana secundaria
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x_offset = (self.master.winfo_screenwidth() - width) // 2
        y_offset = (self.master.winfo_screenheight() - height) // 2
        self.master.geometry(f"+{x_offset}+{y_offset}")

        
    def seleccionar_repositorio(self, listbox):
        # Obtener el índice del elemento seleccionado
        seleccion = listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            # Obtener el valor del repositorio seleccionado
            repo_seleccionado = listbox.get(indice)
            # Mostrar una ventana de diálogo para editar o eliminar el repositorio
            self.mostrar_ventana_accion_repo(repo_seleccionado)
    
    def mostrar_ventana_accion_repo(self, repo_seleccionado):
        # Crear una nueva ventana de diálogo
        ventana_dialogo = tk.Toplevel(self.master)
        ventana_dialogo.title("Editar o Eliminar Repositorio")

        # Etiqueta y campo de entrada para mostrar la URL del repositorio seleccionado
        tk.Label(ventana_dialogo, text="URL del Repositorio:").pack()
        entry_url = tk.Entry(ventana_dialogo, width=50)
        entry_url.insert(tk.END, repo_seleccionado)
        entry_url.pack()

        # Agregar menú contextual para el campo de entrada
        menu_contextual = tk.Menu(ventana_dialogo, tearoff=0)
        menu_contextual.add_command(label="Pegar", command=lambda: entry_url.event_generate("<<Paste>>"))
        entry_url.bind("<Button-3>", lambda event: menu_contextual.post(event.x_root, event.y_root))

        # Botones para aplicar cambios, eliminar o cancelar la operación
        boton_editar = tk.Button(ventana_dialogo, text="Editar Repositorio", command=lambda: self.editar_repositorio(repo_seleccionado, entry_url.get(), ventana_dialogo))
        boton_editar.pack(pady=5)
        boton_eliminar = tk.Button(ventana_dialogo, text="Eliminar Repositorio", command=lambda: self.eliminar_repo(repo_seleccionado, ventana_dialogo))
        boton_eliminar.pack(pady=5)
        boton_cancelar = tk.Button(ventana_dialogo, text="Cancelar", command=ventana_dialogo.destroy)
        boton_cancelar.pack(pady=5)

    def eliminar_repo(self, repo_a_eliminar, ventana_dialogo):
        # Solicitar confirmación al usuario antes de eliminar el repositorio
        confirmacion = messagebox.askyesno("Confirmación", f"¿Estás seguro de que deseas eliminar el repositorio '{repo_a_eliminar}'?")
        if confirmacion:
            contrasena = obtener_contrasena()
            if not contrasena:
                return

            try:
                self.hacer_backup_sources_list()  # Hacer una copia de seguridad del archivo sources.list
                # Ejecutar el comando para eliminar el repositorio
                subprocess.run(['sudo', '-S', 'add-apt-repository', '--remove', repo_a_eliminar], input=contrasena.encode(), check=True)
                messagebox.showinfo("Éxito", "Repositorio eliminado correctamente.")
                ventana_dialogo.destroy()
                # Actualizar la lista de repositorios después de eliminar uno
                self.actualizar_repositorios()
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"No se pudo eliminar el repositorio: {e}")

    def editar_repositorio(self, repo_original, repo_nuevo, ventana_dialogo):
        try:
            contrasena = obtener_contrasena()
            if not contrasena:
                return
            
            self.hacer_backup_sources_list()  # Hacer una copia de seguridad del archivo sources.list
            # Ejecutar el comando para editar el repositorio
            subprocess.run(['sudo', '-S', 'add-apt-repository', '--remove', repo_original], input=contrasena.encode(), check=True)
            subprocess.run(['sudo', '-S', 'add-apt-repository', repo_nuevo], input=contrasena.encode(), check=True)
            messagebox.showinfo("Éxito", "Repositorio editado correctamente.")
            ventana_dialogo.destroy()
            # Actualizar la lista de repositorios después de editar uno
            self.actualizar_repositorios()
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"No se pudo editar el repositorio: {e}")

    def obtener_repositorios_instalados(self):
        # Comando para obtener la lista de repositorios
        comando = "apt-cache policy | grep http | awk '{print $2 $3}'"

        # Ejecutar el comando y recuperar la salida
        try:
            resultado = subprocess.run(comando, shell=True, text=True, capture_output=True, check=True)
            repositorios = resultado.stdout.strip().split('\n')
            return repositorios
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"No se pudieron obtener los repositorios: {e}")
            return []

    def mostrar_advertencia_copia_seguridad(self):
        messagebox.showwarning("Advertencia", "Se realizará una copia de seguridad del archivo sources.list antes de hacer cualquier modificación. La ubicación de la copia de seguridad será: /etc/apt/sources.list.bak")

    def actualizar_repositorios(self):
        self.mostrar_repositorios()

def abrir_administrador_repositorios():
    ventana_admin_repos = tk.Toplevel(ventana_principal)
    ventana_admin_repos.title("Administrador de Repositorios")
    Repositorios(ventana_admin_repos)

# Ejecutar la ventana principal solo si este archivo se ejecuta directamente
if __name__ == "__main__":
    ventana_principal = tk.Tk()
    boton_admin_repos = tk.Button(ventana_principal, text="Administrar Repositorios", command=abrir_administrador_repositorios)
    boton_admin_repos.pack()
    ventana_principal.mainloop()
    
class MonitorizarSistema:
    
    """
Clase 'MonitorizarSistema'.

Class:
    - MonitorizarSistema: Clase para monitorizar el sistema y visualizar estadísticas en una ventana emergente.

Attributes:
    - master: El widget principal al que pertenece la ventana.

Methods:
    - __init__(self, master): Constructor de la clase. Inicializa el widget principal al que pertenece la ventana.
        - master: El widget principal al que pertenece la ventana.
    - monitorizar_sistema(self): Método para monitorizar el sistema y visualizar estadísticas en una ventana emergente.

Raises:
    - No se especifican excepciones en la clase.
"""
    
    def __init__(self, master):
        self.master = master

    def monitorizar_sistema(self):
        # Ocultar la ventana principal temporalmente
        self.master.withdraw()

        # Obtener los datos del sistema
        cpu_percent = psutil.cpu_percent()
        mem_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent
        # Obtener los datos de red
        red_info = psutil.net_io_counters(pernic=False)
        red_envio = red_info.bytes_sent
        red_recepcion = red_info.bytes_recv
        temperatura_cpu = psutil.sensors_temperatures().get('cpu_thermal', [None])[0].current if 'cpu_thermal' in psutil.sensors_temperatures() else None
        carga_sistema = psutil.getloadavg()[0]

        # Crear listas de nombres, valores y colores para los datos
        nombres = ['CPU', 'Memoria', 'Disco', 'Red (enviado)', 'Red (recibido)', 'Temperatura CPU', 'Carga del sistema']
        valores = [cpu_percent, mem_percent, disk_percent, red_envio / 1024 / 1024, red_recepcion / 1024 / 1024, temperatura_cpu, carga_sistema]
        colores = ['blue', 'green', 'red', 'orange', 'purple', 'cyan', 'magenta']

        # Filtrar los datos que no están disponibles y actualizar las listas
        nombres = [n for n, v in zip(nombres, valores) if v is not None]
        valores = [v for v in valores if v is not None]
        colores = colores[:len(valores)]

        # Crear una nueva ventana de Tkinter
        ventana_grafico = tk.Toplevel(self.master)
        ventana_grafico.title("Estadísticas")

        # Crear una figura de Matplotlib
        fig, ax = plt.subplots(figsize=(12, 8))

        # Visualizar los datos en un gráfico de barras
        ax.bar(nombres, valores, color=colores)
        ax.set_xlabel('Recursos del Sistema')
        ax.set_ylabel('Porcentaje de Uso / Valor')
        ax.set_title('Monitorización del Sistema')
        ax.grid(True)

        # Crear un lienzo de Matplotlib para integrarlo en la ventana de Tkinter
        canvas = FigureCanvasTkAgg(fig, master=ventana_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Vincular el evento de cierre de la ventana a una función que solo destruya la ventana de gráficos
        ventana_grafico.protocol("WM_DELETE_WINDOW", ventana_grafico.destroy)
        ventana_grafico.mainloop()