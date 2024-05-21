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
    "pciutils": ["sudo", "apt", "install", "-y", "pciutils"],
    "lshw": ["sudo", "apt", "install", "-y", "lshw"],
}

def verificar_dependencias_sistema():
    dependencias_faltantes = []
    for dependencia, instalacion in DEPENDENCIAS_SISTEMA.items():
        proceso = subprocess.run(['dpkg', '-s', dependencia], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proceso.returncode != 0:
            dependencias_faltantes.append(dependencia)
    
    if dependencias_faltantes:
        mensaje = "Las siguientes dependencias del sistema no están instaladas:\n\n"
        mensaje += "\n".join(dependencias_faltantes)
        messagebox.showinfo("Dependencias faltantes", mensaje)
        return False
    else:
        return True

def verificar_dependencias_pip():
    try:
        with open('requirements.txt', 'r') as req_file:
            required_packages = {}
            for line in req_file:
                line = line.strip()
                if '==' in line:
                    pkg, version = line.split('==')
                    required_packages[pkg] = version
                else:
                    required_packages[line] = None
            
        installed_packages = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'], universal_newlines=True)
        installed_packages_dict = {pkg.split('==')[0].lower(): pkg.split('==')[1] if '==' in pkg else None for pkg in installed_packages.splitlines()}

        #print(f"Paquetes instalados: {installed_packages_dict}")

        packages_to_install = []
        for pkg, version in required_packages.items():
            installed_version = installed_packages_dict.get(pkg.lower())
            if installed_version is None:
                print(f"{pkg} no está instalado.")
                packages_to_install.append(pkg if version is None else f"{pkg}=={version}")
            elif version is not None and installed_version != version:
                print(f"{pkg} tiene una versión diferente: instalada {installed_version}, requerida {version}.")
                packages_to_install.append(f"{pkg}=={version}")

        if packages_to_install:
            mensaje = "Las siguientes dependencias de Python no están instaladas o tienen versiones incorrectas:\n\n"
            mensaje += "\n".join(packages_to_install)
            messagebox.showinfo("Dependencias de Python faltantes", mensaje)
         #   print(f"Dependencias de Python faltantes: {packages_to_install}")
            return False
        else:
            #print("Todas las dependencias de Python están instaladas.")
            return True
    except Exception as e:
        #print(f"Error al verificar dependencias de Python: {e}")
        messagebox.showerror("Error", f"Error al verificar dependencias de Python: {e}")
        return False

def verificar_dependencias():
    sistema_ok = verificar_dependencias_sistema()
    pip_ok = verificar_dependencias_pip()
    return sistema_ok and pip_ok

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
        #print(f"Instalando {dependencia}...")
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
        with open('requirements.txt', 'r') as req_file:
            required_packages = {}
            for line in req_file:
                line = line.strip()
                if '==' in line:
                    pkg, version = line.split('==')
                    required_packages[pkg] = version
                else:
                    required_packages[line] = None
        
        installed_packages = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'], universal_newlines=True)
        installed_packages_dict = {pkg.split('==')[0].lower(): pkg.split('==')[1] if '==' in pkg else None for pkg in installed_packages.splitlines()}
        
        packages_to_install = [pkg if version is None else f"{pkg}=={version}" for pkg, version in required_packages.items() if pkg.lower() not in installed_packages_dict or (version is not None and installed_packages_dict[pkg.lower()] != version)]

        if packages_to_install:
            #print("Instalando dependencias de Python...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + packages_to_install)

            if progress_bar:
                progreso_actual += 1
                progreso = int((progreso_actual / total_dependencias) * 100)
                progress_bar["value"] = progreso
                progress_bar.update()
            return True
        else:
            if progress_bar:
                progreso_actual += 1
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
    except Exception as e:
        print(f"Error general al instalar dependencias de Python: {e}")
        messagebox.showerror("Error", f"Error general al instalar dependencias de Python: {e}")
        return False
