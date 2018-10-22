# Web_Driver


Se crea el Web_Driver para facilitar el uso de selenium, creando metodos que no estan por defecto
en el driver de selenium.

Para utilizar el Web_Driver, se necesita instalar ciertos paquetes: 
- Selenium `sudo pip install selenium`
- PIL `sudo pip install pil`
- Pdfkit `sudo pip install pdfkit`
- chromedriver, download from `http://chromedriver.chromium.org/downloads` 
- Geckodriver, download from `https://github.com/mozilla/geckodriver/releases`

Tambien se precisa asignar en el `settings.py` o en le `settings_local.py` el `path_chromedriver` y el `path_firefoxdriver` en el correspondiente path de los driver descargados 

Para un mejor manejo, se puede utilizar el mismo driver para levantar una pagina web con el browser de firefox.
Se puede utilizar firefox con solo inicializar el objeto Driver como `Driver(browser="firefox")`. Por defecto toma a Chrome como browser
