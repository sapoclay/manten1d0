## Manten1d0: Mantenimiento básico de Ubuntu
![about-manten1d0](https://github.com/sapoclay/manten1d0/assets/6242827/d05e63db-ec27-4448-8ab9-5394d018b893)
------------------------------------------------------------------
* Manten1d0: Sistema de mantenimiento básico y otras cosas para Ubuntu. 
* Creado con: Python 3.10.12
* Versión actual del programa: 0.5.3
* Probado en: Ubuntu 22.04
------------------------------------------------------------------
### Cosas que puede ir haciendo 
------------------------------------------------------------------
![password-manten1d0](https://github.com/sapoclay/manten1d0/assets/6242827/c45a7157-1cf4-42bc-86da-54db4e03c69e)

- Añadida la capacidad de almacenar de forma cifrada la contraseña del usuario, para solo tener que escribirla una única vez, cuando se inicia el programa. Esta debe ser la contraseña del usuario, y debe tener permisos para utilizar sudo.

![comprobando-dependencias](https://github.com/sapoclay/manten1d0/assets/6242827/f8f7487e-7973-4741-ac72-90734b35a9c4)

- Se comprueban las dependencias necesarias al iniciar el programa. Si falta alguna de las dependencias que se pueden ver en el listado de dependencias instalables que hay más abajo, el programa debería instalarlas de manera automática para terminar iniciandose. En caso de que todas las dependencias estén instaladas, nos mostrará un aviso y se iniciará el programa.

![interfaz-manten1d0](https://github.com/sapoclay/manten1d0/assets/6242827/1ba8b27c-d0fa-492e-85a6-282bde3828c0)

- Tras iniciarse el programa, veremos una interfaz de usuario sencilla. Consta de un menú lateral que mostrará todas las opciones que incluye cada categoría en la parte central de la interfaz. Además tendremos algunas opciones en el menú superior de la interfaz.
  
![informacion-sistema](https://github.com/sapoclay/manten1d0/assets/6242827/417f2df7-cd5f-47f3-83df-81dbacb9b45d)

- En la categoría Información, dispondremos de alguna información sobre el sistema operativo que estemos utilizando. También nos mostrará información sobre las tarjetas de red, ip, dns, etc e información el procesador y la memoria de nuestro equipo.
  
![opcion-sistema](https://github.com/sapoclay/manten1d0/assets/6242827/682c8fbf-d36b-47d8-b119-35d07ce4142d)

- En la opción Sistema, veremos difernetes botones. Cada uno de ellos nos dará la posibilidad de realizar diferentes operaciones sobre el sistema. Para saber más sobre qué hace cada uno de los botones, solo tendremos que pasar el ratón por encima, y el tooltip nos dará una explicación de qué podremos hacer con esa opción en particular.
  
![opcion-internet](https://github.com/sapoclay/manten1d0/assets/6242827/ba3f444c-ac31-4312-8409-23bc3cd18f15)

- La opción Internet nos va a dar la posibilidad de reiniciar la tarjeta de red que seleccionemos el desplegable que tenemos disponible. Además también nos dará la posibilidad de hacer ping a la URL que escribamos en la caja de texto dedicada a ello.
  
![limpiar-cache-navegadores](https://github.com/sapoclay/manten1d0/assets/6242827/09945015-7160-4dc0-97e3-3bfee1df548c)

- La categoría Navegadores nos va a dar la posibilidad de limpiar la caché de los navegadores. Si están disponibles en el sistema, claro está.
  
![diccionario](https://github.com/sapoclay/manten1d0/assets/6242827/8f41ebb9-9250-49f9-807e-545cb1f86eda)

- En la última categoría disponible (por el momento), tenemos disponible la opción de Diccionario. Esta abrirá una ventana nueva con el diccionario que se va a cargar desde una URL predefinida. Este diccionario nos dará la posibilidad de buscar contenido dentro del archivo .MD que tengamos abierto, y nos dará también la posibilidad de abrir un archivo .MD que nosotros queramos. Otra opción que nos dará la ventana del diccionario, será la de abrir una terminal para probar alguno de los comandos que se pueden consultar en el diccionario.
  
![tema-oscuro](https://github.com/sapoclay/manten1d0/assets/6242827/9cf5c903-c237-4a53-a5ba-5203e0a02236)

- En las opciones del programa, encontraremos la posibilidad de cambiar entre un tema oscuro y uno claro, y también nos dará la posibilidad de aumentar el tamaño del texto.
- En el menú preferencias, también encontraremos la posibilidad de buscar actualizaciones de forma automática del programa.
- También tendremos la posibilidad de abrir en el navegador por defecto del sistema operativo la URL que escribamos. Esta opción la encontraremos disponible en el menú superior en la opción Archivo.

## Actualización Versión 0.5.1

- Añadidas al menú principal las opciones de eliminar archivos y carpetas o vaciar la papelera de reciclaje.
- Añadida al menú principal la opción Buscar actualizaciones.

## Actualización Versión 0.5.2

- Añadida la opción de buscar archivos duplicados dentro de una carpeta con permisos suficientes. Esto se hace mediante el calculo del hash de cada archivo utilizando SHA-256. Si coincide con el de otros archivos, se determina que son iguales. Esta opción muestra el archivo original y los archivos iguales. Además permite seleccionar todos los archivos que aparecen en el listado y se incluye también un botón para eliminar solo los archivos seleccionados. El listado de archivos duplicados encontrados permite el scroll utilizando la rueda del ratón o el teclado.
- Se ha añadido también la posibildida de hacer doble clic sobre alguno de los archivos seleccionados y que se abra la ubicación del archivo utilizando el gestor de archivos nautilus.
- Todos los botones cuentan ahora con un Tooltip a modo explicativo.
  
## Actualización Versión 0.5.3

- He cambiado la estructura del programa. Ahora dispone de un menú lateral vertical desde donde movernos por las categorías. Dentro de cada categoría se mostrarán las subcategorías que cada categoría incluya.
- Se ha añadido dentro de la categoría Internet la posibilidad de hacer ping a URL.
- Ahora dispone de opciones para cambiar el tema del programa entre un tema claro y otro oscuro. También permite cambiar el tamaño de la fuente de todo el programa.
- Añadida la opción Abrir URL en el Navegador en la opción Archivo del menú superior del programa.
- Se ha añadido la opción de monitorizar el sistema. Esta se presenta con un grafico de la monitorización del momento en el que se presiona el botón.
- He corregido el tooltip. Ahora cuando el usuario hace clic en un botón, el tooltip desaparece de manera correcta.
- Añadida la opción de limpiar el historial de los navegadores (Chrome, Firefox y Edge)
- Se ha corregido el error de python3-tk. Ya que antes si no estaba instalado rompía la ejecución del programa. Ahora se instala de manera automática si falla la importación al iniciar el programa. Una vez terminada la instalación de este paquete, continúa la ejecución normal del programa.
- Añadida la opción para realizar copias de seguridad de carpetas. Se va a crear un archivo .gz en la carpeta que indiquemos. Se utiliza tar para este proposito. También dispone de la opción para restaurar los archivos de la copia de seguridad.
- Añadida la opción para cifrar archivos. Se utiliza ChaCha20 para el cifrado y para el descifrado.

## Dependencias Imprescindibles 

Dependencias necesarias para poder ejecutar el programa. Estas dependencias deben instalarse manualmente.

- Python3 -> sudo apt install python3.10
- pip3 -> sudo apt install python3-pip

## Dependencias instalables

Estas dependencias las comprobará e instalará el programa una vez se ejecute si no las encuentra disponibles en el sistema.

- samba -> sudo apt install samba
- nmap -> sudo apt install python3-nmap
- python3-tk -> sudo apt install python3-tk
- nautilus -> sudo apt install nautilus
- Tkinter -> sudo apt install python3-tk
- Net-tools -> sudo apt install net-tools
- Pyqt5 -> sudo apt install python3-pyqt5
- Gnome-terminal -> sudo apt install gnome-terminal
- smartmontools -> sudo apt install smartmontools
- Matplotlib -> pip3 install matplotlib
- Pillow -> pip3 install --upgrade pillow
- Cryptography -> pip3 install cryptography
- psutil -> pip3 install psutil 
- markdown2 -> pip3 install markdown2
- PyQt5 -> pip3 install PyQt5
- ethtool -> sudo apt install ethtool
- speedtest-cli -> pip3 install speedtest-cli
- tabulate -> pip3 install tabulate
- opencv-python-headless -> pip3 install opencv-python-headless
- wget -> pip3 install wget
- Tooltip -> pip3 install Tooltip
- Fernet -> pip3 install Fernet


## Instalación del paquete .DEB

- En una terminal (Ctrl+Alt+T):

  ``` sudo dpkg -i Manten1d0.deb ```

Tras la instalación deberías poder ver ya el lanzador del programa en el menú de Actividades.

![lanzador](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/1b0a026c-5cd9-4bc1-aca0-f9e2787d9d27)

## Desinstalación

- Eliminaremos el programa escribiendo en una terminal (Ctrl+Alt+T):

``` sudo apt remove manten1d0 ```

- Para no dejar rastro alguno del programa en tu equipo, en la misma terminal será necesario escribir:
  
``` sudo rm -rf /usr/share/Manten1d0/ ```
