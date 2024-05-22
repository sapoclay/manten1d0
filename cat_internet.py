"""
Este módulo contiene funciones para gestionar el reinicio de las tarjetas de red en un sistema Linux (Ubuntu). 
Utiliza varios módulos de Python para interactuar con el sistema operativo, obtener contraseñas, gestionar la interfaz gráfica de usuario 
y mostrar mensajes.

Clases:
    RedTools:
        Clase que proporciona herramientas para el manejo de la red.

        Args:
            root: El widget raíz de Tkinter.

        Attributes:
            root: El widget raíz de Tkinter.
            area_central: El área central donde se muestran las herramientas relacionadas con la red.

Funciones:
    reiniciar_servicio_red():
        Detecta y reinicia el servicio de red en uso (NetworkManager o systemd-networkd).

    reiniciar_networkmanager():
        Reinicia el servicio NetworkManager utilizando el comando systemctl.

    reiniciar_systemd_networkd():
        Reinicia el servicio systemd-networkd utilizando el comando systemctl.

    reiniciar_tarjeta_red(interfaz, etiqueta_ip_local_info, etiqueta_ip_publica_info, callback=None):
        Reinicia una interfaz de red específica desactivándola y activándola nuevamente. Actualiza las etiquetas de la interfaz gráfica con las nuevas direcciones IP.

    mostrar_resultado_ping(resultado_ping):
        Muestra el resultado de un comando ping en una nueva ventana de Tkinter.

    hacer_ping(entry_url):
        Realiza un comando ping a una URL especificada por el usuario y muestra el resultado.
"""
import subprocess
from password import obtener_contrasena
import time
from tkinter import messagebox
import shutil
from cat_informacion import Informacion
import tkinter as tk
import preferencias
import subprocess
import socket
import speedtest
import threading
from tkinter import scrolledtext


""" 

Funciones relacionadas con el reinicio de las tarjetas de red

"""
def reiniciar_servicio_red():
    """
    Detecta y reinicia el servicio de red en uso (NetworkManager o systemd-networkd).

    Si no se encuentra ningún servicio de red conocido, imprime un mensaje indicando la situación.
    """
    try:
        resultado = subprocess.run(['systemctl', 'list-units', '--type=service'], capture_output=True, text=True)
        servicios_red = resultado.stdout
        # Comprobar qué servicio de red está en uso
        if 'NetworkManager.service' in servicios_red:
            reiniciar_networkmanager()
        elif 'systemd-networkd.service' in servicios_red:
            reiniciar_systemd_networkd()
        else:
            print("No se encontró ningún servicio de red conocido en uso.")
    except Exception as e:
            print(f"Error al obtener los servicios de red: {e}")

def reiniciar_networkmanager():
    """
    Reinicia el servicio NetworkManager utilizando el comando systemctl.

    Si ocurre un error durante el reinicio, imprime un mensaje indicando la situación.
    """
    try:
        subprocess.run(['sudo', 'systemctl', 'restart', 'NetworkManager'], check=True)
        print("Se reinició el servicio NetworkManager.")
    except subprocess.CalledProcessError as e:
        print(f"Error al reiniciar NetworkManager: {e}")

def reiniciar_systemd_networkd():
    """
    Reinicia el servicio systemd-networkd utilizando el comando systemctl.

    Si ocurre un error durante el reinicio, imprime un mensaje indicando la situación.
    """
    try:
        subprocess.run(['sudo', 'systemctl', 'restart', 'systemd-networkd'], check=True)
        print("Se reinició el servicio systemd-networkd.")
    except subprocess.CalledProcessError as e:
        print(f"Error al reiniciar systemd-networkd: {e}")

