"""
Funciones relacionadas con el descubrimiento de dispositivos en la red local y la gestión de eventos.

Imports:
    - tkinter as tk: Para la interfaz gráfica.
    - messagebox desde tkinter: Para mostrar mensajes de alerta.
    - nmap: Para escanear la red local en busca de dispositivos.
    - subprocess: Para ejecutar procesos del sistema.
    - threading: Para ejecutar operaciones en segundo plano.

Funciones:
    - encontrar_dispositivos_en_red(): Escanea la red local en busca de dispositivos y devuelve una lista de direcciones IP.
    - abrir_administrador_de_archivos(ip): Abre el administrador de archivos del sistema para la dirección IP especificada.
    - doble_clic(_, lista_dispositivos): Maneja el evento de doble clic en la lista de dispositivos, abriendo el administrador de archivos 
    para la IP seleccionada.

Raises:
    - FileNotFoundError: Si el administrador de archivos correspondiente no está instalado en el sistema.
    - Exception: Si ocurre un error al abrir el administrador de archivos.
"""

import tkinter as tk
from tkinter import messagebox
import nmap
import subprocess
import threading

# Función para encontrar dispositivos en la red local
def encontrar_dispositivos_en_red():
    nm = nmap.PortScanner()
    nm.scan(hosts='192.168.1.0/24', arguments='-sn')
    dispositivos = [host for host in nm.all_hosts()]
    return dispositivos

def abrir_administrador_de_archivos(ip):
    try:
        subprocess.Popen(['nautilus', f'smb://{ip}'])  # Cambiar 'nautilus' al administrador de archivos correspondiente en el sistema
    except FileNotFoundError:
        messagebox.showerror("Error", "Administrador de archivos no encontrado.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al abrir el administrador de archivos: {e}")


# Función para manejar el evento de doble clic
def doble_clic(_, lista_dispositivos):
    ip_seleccionada = lista_dispositivos.get(tk.ACTIVE)
    threading.Thread(target=abrir_administrador_de_archivos, args=(ip_seleccionada,)).start()

