import subprocess
import sys
from password import obtener_contrasena
import tkinter as tk
from tkinter import messagebox, ttk

# Lista de dependencias del sistema junto con sus métodos de instalación
DEPENDENCIAS_SISTEMA = {
    "samba": ["sudo", "apt", "install", "-y", "samba"],
    "nmap": ["sudo", "apt", "install", "-y", "python3-nmap"],
    "net-tools": ["sudo", "apt", "install", "-y", "net-tools"],
    "ethtool": ["sudo", "apt", "install", "-y", "ethtool"],
    "gnome-terminal": ["sudo", "apt", "install", "-y", "gnome-terminal"],
    "python3-psutil": ["sudo", "apt", "install", "-y", "python3-psutil"],
    "smartmontools": ["sudo", "apt", "install", "-y", "smartmontools"],
    "traceroute": ["sudo", "apt", "install", "-y", "traceroute"],
    "python3-dbus": ["sudo", "apt", "install", "-y", "python3-dbus"],
    "python3-tk": ["sudo", "apt", "install", "-y", "python3-tk"],
}

def verificar_dependencias_sistema():
    dependencias_faltantes = []
    for dependencia, instalacion in DEPENDENCIAS_SISTEMA.items():
        proceso = subprocess.run(['apt', 'list', '--installed', dependencia], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proceso.returncode != 0 or dependencia not in proceso.stdout:
            dependencias_faltantes.append(dependencia)
    
    if dependencias_faltantes:
        mensaje = "Las siguientes dependencias del sistema no están instaladas:\n\n"
        mensaje += "\n".join(dependencias_faltantes)
        messagebox.showinfo("Dependencias faltantes", mensaje)
        return False
    else:
        return True

def instalar_dependencias(progress_bar=None):
    """
    Instala las dependencias del sistema y las dependencias de Python.

    Args:
        progress_bar (ttk.Progressbar, optional): Indicador de progreso para mostrar durante la instalación. Defaults to None.

    Returns:
        bool: True si la instalación se realiza correctamente, False si hay algún error durante la instalación.
    """
    total_dependencias = len(DEPENDENCIAS_SISTEMA) + 1  # +1 para incluir las dependencias de Python
    progreso_actual = 0
    contrasena = obtener_contrasena()

    # Instalar dependencias del sistema
    for dependencia, metodo_instalacion in DEPENDENCIAS_SISTEMA.items():
        print(f"Instalando {dependencia}...")
        try:
            proceso_instalacion = subprocess.Popen(["sudo", "-S"] + metodo_instalacion, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            salida, error = proceso_instalacion.communicate(input=contrasena + "\n")
            if proceso_instalacion.returncode != 0:
                if progress_bar:
                    messagebox.showerror("Error de instalación", f"No se pudo instalar {dependencia}: {error}")
                    sys.exit(1)
                else:
                    print(f"No se pudo instalar {dependencia}: {error}")
                return False
            
            progreso_actual += 1
            if progress_bar:
                progreso = int((progreso_actual / total_dependencias) * 100)
                progress_bar["value"] = progreso
                progress_bar.update()
        except subprocess.CalledProcessError as e:
            if progress_bar:
                messagebox.showerror("Error de instalación", f"No se pudo instalar {dependencia}: {e}")
            else:
                print(f"No se pudo instalar {dependencia}: {e}")
            return False

    # Instalar dependencias de Python
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        progreso_actual += 1
        if progress_bar:
            progreso = int((progreso_actual / total_dependencias) * 100)
            progress_bar["value"] = progreso
            progress_bar.update()
        return True
    except subprocess.CalledProcessError as e:
        if progress_bar:
            messagebox.showerror("Error de instalación", f"No se pudieron instalar las dependencias de Python: {e}")
        else:
            print(f"No se pudieron instalar las dependencias de Python: {e}")
        return False

def verificar_dependencias():
    if not verificar_dependencias_sistema():
        return False
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'check'])
        return True
    except subprocess.CalledProcessError:
        return False