def reiniciar_tarjeta_red(interfaz, etiqueta_ip_local_info, etiqueta_ip_publica_info, callback=None):
        """
        Reinicia una interfaz de red específica desactivándola y activándola nuevamente. 
        Actualiza las etiquetas de la interfaz gráfica con las nuevas direcciones IP.

        Args:
            interfaz (str): Nombre de la interfaz de red a reiniciar.
            etiqueta_ip_local_info (tk.Label): Etiqueta de Tkinter para mostrar la dirección IP local. Deshabilitado.
            etiqueta_ip_publica_info (tk.Label): Etiqueta de Tkinter para mostrar la dirección IP pública.Deshabilitado.
            callback (function, optional): Función de callback para ejecutar después de reiniciar la tarjeta de red.

        Si no se selecciona ninguna interfaz o no se proporciona la contraseña, muestra una advertencia. Si ifconfig no está instalado, 
        lo instala automáticamente.
        """
        try:
            # Verificar si se ha seleccionado una interfaz
            if not interfaz:
                messagebox.showwarning("Tarjeta de red no seleccionada", "Por favor, seleccione una tarjeta de red.")
                return

            # Obtener la contraseña
            contrasena = obtener_contrasena()
            if contrasena is None:
                messagebox.showwarning("Contraseña requerida", "Debes ingresar la contraseña para reiniciar la tarjeta de red.")
                return

            # Convertir la contraseña a cadena si es de tipo bytes
            if isinstance(contrasena, bytes):
                contrasena = contrasena.decode('utf-8')

            # Instalar ifconfig con sudo si no está instalado
            if not shutil.which("ifconfig"):
                messagebox.showinfo("Instalación de ifconfig", "ifconfig no está instalado en el sistema. Se procederá a su instalación.")

                comando_instalacion = ['sudo', '-S', 'apt', 'install', 'net-tools']
                proceso_instalacion = subprocess.run(comando_instalacion, input=contrasena, universal_newlines=True, check=True)
                if proceso_instalacion.returncode == 0:
                    messagebox.showinfo("Instalación exitosa", "'ifconfig' se ha instalado correctamente. Continuamos con el reinicio de la tarjeta de red...")
                else:
                    messagebox.showerror("Error de instalación", "Ha ocurrido un error durante la instalación de 'ifconfig'.")
                    return

            # Desactivar y luego activar la interfaz de red específica
            subprocess.run(['sudo', '-S', 'ifconfig', interfaz, 'down'], input=contrasena, universal_newlines=True, check=True)
            time.sleep(7)
            messagebox.showinfo("Reinicio de red", "Tarjeta de red apagada correctamente")

            subprocess.run(['sudo', '-S', 'ifconfig', interfaz, 'up'], input=contrasena, universal_newlines=True, check=True)
            time.sleep(7)
            messagebox.showinfo("Reinicio de red", "Tarjeta de red iniciada correctamente")

            # Esperar unos segundos antes de obtener las nuevas direcciones IP
            time.sleep(7)

            # Obtener las nuevas direcciones IP después de reiniciar la tarjeta de red
            informacion = Informacion()
            nueva_ip_local = informacion.obtener_direccion_ip_local()
            nueva_ip_publica = informacion.obtener_direccion_ip_publica()

            # Actualizar las etiquetas con las nuevas direcciones IP
#            etiqueta_ip_local_info.config(text=nueva_ip_local)
#            etiqueta_ip_publica_info.config(text=nueva_ip_publica)

            if callback:
                callback("La tarjeta de red se reinició correctamente.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al reiniciar la tarjeta de red: {e}")

def mostrar_resultado_ping(resultado_ping):
    """
    Muestra el resultado de un comando ping en una nueva ventana de Tkinter.

    Args:
        resultado_ping (str): Resultado del comando ping a mostrar.
    """
    ventana_resultado_ping = tk.Toplevel()
    ventana_resultado_ping.title("Resultado del Ping")

    # Etiqueta para mostrar el resultado del ping
    resultado_label = tk.Label(ventana_resultado_ping, text=resultado_ping, font=("Arial", 12))
    resultado_label.pack(padx=10, pady=10)
    # Aplicar el tema seleccionado a la nueva ventana
    preferencias.cambiar_tema(ventana_resultado_ping, preferencias.tema_seleccionado)
    preferencias.cambiar_tema(resultado_label, preferencias.tema_seleccionado)

def hacer_ping(entry_url):
    """
    Realiza un comando ping a una URL especificada por el usuario y muestra el resultado.

    Args:
        entry_url (tk.Entry): Entrada de Tkinter que contiene la URL para hacer ping.

    Si no se ingresa una URL, muestra un mensaje de error. Si el ping falla, muestra un mensaje de error con el motivo.
    """
    url = entry_url.get()
    if not url:
        messagebox.showerror("Error", "Por favor, ingrese una URL para hacer ping.")
        return
    
    def eliminar_protocolo(url):
        """
        Elimina el protocolo de una URL.

        Args:
            url (str): URL de la que se eliminará el protocolo.

        Retorna:
            str: URL sin el protocolo.
        """
        # Lista de protocolos conocidos
        protocolos = ['http://', 'https://', 'ftp://', 'ftps://', 'sftp://', 'ssh://', 'telnet://', 'smtp://', 'imap://', 'pop3://']

        # Iterar sobre los protocolos y eliminar el primero que coincida con la URL
        for protocolo in protocolos:
            if url.startswith(protocolo):
                return url[len(protocolo):]  # Eliminar el protocolo de la URL

        # Si no se encuentra ningún protocolo conocido, devolver la URL sin cambios
        return url

    try:
        url_sin_protocolo = eliminar_protocolo(url)
        resultado = subprocess.run(['/bin/ping', '-c', '4', url_sin_protocolo], capture_output=True, text=True, timeout=10)
        resultado_ping = resultado.stdout
        mostrar_resultado_ping(resultado_ping)
    except subprocess.TimeoutExpired:
        messagebox.showerror("Error", "Tiempo de espera de ping agotado. No se recibió respuesta.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al hacer ping a la URL: {e}")

