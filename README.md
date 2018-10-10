# Web_Driver


Se crea el Web_Driver para facilitar el uso de selenium, creando metodos que no estan por defecto
en el driver de selenium.

Para utilizar el Web_Driver, se necesita instalar ciertos paquetes: 
- Selenium
- PIL
- Colorama
- Pdfkit
- Driver para chrome
- Geckodriver

Tambien se precisa asignar en el `settings.py` el `path_chromedriver` y el `path_firefoxdriver` en el correspondiente path de los driver descargados 

Para un mejor manejo, se puede utilizar el mismo driver para levantar una pagina web con el browser de firefox.
Se puede utilizar firefox con solo llamar a `browser="firefox"` en el inicilizador del driver
