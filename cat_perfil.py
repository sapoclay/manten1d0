"""
Este módulo proporciona una interfaz gráfica para modificar el perfil de usuario en un sistema operativo basado en Unix/Linux.

Módulos Importados:
- tkinter: Proporciona la funcionalidad para crear la interfaz gráfica de usuario.
- messagebox: Permite mostrar cuadros de mensaje.
- filedialog: Permite al usuario seleccionar archivos.
- simpledialog: Permite solicitar la entrada del usuario a través de cuadros de diálogo.
- PIL (Pillow): Proporciona herramientas para trabajar con imágenes.
- os: Proporciona una forma de usar funcionalidades dependientes del sistema operativo.
- subprocess: Permite ejecutar comandos del sistema operativo y capturar su salida.
- getpass: Proporciona una manera de manejar entradas sensibles como contraseñas.
- password: Contiene funciones para limpiar archivos de configuración y obtener contraseñas de sudo.
- tooltip: Proporciona una clase para mostrar tooltips en widgets de tkinter.
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os
from subprocess import Popen, PIPE
import subprocess
import getpass
from password import limpiar_archivos_configuracion, obtener_contrasena
from tooltip import ToolTip

class PerfilUsuario:
    """Clase para la interfaz de modificación del perfil de usuario."""
    def __init__(self, root):
        """Inicializa la interfaz gráfica de usuario.

        Args:
            root (tk.Tk): La ventana principal de tkinter.
        """
        self.root = root
        self.root.title("Modificar Perfil de Usuario en el Sistema Operativo")
        self.root.geometry("400x600")

        # Etiqueta y entrada para el nombre
        tk.Label(root, text="* Nombre:").pack()
        self.entry_nombre = tk.Entry(root)
        self.entry_nombre.pack()
        ToolTip(self.entry_nombre, "Escribe tu Nombre de Usuario")

        # Dibujar una línea horizontal
        self.canvas = tk.Canvas(root, width=200, height=2, bg="lightgrey", highlightthickness=0)
        self.canvas.create_line(0, 1, 500, 1, fill="silver")
        self.canvas.pack(pady=10)

        # Etiqueta y entrada para la contraseña
        tk.Label(root, text="* Contraseña:").pack()
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack()
        ToolTip(self.entry_password, "Escribe/Modifica la Contraseña para tu Usuario")

        # Etiqueta y entrada para la confirmación de la contraseña
        tk.Label(root, text="* Confirmar Contraseña:").pack()
        self.entry_confirm_password = tk.Entry(root, show="*")
        self.entry_confirm_password.pack()
        ToolTip(self.entry_confirm_password, "Confirma la Contraseña para tu Usuario")

        # Botón para mostrar/ocultar contraseña
        self.boton_mostrar_contrasena = tk.Button(root, text="Mostrar", command=self.mostrar_ocultar_contrasena)
        self.boton_mostrar_contrasena.pack()
        ToolTip(self.boton_mostrar_contrasena, "Mostrar/Ocultar Contraseña")

        # Dibujar una línea horizontal
        self.canvas = tk.Canvas(root, width=200, height=2, bg="lightgrey", highlightthickness=0)
        self.canvas.create_line(0, 1, 500, 1, fill="silver")
        self.canvas.pack(pady=10)

        # Botón para elegir una imagen de perfil
        self.seleccion_imagen = tk.Button(root, text="Seleccionar Imagen de Perfil", command=self.seleccionar_imagen)
        self.seleccion_imagen.pack(pady=5)
        ToolTip(self.seleccion_imagen, "Guardar Perfil de Usuario con los Datos Introducidos")
        
        # Previsualización de la imagen de perfil
        self.label_imagen = tk.Label(root)
        self.label_imagen.pack(pady=10)
        ToolTip(self.label_imagen, "Previsualización de la Imagen de Usuario")

        # Dibujar una línea horizontal
        self.canvas = tk.Canvas(root, width=200, height=2, bg="lightgrey", highlightthickness=0)
        self.canvas.create_line(0, 1, 500, 1, fill="silver")
        self.canvas.pack(pady=10)

        # Contenedor para los botones
        self.frame_botones = tk.Frame(root)
        self.frame_botones.pack(pady=10)

        # Botón para guardar los cambios
        self.boton_guardar_perfil = tk.Button(self.frame_botones, text="Guardar Perfil", command=self.guardar_perfil)
        self.boton_guardar_perfil.pack(side=tk.LEFT, padx=5)
        ToolTip(self.boton_guardar_perfil, "Guardar Perfil de Usuario con los Datos Introducidos")

        # Botón para cancelar
        self.boton_cancelar = tk.Button(self.frame_botones, text="Cancelar", command=root.destroy)
        self.boton_cancelar.pack(side=tk.LEFT, padx=5)
        ToolTip(self.boton_cancelar, "Cancelar el guardado del Perfil de Usuario")


        # Dibujar una línea horizontal
        self.canvas = tk.Canvas(root, width=200, height=2, bg="lightgrey", highlightthickness=0)
        self.canvas.create_line(0, 1, 500, 1, fill="silver")
        self.canvas.pack(pady=10)

        # Ruta de la imagen de perfil seleccionada
        self.imagen_perfil = None
        self.imagen_tk = None  # Retener la referencia a la imagen

        # Cargar los datos actuales del usuario
        self.cargar_datos_usuario()

    def mostrar_ocultar_contrasena(self):
        """Muestra u oculta la contraseña en los campos de entrada."""
        if self.entry_password.cget('show') == '*':
            self.entry_password.config(show='')
            self.entry_confirm_password.config(show='')
            self.boton_mostrar_contrasena.config(text="Ocultar")
        else:
            self.entry_password.config(show='*')
            self.entry_confirm_password.config(show='*')
            self.boton_mostrar_contrasena.config(text="Mostrar")

    def seleccionar_imagen(self):
        """Abre un cuadro de diálogo para seleccionar una imagen de perfil."""
        self.imagen_perfil = filedialog.askopenfilename(
            initialdir=os.path.expanduser("~"),
            title="Seleccionar Imagen de Perfil",
            filetypes=(("Archivos de imagen", "*.png *.jpg *.jpeg"), ("Todos los archivos", "*.*"))
        )
        if self.imagen_perfil:
            # Mostrar la previsualización de la imagen seleccionada
            self.mostrar_previsualizacion_imagen(self.imagen_perfil)
            messagebox.showinfo("Imagen seleccionada", f"Imagen seleccionada: {self.imagen_perfil}")

    def mostrar_previsualizacion_imagen(self, ruta_imagen):
        """Muestra una previsualización de la imagen de perfil seleccionada.

        Args:
            ruta_imagen (str): La ruta del archivo de imagen seleccionado.
        """
        try:
            imagen = Image.open(ruta_imagen)
            imagen.thumbnail((100, 100))
            self.imagen_tk = ImageTk.PhotoImage(imagen)  # Asignar la imagen a una variable de instancia
            self.label_imagen.config(image=self.imagen_tk)
            self.label_imagen.image = self.imagen_tk
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen de perfil: {e}")

    def cargar_datos_usuario(self):
        """Carga los datos actuales del usuario, incluyendo el nombre y la imagen de perfil."""
        try:
            username = getpass.getuser()
            # Obtener el nombre completo usando `getent`
            result = subprocess.run(['getent', 'passwd', username], capture_output=True, text=True, check=True)
            user_info = result.stdout.strip().split(':')
            nombre_completo = user_info[4].split(',')[0]  # GECOS field

            self.entry_nombre.insert(0, nombre_completo)

            # Cargar la imagen de perfil actual con sudo
            contrasena_sudo = obtener_contrasena()
            face_file = f'/var/lib/AccountsService/icons/{username}'
            user_accounts_file = f'/var/lib/AccountsService/users/{username}'

            # Intentar obtener el icono del archivo de usuario
            result = subprocess.run(
                ['sudo', '-S', 'cat', user_accounts_file],
                input=f"{contrasena_sudo}\n",
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                lines = result.stdout.splitlines()
                for line in lines:
                    if line.startswith('Icon='):
                        face_file = line.split('=')[1].strip()
                        break

            # Mostrar la imagen de perfil actual
            if os.path.exists(face_file):
                self.mostrar_previsualizacion_imagen(face_file)
            else:
                messagebox.showwarning("Advertencia", "No se encontró ninguna imagen de perfil actual.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos del usuario: {e}")

    def guardar_perfil(self):
        """Guarda los cambios en el perfil del usuario, incluyendo el nombre y la contraseña."""
        nombre = self.entry_nombre.get()
        password = self.entry_password.get()
        confirm_password = self.entry_confirm_password.get()

        # Validar la entrada
        if not nombre or not password or not confirm_password:
            messagebox.showerror("Error", "Todos los campos con * son obligatorios.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        # Obtener la contraseña de sudo
        contrasena_sudo = obtener_contrasena()

        try:
            # Actualizar el nombre completo
            subprocess.run(['sudo', '-S', 'usermod', '-c', nombre, getpass.getuser()], input=f"{contrasena_sudo}\n", text=True, check=True)

            # Cambiar la contraseña usando chpasswd
            passwd_input = f"{getpass.getuser()}:{password}"
            process = Popen(['sudo', 'chpasswd'], stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
            stdout, stderr = process.communicate(input=f"{passwd_input}\n")
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, 'chpasswd', output=stdout, stderr=stderr)

            # Preguntar al usuario si desea reiniciar la sesión para aplicar los cambios
            reiniciar_sesion = messagebox.askyesno("Reiniciar Sesión", "¿Quieres reiniciar la sesión para aplicar los cambios?")
            if reiniciar_sesion:
                limpiar_archivos_configuracion()
                subprocess.run(['pkill', '-HUP', '-u', getpass.getuser()])
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"No se pudo actualizar la contraseña: {e.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la contraseña: {e}")


