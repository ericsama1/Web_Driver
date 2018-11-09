# Web_Driver


Se crea el Web_Driver para facilitar el uso de selenium, creando metodos 
que no estan por defecto en el driver de selenium. Obtener una imagen 
de un sitio web, convertir en pdf la pagina actual, etc.


## Instalacion de los elementos

Para utilizar el Web_Driver, se necesita instalar ciertos paquetes: 
- Selenium `sudo pip install selenium`
- PIL `sudo pip install pil`
- Pdfkit `sudo pip install pdfkit`
- chromedriver, download from `http://chromedriver.chromium.org/downloads` 
- Geckodriver, download from `https://github.com/mozilla/geckodriver/releases`
- operachromiumdriver, download from `https://github.com/operasoftware/operachromiumdriver/releases`

## Setear parametros

### settings.py

En este archivo pondremos las settings que nosotros utilizaremos en este caso,
tenemos las opciones de pdf y el path del log

- `pdf_option`: en esta variable, se asigan el formato del pdf que se quiere utilizar. Por 
defecto esta en modo `page-size: A4` y `encoding: UTF-8`
- `LOG_FILE`: es el path del archivo log que se va a utilizar, por default esta como 
`web_driver.log`

Tambien se importaran settings que sean locales con el archivo `settings_local.py`

### settings_local.py

En esta setting, asignaremos los path de los driver de los browser que se utilizaran.
Esta setting se ignora en el git, y solo funcionara con las settings locales que se ingresan.
Se muesta un ejemplo de como se tiene que asignar el path de los driver
- `path_chromedriver = /home/user/Download/chromedriver`
- `path_firefoxdriver = /home/user/Download/geckodriver`
- `path_operadriver = /home/user/Download/operadriver`
- `opera_binary_location = /usr/bin/opera`

## Como utilizar

Una de las ventajas que presenta este driver, es la posibilidad de utilizar metodos
los mismos metodos para diferentes browsers. Por el momento, se puede utlizar en 
`Google Chrome`, `Mozilla Firefox` y `Opera`.

### Inicializar el driver

El init del driver esta compuesto por lo siguiente:

![](/Images/driver_init.jpg)

Por defecto los valores del driver se muestran en Falso o con valores nulos, y el browser
que se utiliza por defecto será `Google Chrome`.
 - `browser`: se le asignará el nombre del browser que se quiere utilizar, los nombres de estos 
 se encuentran en `constants/constants.py` como `CHOME`, `FIREFOX` y `OPERA`
 - `device`: este parametro es para utilizar la emulación de la interfaz de un dispositivo 
 móvil. Los nombres de los dispositivos que se pueden emular, se encuentran en `constants/constants.py` como un array en `DEVICE_ARRAY`
 - `headless`: para este parametro se utiliza `True/False`, es para habilitar el modo headless,
 y que el browser trabaje en background
 - `size`: para este parametro hay que pasar un diccionario con `width` y `height`

Tambien se documenta que todas las acciones que realice el driver, 
en el log `web_driver.log`.

Todos los browser son compatibles con los metodos que se encuentra en la
libreria, lo unico que difiere son los argumentos que se pasan por
argumento al iniciar el browser.