"""
Clase `LimpiadorNavegadores` y los módulos asociados para la limpieza de caché y historial de navegadores.
 
Imports:
    - subprocess: Para ejecutar procesos del sistema.
    - os: Para realizar operaciones relacionadas con el sistema operativo.
    - threading: Para ejecutar operaciones en segundo plano.
    - messagebox desde tkinter: Para mostrar mensajes de alerta.

Clase:
    - LimpiadorNavegadores: Clase estática que proporciona métodos para limpiar la caché y el historial de navegadores web.

Métodos Estáticos:
    - limpiar_cache_chrome(window, boton, callback=None): Limpia la caché de Google Chrome.
    - limpiar_cache_firefox(window, boton, callback=None): Limpia la caché de Mozilla Firefox.
    - limpiar_cache_edge(window, boton, callback=None): Limpia la caché de Microsoft Edge.
    - _limpiar_cache(window, boton, executable, argument, callback=None): Método privado para realizar la limpieza de caché.
    - limpiar_historial_chrome(): Limpia el historial de Google Chrome.
    - limpiar_historial_firefox(): Limpia el historial de Mozilla Firefox.
    - limpiar_historial_edge(): Limpia el historial de Microsoft Edge.

Raises:
    - FileNotFoundError: Si el ejecutable del navegador no se encuentra en la ruta por defecto.
    - subprocess.CalledProcessError: Si ocurre un error al ejecutar el comando para limpiar la caché o el historial.
"""

import os
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox

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
            threading.Thread(
                target=LimpiadorNavegadores._limpiar_cache,
                args=(window, boton, chrome_path, '--clear-browser-data', callback),
            ).start()

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
            threading.Thread(
                target=LimpiadorNavegadores._limpiar_cache,
                args=(window, boton, firefox_path, '--clear-cache', callback),
            ).start()

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
            threading.Thread(
                target=LimpiadorNavegadores._limpiar_cache,
                args=(window, boton, edge_path, '--clear-browser-data', callback),
            ).start()

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
            messagebox.showerror(
                "Error",
                "No se pudo limpiar el historial de Chrome. Asegúrate de tener Google Chrome instalado.",
            )

    @staticmethod
    def limpiar_historial_firefox():
        try:
            # Comando para limpiar el historial de Firefox en Linux
            subprocess.run(["firefox", "--delete-history"], check=True)
            messagebox.showinfo("Éxito", "Historial de Firefox limpiado con éxito.")
        except (subprocess.CalledProcessError, FileNotFoundError):
            messagebox.showerror(
                "Error",
                "No se pudo limpiar el historial de Firefox. Asegúrate de tener Mozilla Firefox instalado.",
            )

    @staticmethod
    def limpiar_historial_edge():
        try:
            # Comando para limpiar el historial de Edge en Linux
            subprocess.run(["microsoft-edge", "--delete-history"], check=True)
            messagebox.showinfo("Éxito", "Historial de Edge limpiado con éxito.")
        except (subprocess.CalledProcessError, FileNotFoundError):
            messagebox.showerror(
                "Error",
                "No se pudo limpiar el historial de Edge. Asegúrate de tener Microsoft Edge instalado.",
            )
class InstalarNavegadores:
    """
    Clase para instalar navegadores web en Ubuntu.

    Métodos estáticos disponibles:
        - instalar_chrome(): Instala Google Chrome.
        - instalar_firefox(): Instala Mozilla Firefox.
        - instalar_edge(): Instala Microsoft Edge.

    Ejemplo de uso:
        Para instalar Google Chrome:
            InstalarNavegadores.instalar_chrome()

        Para instalar Mozilla Firefox:
            InstalarNavegadores.instalar_firefox()

        Para instalar Microsoft Edge:
            InstalarNavegadores.instalar_edge()
    """
    @staticmethod
    def instalar_chrome():
        progress_window = tk.Toplevel()
        progress_window.title("Instalando Google Chrome")
        progress_bar = ttk.Progressbar(progress_window, length=300, mode="indeterminate")
        progress_bar.pack(pady=10)
        progress_bar.start()

        # Función para ejecutar los comandos en un hilo separado
        def instalar():
            try:
                subprocess.run([
                    "wget",
                    "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb",
                ], check=True)

                subprocess.run(
                    ["sudo", "dpkg", "-i", "google-chrome-stable_current_amd64.deb"],
                    check=True
                )

                subprocess.run(["sudo", "apt-get", "-f", "install", "-y"], check=True)

                os.remove("google-chrome-stable_current_amd64.deb")

                messagebox.showinfo("Éxito", "Google Chrome se ha instalado correctamente.")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Error al instalar Google Chrome: {e}")
            except FileNotFoundError as e:
                messagebox.showerror("Error", f"Error al eliminar el archivo: {e}")
            finally:
                progress_bar.stop()
                progress_window.destroy()

        # Ejecutar la función en un hilo separado
        threading.Thread(target=instalar).start()
            
    @staticmethod
    def instalar_firefox():
        progress_window = tk.Toplevel()
        progress_window.title("Instalando Mozilla Firefox")
        progress_bar = ttk.Progressbar(progress_window, length=300, mode="indeterminate")
        progress_bar.pack(pady=10)
        progress_bar.start()

        # Función para ejecutar los comandos en un hilo separado
        def instalar():
            try:
                subprocess.run(["sudo", "apt-get", "update"], check=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "firefox"], check=True)
                messagebox.showinfo("Éxito", "Mozilla Firefox se ha instalado correctamente.")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Error al instalar Mozilla Firefox: {e}")
            finally:
                progress_bar.stop()
                progress_window.destroy()

        # Ejecutar la función en un hilo separado
        threading.Thread(target=instalar).start()

    @staticmethod
    def instalar_edge():
        progress_window = tk.Toplevel()
        progress_window.title("Instalando Microsoft Edge")
        progress_bar = ttk.Progressbar(progress_window, length=300, mode="indeterminate")
        progress_bar.pack(pady=10)
        progress_bar.start()

        # Función para ejecutar los comandos en un hilo separado
        def instalar():
            try:
                # Descargar la clave GPG de Microsoft
                key_url = "https://packages.microsoft.com/keys/microsoft.asc"
                key_file = "/tmp/microsoft.asc"
                subprocess.run(["wget", "-qO", key_file, key_url], check=True)
                # Agregar la clave GPG al directorio trusted.gpg.d
                subprocess.run(["sudo", "mkdir", "-p", "/etc/apt/trusted.gpg.d"], check=True)
                subprocess.run(["sudo", "apt-key", "add", key_file], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                # Añadir el repositorio de Microsoft Edge
                subprocess.run([
                    "sudo",
                    "sh",
                    "-c",
                    'echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge.list',
                    ],
                    check=True,
                )
                # Actualizar el índice de paquetes
                subprocess.run(["sudo", "apt-get", "update"], check=True)
                # Instalar Microsoft Edge
                subprocess.run(["sudo", "apt-get", "install", "-y", "microsoft-edge-stable"], check=True)
                messagebox.showinfo("Éxito", "Microsoft Edge se ha instalado correctamente.")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Error al instalar Microsoft Edge: {e}")
            finally:
                progress_bar.stop()
                progress_window.destroy()

        # Ejecutar la función en un hilo separado
        threading.Thread(target=instalar).start()
