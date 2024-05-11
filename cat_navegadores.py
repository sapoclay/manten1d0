import subprocess
import os
import threading
from tkinter import messagebox

# Clase para realizar la limpieza de la caché de los navegadores
class LimpiadorNavegadores:
    @staticmethod
    def limpiar_cache_chrome(window, boton, callback=None):
        # Deshabilitar el botón para evitar múltiples clics
        boton.config(state="disabled")
        chrome_path = '/usr/bin/google-chrome'
        if not os.path.exists(chrome_path):
            return "Google Chrome no está instalado o no se encuentra en la ruta por defecto."
        
        try:
            mensaje = "Limpiando caché de Google Chrome..."
            if callback:
                callback(mensaje)

            # Eliminar el directorio de caché de Google Chrome
            chrome_cache_path = os.path.expanduser("~/.cache/google-chrome")
            if os.path.exists(chrome_cache_path):
                os.system(f"rm -rf {chrome_cache_path}")

            # Limpiar la caché de Google Chrome
            threading.Thread(target=LimpiadorNavegadores._limpiar_cache, args=(window, boton, chrome_path, '--clear-browser-data', callback)).start()

        except Exception as e:
            return f"Error al limpiar la caché de Google Chrome: {e}"

    @staticmethod
    def limpiar_cache_firefox(window, boton, callback=None):
        # Deshabilitar el botón para evitar múltiples clics
        boton.config(state="disabled")
        firefox_path = '/usr/bin/firefox'
        if not os.path.exists(firefox_path):
            return "Mozilla Firefox no está instalado o no se encuentra en la ruta por defecto."
        
        try:
            mensaje = "Limpiando caché de Mozilla Firefox..."
            if callback:
                callback(mensaje)

            # Eliminar el directorio de caché de Mozilla Firefox
            firefox_cache_path = os.path.expanduser("~/.cache/mozilla")
            if os.path.exists(firefox_cache_path):
                os.system(f"rm -rf {firefox_cache_path}")

            # Limpiar la caché de Mozilla Firefox
            threading.Thread(target=LimpiadorNavegadores._limpiar_cache, args=(window, boton, firefox_path, '--clear-cache', callback)).start()

        except Exception as e:
            return f"Error al limpiar la caché de Mozilla Firefox: {e}"

    @staticmethod
    def limpiar_cache_edge(window, boton, callback=None):
        # Deshabilitar el botón para evitar múltiples clics
        boton.config(state="disabled")
        edge_path = '/usr/bin/microsoft-edge'
        if not os.path.exists(edge_path):
            return "Microsoft Edge no está instalado o no se encuentra en la ruta por defecto."
        
        try:
            mensaje = "Limpiando caché de Microsoft Edge..."
            if callback:
                callback(mensaje)

            # Eliminar el directorio de caché de Microsoft Edge
            edge_cache_path = os.path.expanduser("~/.cache/microsoft-edge")
            if os.path.exists(edge_cache_path):
                os.system(f"rm -rf {edge_cache_path}")

            # Limpiar la caché de Microsoft Edge
            threading.Thread(target=LimpiadorNavegadores._limpiar_cache, args=(window, boton, edge_path, '--clear-browser-data', callback)).start()
            
        except Exception as e:
            return f"Error al limpiar la caché de Microsoft Edge: {e}"

    @staticmethod
    def _limpiar_cache(window, boton, executable, argument, callback=None):
        try:
            subprocess.run([executable, argument], check=True)
            mensaje = "Caché limpiada correctamente."
            if callback:
                callback(mensaje)
                boton.config(state="normal")
        except subprocess.CalledProcessError as e:
            mensaje = f"Error al limpiar la caché: {e}"
            if callback:
                callback(mensaje)
    
    @staticmethod
    def limpiar_historial_chrome():
        try:
            # Comando para limpiar el historial de Chrome en Linux
            subprocess.run(["google-chrome", "--delete-history"], check=True)
            messagebox.showinfo("Éxito", "Historial de Chrome limpiado con éxito.")
        except (subprocess.CalledProcessError, FileNotFoundError):
            messagebox.showerror("Error", "No se pudo limpiar el historial de Chrome. Asegúrate de tener Google Chrome instalado.")

    @staticmethod
    def limpiar_historial_firefox():
        try:
            # Comando para limpiar el historial de Firefox en Linux
            subprocess.run(["firefox", "--delete-history"], check=True)
            messagebox.showinfo("Éxito", "Historial de Firefox limpiado con éxito.")
        except (subprocess.CalledProcessError, FileNotFoundError):
            messagebox.showerror("Error", "No se pudo limpiar el historial de Firefox. Asegúrate de tener Mozilla Firefox instalado.")

    @staticmethod
    def limpiar_historial_edge():
        try:
            # Comando para limpiar el historial de Edge en Linux
            subprocess.run(["microsoft-edge", "--delete-history"], check=True)
            messagebox.showinfo("Éxito", "Historial de Edge limpiado con éxito.")
        except (subprocess.CalledProcessError, FileNotFoundError):
            messagebox.showerror("Error", "No se pudo limpiar el historial de Edge. Asegúrate de tener Microsoft Edge instalado.")


