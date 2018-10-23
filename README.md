# Web_Driver


Se crea el Web_Driver para facilitar el uso de selenium, creando metodos 
que no estan por defecto en el driver de selenium. Obtener una imagen 
de un sitio web, convertir en pdf la pagina actual, etc.

Para utilizar el Web_Driver, se necesita instalar ciertos paquetes: 
- Selenium `sudo pip install selenium`
- PIL `sudo pip install pil`
- Pdfkit `sudo pip install pdfkit`
- chromedriver, download from `http://chromedriver.chromium.org/downloads` 
- Geckodriver, download from `https://github.com/mozilla/geckodriver/releases`
- operachromiumdriver, download from `https://github.com/operasoftware/operachromiumdriver/releases`

Tambien se precisa asignar en el `settings.py` o en el `settings_local.py` 
el `path_chromedriver`, el `path_firefoxdriver` y el `path_operadriver` en 
el correspondiente path de los driver descargados. Tambien, se le debe 
asignar a `opera_binary_location` la direccion del ejecutable de opera, para 
poder usarlo.

Por ejemplo: 
- `path_chromedriver = /home/user/Download/chromedriver`
- `path_firefoxdriver = /home/user/Download/geckodriver`
- `path_operadriver = /home/user/Download/operadriver`
- `opera_binary_location = /usr/bin/opera`

Para un mejor manejo, se puede utilizar el mismo driver para levantar una 
pagina web con el browser de firefox u opera. El cual utiliza los mismos metodos 
que el driver de chrome. Se puede utilizar firefox con solo inicializar el 
objeto Driver como `Driver(browser="firefox")`. Por defecto toma a Chrome 
como browser.

Tambien se documenta que todas las acciones que realice el driver, 
en el log `web_driver.log`.

Todos los browser son compatibles con los metodos que se encuentra en la
libreria, lo unico que difiere son los argumentos que se pasan por
argumento al iniciar el browser.