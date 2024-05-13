import subprocess
from tkinter import messagebox
from password import obtener_contrasena

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
