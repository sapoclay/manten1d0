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
import psutil
import socket

# Función para obtener la red local automáticamente
def obtener_red_local():
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET and not addr.address.startswith('127.'):
                ip_address = addr.address
                netmask = addr.netmask
                return f"{ip_address}/{netmask_to_cidr(netmask)}"
    return None

def netmask_to_cidr(netmask):
    return sum([bin(int(x)).count('1') for x in netmask.split('.')])

# Función para encontrar dispositivos en la red local
def encontrar_dispositivos_en_red():
    nm = nmap.PortScanner()
    red = obtener_red_local()
    if red:
        nm.scan(hosts=red, arguments='-sn')
        dispositivos = [host for host in nm.all_hosts()]
        return dispositivos
    else:
        return []

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

