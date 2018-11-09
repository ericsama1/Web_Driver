# Web_Driver


Se crea el Web_Driver para facilitar el uso de selenium, creando metodos 
que no estan por defecto en el driver de selenium. Obtener una imagen 
de un sitio web, convertir en pdf la pagina actual, etc.


## Instalacion de los elementos

Para utilizar el Web_Driver, se necesita instalar ciertos paquetes: 
- Selenium `sudo pip install selenium`
- PIL `sudo pip install pil`
- Pdfkit `sudo pip install pdfkit`
- chromedriver, download from http://chromedriver.chromium.org/downloads
- Geckodriver, download from https://github.com/mozilla/geckodriver/releases
- operachromiumdriver, download from 
https://github.com/operasoftware/operachromiumdriver/releases

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
 móvil. Los nombres de los dispositivos que se pueden emular, se encuentran en 
 `constants/constants.py` como un array en `DEVICE_ARRAY`
 - `headless`: para este parametro se utiliza `True/False`, es para habilitar el modo headless,
 y que el browser trabaje en background
 - `size`: para este parametro hay que pasar un diccionario con `width` y `height`
 - `incognito`: este paramatro se puede utilizar para habilitar el modo headless del browser, 
 este se habilita con `True/False`
 - `command`: este parametro se utiliza para ingresar manualmente algun parametro para el 
 browser
 - `position`: parametro para posicion la ventana en una coordenada deseada, utiliza un 
 diccionario con `X` e `Y`
 - `fullscreen`: parametro para habilitar el modo fullscreen del navegador, se habilita con
 `True` o `False`

 ### Metodos dentro del driver

 - `close()`: cierra el navegador
 - `url(string)`: se habre el navegador con la url ingresada en el string
 - `search_ids(by, value)`: se devuelven los nombres de los id buscados con el parametro by y value
 - `buscar_error()`: se busca si se esta mostrando algun mensaje de erro
 - `is_visible(by, value)`: Se verifica si un elemento se encuentra visible
 - `is_enabled(by, value)`: Se verifica si un elemento se 
 encuentra habilitado
 - `get_text(by, value)`. Se obtiene el texto que esta dentro
 del elemento buscado por by y value
 - `check_box(by, value, class_name)`: Se verifica que los elementos del class_name se encuentren dentro del elemento buscado por by y value
 - `get_box(by, value, element)`: Se obtiene las coordenadas que se encuentra el elemento buscado por by y value; tambien se lo puede buscar como un webelement
 - `get_size(by, value)`: devuelve el tamaño del elemento buscado por by y value. Se devuelve el valor en un formato de diccionario con `width` y `height`
 - `get_location(by, value)`: Devuelve las coordenadas del elemento buscado por by y value
 - `send_text_to_input(by, value, text)`: metodo que se utiliza para ingresar un texto en un elemento que se busca por by y value. Si el elemento buscado, es un input de contraseña, no queda registrado el texto en el log
 - `send_enter_key(by, value)`: metodo para ingresar la tecla enter en un input
 - `click(by, value)`: se hace click sobre el elemento que se busca por by y value
 - `click_by_text(text, tagname)`: se hace una busqueda con xpath para obtener todos los elementos que contengan el texto ingresado. El tagname se utiliza para filtrar los elementos busados.
 - `select_by_text(by, value, valor)`: metodo que se utiliza para seleccionar una opcion de un select que se busca por by y value.
 - `select_random(by, value)`: selecciona, de manera aleatoria, una opcion dentro del select que se busca por by y value
 - `select_by_index(by, value, index)`: selecciona la opcion que se encuentra en la posicion que se pasa por la variable index, del select que se busca por by y value
 - `select_by_value(by, value, select_value)`: metodo que se utiliza para seleccionar una opcion del select utilizando el value de la opcion
 - `get_select_option(by, value)`: devuelve todas las opciones dentro del select que se busca
 - `check(value)`: metodo para marcar un checkbox, se busca por id
 - `search_elem(by, value)`: metodo para utilizar para ver si un elemento esta visible y habilitado
 - `tabs()`: devuelvo el nombre de las tabs que se encuentran abiertos, en forma de array
 - `change_tab(windows_name)`: metodo para cambiar de pestaña. El parametro windows_name se tiene que utilizar en conjunto de tabs()
 - `new_tab(url)`: se utiliza para abrir una nueva pestaña con la url ingresada
 - `close_tab()`: se cierra la pestaña activa y deja activa la primera de todas
 - `execute_script(script)`: ejecuta una funcion javascript que se ingresa por parametro
 - `screenshot(path)`: hace una captura de pantalla de la pantalla actual del browser, y se lo guarda en el path ingresado
 - `elem_screenshot(by, value, path)`: se hace una captura de pantalla donde se muestre el elemento buscado, y se guarda en el path ingresado
 - `element_to_png(by, value, dirname)`: se hace una captura de pantalla de sólo el elemento buscado. Si el elemento que se quiere hacer la captura es mas grande que la ventana del browser, se trata de capturar en su totalidad
 - `get_image(by, value, dirname)`: se descarga la imagen que se busca.
 - `mouse_over(by, value)`: metodo para posicion el mouse sobre un elemento. Si el elemento se encuentra fuera de la ventana actual del browser, se desplaza automaticamente hasta el elemento.
 - `double_click(by, value)`: se hace doble click sobre el elemento que se busca
 - `mouse_scroll(bu, value, horizontal, vertical)`: se hace scroll sobre el elemento buscado. Las variables `horizontal` y `vertical` son la cantidad de pixelces que se quiere desplazar en ese sentido
 - `get_attibute(by, value, attribute)`: metodo que devulve el atributo de un elemento que se busca
 - `clear(by, value)`: limpia el input buscado
 - `clear_all()`: limpia todos los input que hay en la pagina
 - `alert_confirm()`: confirma una alerta
 - `alert_dismmis()`: rechaza una alerta
 - `input_alert(text)`: se escribe el string que se pasa por la variable text al input de la alerta
 - `back()`: regresa una pagina anterior del historial
 - `foward()`: metodo para adelantar una pagina en el historial
 - `set_windows_size(size)`: metodo para setear el tamaño de la ventana con la cual se quiere trabajar
 - `get_windoes_size()`: devuelve el tamaño actual del browser
 - `maximize_windows()`: metodo para maximizar la ventana de la aplicacion
 - `to_pdf(dirname, option)`: metodo para descargar una pagina en formato pdf. Se tiene que ingresar la forma para guardar, ya sea con el html de la pagina o la url
 - `get_html()`: devuelvo el codigo html de la pagina actual
 - `get_url()`: devuelvo la url actual

Cada accion del driver, se veran reflejadas en el log que se setea en `settings`


Todos los browser son compatibles con los metodos que se encuentra en la
libreria, lo unico que difiere son los argumentos que se pasan por
argumento al iniciar el browser.