"""
Clases y funciones para realizar copias de seguridad y operaciones de cifrado y descifrado de archivos.

Dependencias:
    - subprocess: Para ejecutar comandos en el sistema operativo.
    - messagebox de tkinter: Para mostrar mensajes de error en ventanas emergentes.
    - os: Para interactuar con el sistema operativo.
    - tkinter: Para la interfaz gráfica de usuario.
    - filedialog de tkinter: Para seleccionar archivos y ubicaciones.
    - obtener_contrasena de password: Para obtener la contraseña del usuario.
    - cryptography.hazmat: Para realizar operaciones de cifrado y descifrado de archivos.

Clases:
    - CopiaSeguridad: Permite realizar una copia de seguridad de un directorio.
    - RestaurarCopiaSeguridad: Permite restaurar una copia de seguridad en un directorio.

Funciones:
    - generar_clave_maestra: Genera una clave maestra a partir de la contraseña del usuario y un salt.
    - cifrar_archivo: Permite cifrar un archivo seleccionado por el usuario usando ChaCha20.
    - descifrar_archivo: Permite descifrar un archivo cifrado seleccionado por el usuario.
"""
 
import subprocess
from tkinter import messagebox
from password import obtener_contrasena
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from password import obtener_contrasena  
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class CopiaSeguridad:
    def __init__(self, origen, destino):
        self.origen = origen
        self.destino = destino
    
    def realizar_copia_seguridad(self):
        try:
            # Obtener la contraseña de sudo
            contrasena = obtener_contrasena()
            # Crear el archivo de copia de seguridad con tar usando sudo y la contraseña proporcionada
            if self.destino.startswith("/"):
                # La ruta de destino es una ruta absoluta, por lo que es necesario usar sudo
                comando = f"echo '{contrasena}' | sudo -S tar -czvf {self.destino} -C {self.origen} ."
            else:
                # La ruta de destino es una ruta relativa, no es necesario usar sudo
                comando = f"tar -czvf {self.destino} -C {self.origen} ."
            subprocess.run(comando, shell=True)
            return True
        except Exception as e:
            # Mostrar mensaje de error en una ventana emergente
            messagebox.showerror("Error", f"Error al realizar la copia de seguridad: {e}")
            return False

class RestaurarCopiaSeguridad:
    def __init__(self, origen, destino):
        self.origen = origen
        self.destino = destino
    
    def restaurar_copia_seguridad(self):
        try:
            # Obtener la contraseña de sudo
            contrasena = obtener_contrasena()
            # Restaurar la copia de seguridad con tar usando sudo y la contraseña proporcionada
            comando = f"echo '{contrasena}' | sudo -S tar -xzvf {self.origen} -C {self.destino}"
            subprocess.run(comando, shell=True)
            return True
        except Exception as e:
            # Mostrar mensaje de error en una ventana emergente
            messagebox.showerror("Error", f"Error al restaurar la copia de seguridad: {e}")
            return False


# Función para generar una clave derivada de la contraseña
def generar_clave_maestra(contrasena, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(contrasena.encode())

def cifrar_archivo():
    dir_usuario = os.path.expanduser('~')
        
    # Seleccionar el archivo a cifrar
    archivo_a_cifrar = filedialog.askopenfilename(
        title="Seleccionar archivo a cifrar",
        initialdir=dir_usuario
    )
        
    if not archivo_a_cifrar:
        return

    # Obtener la contraseña del usuario
    contrasena = obtener_contrasena()
    if not contrasena:
        return

    # Generar un salt aleatorio
    salt = os.urandom(16)

    # Generar la clave maestra a partir de la contraseña y el salt
    clave_maestra = generar_clave_maestra(contrasena, salt)

    # Generar un nonce aleatorio para el cifrado
    nonce = os.urandom(16)

    # Leer los datos del archivo a cifrar
    with open(archivo_a_cifrar, 'rb') as f:
        datos = f.read()

    # Inicializar el cifrador ChaCha20
    cipher = Cipher(algorithms.ChaCha20(clave_maestra, nonce), mode=None, backend=default_backend())
    encryptor = cipher.encryptor()

    # Cifrar los datos
    datos_cifrados = encryptor.update(datos) + encryptor.finalize()

    # Seleccionar la ubicación y el nombre del archivo cifrado
    archivo_salida = filedialog.asksaveasfilename(
        title="Guardar archivo cifrado",
        initialdir=dir_usuario,
        filetypes=(("Archivos cifrados", "*.cifrado"),),
        defaultextension=".cifrado",
        initialfile=archivo_a_cifrar.split('/')[-1] + ".cifrado"  # Nombre por defecto
    )
        
    if not archivo_salida:
        return

    # Escribir los datos cifrados y el salt en el archivo cifrado
    with open(archivo_salida, 'wb') as f:
        f.write(salt + nonce + datos_cifrados)

    messagebox.showinfo("Cifrado completado", f"El archivo {archivo_salida} ha sido cifrado con éxito.")


def descifrar_archivo():
    # Obtener el directorio de inicio del usuario
    dir_usuario = os.path.expanduser('~')

    # Definir los tipos de archivo a mostrar
    tipos_archivo = [("Archivos encriptados", "*.cifrado")]

    # Seleccionar el archivo cifrado a descifrar
    archivo_cifrado = filedialog.askopenfilename(
        title="Seleccionar archivo cifrado a descifrar",
        initialdir=dir_usuario,
        filetypes=tipos_archivo
    )
    if not archivo_cifrado:
        return

    # Obtener la contraseña del usuario
    contrasena = obtener_contrasena()
    if not contrasena:
        return

    # Leer el salt y el nonce del archivo cifrado
    with open(archivo_cifrado, 'rb') as file:
        salt = file.read(16)  # Leer el salt del archivo
        nonce = file.read(16)  # Leer el nonce del archivo
        datos_cifrados = file.read()  # Leer los datos cifrados

    # Generar la clave maestra a partir de la contraseña y el salt
    clave_maestra = generar_clave_maestra(contrasena, salt)

    # Inicializar el descifrador ChaCha20
    cipher = Cipher(algorithms.ChaCha20(clave_maestra, nonce), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()

    try:
        # Descifrar los datos
        datos_descifrados = decryptor.update(datos_cifrados) + decryptor.finalize()

        # Seleccionar la ubicación y el nombre del archivo descifrado
        archivo_descifrado = filedialog.asksaveasfilename(
            title="Guardar archivo descifrado",
            initialdir=dir_usuario,
            initialfile=os.path.basename(archivo_cifrado).replace('.cifrado', ''),
            filetypes=(("Todos los archivos", "*.*"),)
        )
        if not archivo_descifrado:
            # El usuario canceló la selección del archivo
            messagebox.showinfo("Operación cancelada por el usuario.")
            return

        # Escribir los datos descifrados en el archivo descifrado
        with open(archivo_descifrado, 'wb') as file:
            file.write(datos_descifrados)

        messagebox.showinfo("Descifrado completado", f"El archivo {archivo_cifrado} ha sido descifrado con éxito.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al descifrar el archivo: {e}")