class RedTools:
    def __init__(self, root):
        """
        Inicializa la clase RedTools.

        Args:
            root: El widget raíz de Tkinter.
        """
        self.root = root
        self.area_central = None

    def set_area_central(self, area_central):
        """
        Establece el área central donde se mostrarán las herramientas relacionadas con la red.

        Args:
            area_central: El área central de la interfaz gráfica de Tkinter.
        """
        self.area_central = area_central

    def escanear_puertos(self, ip):
        """
        Realiza un escaneo de puertos en una dirección IP específica.

        Args:
            ip (str): La dirección IP a escanear.
        """
        def realizar_escaneo():
            """
            Función interna para realizar el escaneo de puertos.
            """
            resultado_text.delete('1.0', tk.END)
            try:
                ip = entry_ip.get()
                for puerto in range(1, 1025):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.5)
                    resultado = s.connect_ex((ip, puerto))
                    if resultado == 0:
                        resultado_text.insert(tk.END, f"Puerto {puerto}: Abierto\n")
                    s.close()
            except Exception as e:
                resultado_text.insert(tk.END, f"Error: {e}\n")

        self.limpiar_area_central()
        tk.Label(self.area_central, text="Escaneo de Puertos", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(self.area_central, text="Introduce la IP a escanear:", font=("Arial", 12)).pack(pady=5)
        entry_ip = tk.Entry(self.area_central, width=30)
        entry_ip.pack(pady=5)
        tk.Button(self.area_central, text="Escanear", command=realizar_escaneo).pack(pady=10)
        resultado_text = tk.Text(self.area_central, height=20, width=80)
        resultado_text.pack(pady=10)

    def test_velocidad(self):
        """
        Realiza un test de velocidad de Internet.
        """
        def realizar_test():
            resultado_text.delete('1.0', tk.END)
            st = speedtest.Speedtest()
            st.download()
            st.upload()
            resultados = st.results.dict()
            resultado_text.insert(tk.END, f"Velocidad de descarga: {resultados['download'] / 1_000_000:.2f} Mbps\n")
            resultado_text.insert(tk.END, f"Velocidad de carga: {resultados['upload'] / 1_000_000:.2f} Mbps\n")
            resultado_text.insert(tk.END, f"Ping: {resultados['ping']} ms\n")

        self.limpiar_area_central()
        tk.Label(self.area_central, text="Test de Velocidad de Internet", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(self.area_central, text="Iniciar Test", command=realizar_test).pack(pady=10)
        resultado_text = tk.Text(self.area_central, height=20, width=80)
        resultado_text.pack(pady=10)

    def diagnostico_red(self):
        """
        Realiza un diagnóstico de la red.
        """
        def realizar_diagnostico():
            resultado_text.delete('1.0', tk.END)
            try:
                # Verificar si traceroute está instalado
                if not shutil.which("traceroute"):
                    raise Exception("El comando 'traceroute' no está instalado. Por favor, instálalo e inténtalo de nuevo.")

                # Verificar si netstat está instalado
                if not shutil.which("netstat"):
                    raise Exception("El comando 'netstat' no está instalado. Por favor, instálalo e inténtalo de nuevo.")

                # Ejecutar traceroute
                resultado_text.insert(tk.END, "Traceroute:\n")
                traceroute = subprocess.Popen(['traceroute', 'www.google.com'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                for line in iter(traceroute.stdout.readline, b''):
                    resultado_text.insert(tk.END, line.decode())

                # Ejecutar netstat
                resultado_text.insert(tk.END, "\nNetstat:\n")
                netstat = subprocess.Popen(['netstat', '-tuln'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                for line in iter(netstat.stdout.readline, b''):
                    resultado_text.insert(tk.END, line.decode())
            except Exception as e:
                resultado_text.insert(tk.END, f"Error: {e}\n")

        self.limpiar_area_central()
        tk.Label(self.area_central, text="Diagnóstico de Red", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(self.area_central, text="Iniciar Diagnóstico", command=realizar_diagnostico).pack(pady=10)
        resultado_text_frame = tk.Frame(self.area_central)
        resultado_text_frame.pack(pady=10)
        resultado_text = scrolledtext.ScrolledText(resultado_text_frame, height=20, width=80, wrap=tk.NONE)
        resultado_text.pack(expand=True, fill=tk.BOTH)

    def limpiar_area_central(self):
        for widget in self.area_central.winfo_children():
            widget.destroy()
            
