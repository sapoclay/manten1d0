## Manten1d0: Mantenimiento básico de Ubuntu
![Manten1d0](https://github.com/sapoclay/manten1d0/assets/6242827/358bb3c2-d0af-4f07-a592-dcee7b1ed1a0)
------------------------------------------------------------------
* Manten1d0: Sistema de mantenimiento básico y otras cosas para Ubuntu. 
* Creado con: Python 3.10.12
* Versión actual del programa: 0.5.7
* Probado en: Ubuntu 22.04
------------------------------------------------------------------
### Cosas que puede ir haciendo 
------------------------------------------------------------------
![password-manten1d0](https://github.com/sapoclay/manten1d0/assets/6242827/c45a7157-1cf4-42bc-86da-54db4e03c69e)

- Añadida la capacidad de almacenar de forma cifrada la contraseña del usuario, para solo tener que escribirla una única vez, cuando se inicia el programa. Esta debe ser la contraseña del usuario, y debe tener permisos para utilizar sudo.

![comprobando-dependencias](https://github.com/sapoclay/manten1d0/assets/6242827/f8f7487e-7973-4741-ac72-90734b35a9c4)

- Se comprueban las dependencias necesarias al iniciar el programa. Si falta alguna de las dependencias que se pueden ver en el listado de dependencias instalables que hay más abajo, el programa debería instalarlas de manera automática para terminar iniciandose. En caso de que todas las dependencias estén instaladas, nos mostrará un aviso y se iniciará el programa.

![interfaz](https://github.com/sapoclay/manten1d0/assets/6242827/80f57daf-97a6-4212-b1c0-da5c61a64000)

- Tras iniciarse el programa, veremos una interfaz de usuario sencilla. Consta de un menú lateral que mostrará todas las opciones que incluye cada categoría en la parte central de la interfaz. Además tendremos algunas opciones en el menú superior de la interfaz.
  
![info-SO](https://github.com/sapoclay/manten1d0/assets/6242827/729081ad-5f20-4911-9fe7-cc1b31495942)

- En la categoría Información, dispondremos de alguna información sobre el sistema operativo que estemos utilizando. También nos mostrará información sobre las tarjetas de red, ip, dns, etc e información el procesador y la memoria de nuestro equipo.
  
![sistema](https://github.com/sapoclay/manten1d0/assets/6242827/d8a4cb09-9b22-4489-80f7-6a130af56b7b)

- En la opción Sistema, veremos difernetes botones. Cada uno de ellos nos dará la posibilidad de realizar diferentes operaciones sobre el sistema. Para saber más sobre qué hace cada uno de los botones, solo tendremos que pasar el ratón por encima, y el tooltip nos dará una explicación de qué podremos hacer con esa opción en particular.
  
![opcion-internet](https://github.com/sapoclay/manten1d0/assets/6242827/ba3f444c-ac31-4312-8409-23bc3cd18f15)

- La opción Internet nos va a dar la posibilidad de reiniciar la tarjeta de red que seleccionemos el desplegable que tenemos disponible. Además también nos dará la posibilidad de hacer ping a la URL que escribamos en la caja de texto dedicada a ello.
  
![navegadores](https://github.com/sapoclay/manten1d0/assets/6242827/dc6c5b5b-dfc0-4979-8af9-0e5dab6f6a40)

- La categoría Navegadores nos va a dar la posibilidad de limpiar la caché de los navegadores. Limpiar la caché de los navegadores, y también tendremo la posibilidad de instalar Chrome, Firefox o Edge de forma desatendida.
  
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
- Se ha añadido también la posibilididad de hacer doble clic sobre alguno de los archivos seleccionados y que se abra la ubicación del archivo utilizando el gestor de archivos nautilus.
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
![opciones-archivos](https://github.com/sapoclay/manten1d0/assets/6242827/f0d64f77-03b9-40d9-91bf-9c3c2a9c2c5d)
- Añadida la opción para realizar copias de seguridad de carpetas. Se va a crear un archivo .gz en la carpeta que indiquemos. Se utiliza tar para este proposito. También dispone de la opción para restaurar los archivos de la copia de seguridad.
- Añadida la opción para cifrar archivos. Se utiliza ChaCha20 para el cifrado y para el descifrado.

## Actualización Versión 0.5.4

- Añadidas las funcionalidades "Escenear Puertos", "Test Velocidad" y "Diagnóstico Red" a la categoría Internet.

## Actualización Versión 0.5.5

- Corregido y optimizado el sistema de actualización del programa.
- Simplificado el sistema de comprobación de dependencias para instalar las dependencias con pip3 y con APT. Ahora las dependencias de pip3 se establecen en el archivo requierements.txt y las dependencias APT se establecen en el diccionario del archivo dependencias.py.
- Modificados los permisos del archivo config.ini para su lectura desde el archivo .deb.
- Añadidas funcionalidades para modificar el perfil de usuario del sistema (requiere que el usuario tenga privilegios de sudo). Por el momento solo permite modificar el nombre de usuario, la contraseña y la fotografía de perfil.
- La categoría Sistema ahora ofrece la posibilidad de seleccionar un archivo .deb e instalarlo utilizando dpkg.
![desinstalar](https://github.com/sapoclay/manten1d0/assets/6242827/06dfeed0-a1f2-428d-b461-a3b812392876)
- Añadida la posibilidad de desinstalar los paquetes snap y deb instalados por el usuario. En la ventana de desinstalación se ha añadido un cuadro de búsqueda dinámico para buscar el paquete a desinstalar.
- También se ha añadido la opción para abrir el repositorio en GitHub del proyecto desde el menú superior, opción Preferencias.
![conexion-internet](https://github.com/sapoclay/manten1d0/assets/6242827/2c714f02-b0e9-4106-9c61-2dc2e1a441c9)
- Se ha añadido información sobre la conexión a internet en el menú lateral. En la parte inferior aparecerá una etiqueta en verde cuando la conexión a internet esté activa. Si en algún momento se pierde la conexión, esta etiqueta pasará a rojo y el texto cambiará a "Sin conexión".
- Acabo de añadir la opción de instalación de los navegadores más típicos (Firefox, Chrome y Edge). Esta opción de instalación aparece en la categoría Navegadores.
- Reparados los errores en la gestión de los repositorios.
- Corrección de errores menores.

## Actualización Versión 0.5.6
- Añadido un editor de texto básico para tomar notas. Permite trabajar con archivos .md y .txt. Se han añadido opciones al menú contextual del ratón dentro del editor básico. El editor cuenta palabras y caracteres. Permite búsqueda, con resaltado de resultados.
- Corrección de ToolTips.
- Ahora se muestra la información de la tarjeta gráfica utilzando lspci y lshw. Además se usa nvidia-smi (si está disponible) para calcular la temperatura y la memoria disponible en la tarjeta. Si la tarjeta no es nvidia, los datos no se mostrarán correctamente (es que todas mis tarjetas son nvidia XD )
- Reparados los errores que se producían en la instalación de paquetes .DEB cuando no se selecciona un archivo para instalar.
- Optimizado el test de velocidad de la conexión a internet, el diagnóstico de red y el escaner de puertos.
- Añadidos botones para abrir los navegadores web (Firefox, Chrome o Edge)
- También se han añadido botones para abrir los navegadores (Firefox, Chrome o Edge) en modo incógnito.
- En la red local, ahora el programa detecta automáticamente la red local. Ya no tiene por que ser 192.168.x.x. Por el momento la conexión debe realizarse entre equipos con Samba instalado. Se utiliza nautilus para abrir las carpetas compartidas.
- Añadidos valores numéricos a la monitorización del sistema.
- Otras correcciones a la hora de gestionar el cierre de la aplicación.

## Actualización Versión 0.5.7
![logs](https://github.com/sapoclay/manten1d0/assets/6242827/2e742038-8c1d-4de6-9aa8-c3639ba54f38)
- Añadida la consulta de logs del sistema a la opción "Sistema".
- Se ha añadido a la sección "Archivos", la posibilidad de buscar en todo el sistema de manera recursiva archivos. En la lista de archivos encontrados, si se hace doble clic sobre uno de los archivos, se abrirá el gestor de archivos nautilus en la carpeta en la que se encuentre el archivo seleccionado. Además acepta la búsqueda utilizando * o ?.
![renombrar-archivos](https://github.com/sapoclay/manten1d0/assets/6242827/49915632-ad65-4238-8d76-cf4ceb15a230)
- He añadido la opción de renombrado masivo en la sección "Archivos". Con ella bastará con seleccionar la carpeta que incluye los archivos. Después no hay más que escribir el prefijo que se le quiere dar a totos los archivos, y tras pulsar el botón renombrar, se cambiará el nombre a todos los archivos utilizando el prefijo escrito y un número incremental. También nos permitirá ver con nautilus la carpeta que seleccionemos con los archivos a renombrar.

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
- traceroute -> sudo apt install traceroute
- pciutils -> sudo apt-get install pciutils
- lshw -> sudo apt-get install lshw
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
- py3nvml -> pip3 install py3nvml


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
