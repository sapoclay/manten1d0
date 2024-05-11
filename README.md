## Mantenimiento básico de Ubuntu

------------------------------------------------------------------
![about](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/24750aa9-a9ff-4381-b8f0-d5200a6417b4)
* Sistema de mantenimiento básico y otras cosas para Ubuntu. 
* Creado con Python 3.10.12
* Versión actual del programa: 0.5.1
------------------------------------------------------------------
### Cosas que puede ir haciendo 
------------------------------------------------------------------
![actualizar-sistema](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/5d39287a-bba0-483d-bb07-95664f14c4f7)
- Actualizar paquetes del sistema.
- Instalación desde gestor de software (tienda snap).
- Limpiar caché del sistema.
![repositorios](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/61d46859-7c52-43bb-b1ee-28006e825769)
- Opción para trabajar con los repositorios instalados en el sistema (eliminar/editar/añadir). Todos los cambios se harán en el archivo source.list, pero se hará una copia de seguridad antes de realizar algún cambio en el archivo. La ubicación de la copia de seguridad será /etc/apt/sources.list.bak (esto todavía está en proceso por lo que puede fallar o no hacer lo que se espera)
![reiniciar-tarjeta-red](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/0b46dd7a-c9bd-4fff-afd9-6250f444d8c7)
- Reiniciar tarjetas de red.
- Incluye un menú Archivo y About con los que se puede interactuar a gole de clic.
  ![add-password](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/9fff8fbe-7fb4-4eb8-9dec-640161bdfc3e)
- Añadida la capacidad de almacenar de forma cifrada la contraseña del usuario, para solo tener que escribirla una única vez. Esta debe ser la contraseña del usuario, y debe tener permisos para utilizar sudo.
- Añadida la identificación del sistema (Ubuntu), Kernel, usuario, entorno gráfico, Ip pública, Ip Local, DNS local y DNS publicos, etc ...
![monitorizar-sistema](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/d022bcd4-aabc-4694-80f0-1b1781a7dbbf)
- Añadida la monitorización del sistema con visualización en un gráfico con Tkinter y Matplotlib.
![procesos](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/0481cf35-0e5d-4451-bb1f-24e02d321179)
- Permite ver y ordenar los procesos del sistema, aun que el consumo de CPU se reduce al momento en el que se inicia este administrador de procesos. Se añade un buscador por nombre o PID para poder buscar el proceso que quieres cerrar con el botón creado para ello.
![aplicaciones-al-inicio](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/2693e8e4-d0d8-4966-845a-ad5c88d67be5)
- Añadida la posibilidad de ver/añadir o eliminar las aplicaciones que se inician con el sistema.
- Añadida la posibilidad de limpiar la caché de navegadores como Firefox, Chrome y Edge.
![diccionario](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/03cb7c72-960b-4627-8f7d-cee72dcd9fe9)
- Añadida la opción de diccionario en el menú Archivo. Este diccionario es obtenido de un archivo .md. El diccionario permite buscar entre todo su contenido. En la ventana del diccionario se ha añadido un menú desde el que el usuario podrá cargar archivos markdown para poder realizar consultas. El menú de esta ventana incluye también una opción para volver a cargar el diccionario por defecto, una opciń para cerrar el diccionario y la opción de abrir la terminal por defecto de Ubuntu (gnome-terminal).
- Se ha añadido la posibilidad de ver el hardware del equipo (procesador, grafica, tarjetas de red, etc ...)
![comprobacion-dependencias](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/6e7f41cc-0d98-43db-83ae-a22bba4f9ff3)
- Para simplificar las cosas, al incio del programa se comprueba si la lista de dependencias que se muestra aquí debajo se cumple. Si no se cumple se procede a su instalación antes de intentar arrancar el programa.
![iplocales](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/c5e8cc72-83d3-4dd6-a2dc-fd08f299cfce)
- Se ha añadido la localización de equipos en la misma red. Dentro del listado de equipos obtenidos, tendremos la posibilidad de abrir con nautilus, si los permisos y el firewall lo permiten. Para esto se utiliza el protocolo samba, por lo que es necesario que esté instalado en el equipo con el que queremos conectarnos. En el equipo en el que se ejecute este script se instalará samba como dependencia.

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
  
## Dependencias Imprescindibles 

Dependencias necesarias para poder ejecutar el programa. Estas dependencias deben instalarse manualmente.

- Python3 -> sudo apt install python3.10
- pip3 -> sudo apt install python3-pip

## Dependencias instalables

Estas dependencias las comprobará e instalará el programa una vez se ejecute si no las encuentra disponibles en el sistema.

- samba -> sudo apt install samba
- nmap -> sudo apt install python3-nmap
- nautilus -> sudo apt install nautilus
- Tkinter -> sudo apt install python3-tk
- Net-tools -> sudo apt install net-tools
- Pyqt5 -> sudo apt install python3-pyqt5
- Gnome-terminal -> sudo apt install gnome-terminal
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


## Instalación del paquete .DEB

- En una terminal (Ctrl+Alt+T):

  ``` sudo dpkg -i mantenimientobasico.deb ```

Tras la instalación deberías poder ver ya el lanzador del programa en el menú de Actividades.

![lanzador](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/1b0a026c-5cd9-4bc1-aca0-f9e2787d9d27)

## Desinstalación

- En una terminal (Ctrl+Alt+T):

``` sudo apt remove mantenimientobasico ```
