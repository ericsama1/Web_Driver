#    Libreria para poder utilizar las funciones de selenium, permitiendo
#    que se pueda utilizar en chrome y en firefox
#    Todavia hay funciones que no son compatibles en firefox, en chrome
#    estan funcionando
import sys
from base64 import b64decode
from io import BytesIO
from random import choice
from urllib.request import urlretrieve

from PIL import Image
from colorama import Fore
from pdfkit import from_string, from_url
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException, ElementClickInterceptedException,
    UnexpectedTagNameException, NoSuchWindowException,
    WebDriverException, InvalidElementStateException,
    NoAlertPresentException, ElementNotSelectableException,
    ElementNotVisibleException)
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.opera.options import Options as OperaOptions
from selenium.webdriver.common.action_chains import ActionChains as AC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from constants.constants import CHROME, FIREFOX, OPERA
from log.Log import Log
from settings import (path_firefoxdriver, path_chromedriver, path_operadriver,
                      opera_binary_location)


class Driver:
    def __init__(self, browser=CHROME, device=None, headless=False,
                 size=None, incognito=False, commands=None, position=None,
                 fullscreen=False
                 ):
        """Inicializador del driver

        :param browser: Se ingresa el navegador que se quiere utilizar,
                        por momentos solo se puede utilizar
                        firefox y chrome
        :param device: es para pasar por parametro el dispositivo que
                       se quiere utilizar.
        :param headless: flag para habilitar en modo headless
        :param size: tamano de la ventana del browser, utiliza un dict con
                     'ancho' y 'alto'
        :param incognito: flag para habilitar el modo incognito
        :param commands: se puede ingresar manualmente comandos para utilizar
                         en el driver
        :param position: posicion que se quiere abrir el browser, utiliza un
                         dict con 'x' e 'y', solo funciona con chrome
        :param fullscreen: flag para habilitar el modo fullscreen, solo
                           funciona con chrome
        """
        self.__log = Log('web_driver.log')  # se crea un log en la ubicacion
        self.__menu_size = 0
        # se deja 1920x1080 como tamano por defecto de las pantallas
        # si se usa el headless
        if headless and size is None:
            size = {
                "ancho": 1920,
                "alto": 1080
            }
        browser_options = self.__set_options(browser, device, headless,
                                             incognito, commands, position,
                                             fullscreen)
        if browser == FIREFOX:
            # el menu size es los pixeles que usa la barra de direcciones,
            # el conjunto de las pestanas en firefox
            self.__menu_size = 75
            try:
                self.__browser = webdriver.Firefox(
                    executable_path=path_firefoxdriver,
                    firefox_options=browser_options)
            except WebDriverException:
                self.__log_error()
                print("{}No se pudo iniciar el driver, revisar los "
                      "parametros {}".format(Fore.RED, Fore.RESET))
                exit(1)
        elif browser == CHROME:
            if headless:
                # si uso el headless, no tngo pixeles molestos
                self.__menu_size = 0
            else:
                # el menu size es los pixeles que usa la barra de direcciones,
                # el conjunto de las pestanas, y la alerta de sistema
                # automatizado
                self.__menu_size = 105
            try:
                self.__browser = webdriver.Chrome(
                    executable_path=path_chromedriver,
                    chrome_options=browser_options)
            except WebDriverException:
                self.__log_error()
                print("{}No se pudo iniciar el driver, revisar los "
                      "parametros {}".format(Fore.RED, Fore.RESET))
                exit(1)
        elif browser == OPERA:
            try:
                self.__browser = webdriver.Opera(
                    executable_path=path_operadriver,
                    options=browser_options)
            except WebDriverException:
                self.__log_error
                exit(1)
        if not fullscreen:
            if size is None:
                # si no se ingresa una medida y no se usa el headless, se
                # maximiza la pantalla
                self.maximize_windows()
            else:
                self.set_windows_size(size)
        self.__browser.implicitly_wait(0.3)  # timeout para el wait

    def __set_options(self, browser, device, headless, incognito,
                      commands, position, fullscreen):
        """
        Metodo para setear las opciones para los navegadores. Se
        dejan los argumentos que no funcionan en firefox, ya que
        estos no afectan al browser

        :param browser: nombre del navegador que se utiliza
        :param device: nombre del dispositivo movil
        :param headless: flag para habilitar la opcion de headless
        :param incognito: flag para habilitar el modo incognito
        :param commands: se puede ingresar manualmente comandos
                         para utilizar en el driver
        :param position: posicion que se quiere abrir el browser,
                         utiliza un dict con 'x' e 'y', solo
                         funciona con chrome
        :param fullscreen: flag para habilitar el modo fullscreen, solo
                           funciona con chrome
        :return: devuelvo un Options segun el navegador que utilizo
        """
        # el objeto Options varia segun el navegador
        if browser == FIREFOX:
            browser_options = FirefoxOptions()
        elif browser == CHROME:
            browser_options = ChromeOptions()
        elif browser == OPERA:
            browser_options = OperaOptions()
            # para hacer andar opera, hay que pasarle la direccion del
            # ejecutable de opera
            browser_options.binary_location = opera_binary_location
        else:
            # si no se ingresa un valor valido, por ahora los valores validos,
            # son chrome y firefox
            print('{}NO se ingreso un navegador valido{}'.format(
                Fore.RED, Fore.RESET))
            sys.exit(1)
        self.__log_info('Se inicia la aplicacion con {}'.format(browser))

        # si el device es None, entonces no se emula
        # la emulacion solo funciona en chrome
        if device is not None:
            if browser == CHROME:
                # la emulacion de mobile
                mobile_emulation = {"deviceName": device}
                browser_options.add_experimental_option("mobileEmulation",
                                                        mobile_emulation)
                self.__log_info('Se inicia con la vista del movil'
                                ' {}'.format(device))
            else:
                self.__log_warning('No se puede emular un dispositivo '
                                   'movil en {}'.format(browser))

        # si el flag estan en True, se abre el navegador en modo incognito
        # el argumento es diferente respecto al browser utilizado
        if incognito:
            if browser == CHROME:
                browser_options.add_argument("--incognito")
            elif (browser == FIREFOX or browser == OPERA):
                browser_options.add_argument("--private")

        # si el flag esta en True, se habilita el modo headless
        # el headless no funciona como corresponde en opera
        if headless:
            if browser == OPERA:
                self.__log_warning('No se puede utilizar la herramienta '
                                   'headless para opera')
            else:
                browser_options.add_argument("--headless")

        # dejo esta opcion para que el usuario pueda ingresar a mano los
        # comandos que quiere ingresar manualmente
        if commands is not None:
            browser_options.add_argument(commands)

        # se puede pasar por parametro la posicion del navegador, funciona con
        # chrome
        if position is not None:
            if browser == CHROME:
                browser_options.add_argument('--window-position={},{}'.format(
                                                position['x'], position['y']))
            else:
                self.__log_warning('No se puede posicionar la ventana en {}'.
                                   format(browser))

        # si el flag esta en True, se hace un f11 al browser para dejarlo en
        # fullscreen, solo funciona en chrome
        if fullscreen:
            if browser == CHROME:
                browser_options.add_argument('--start-fullscreen')
            else:
                self.__log_warning('no esta habilitado el fullscreen en {}'.
                                   format(browser))

        # agrego este argumento para que se quite la barra de scroll en las
        # capturas de pantalla
        browser_options.add_argument('--hide-scrollbar')
        return browser_options

    def close(self):
        """ Metodo para cerrar el navegador que se esta utilizando """
        self.__browser.quit()
        self.__log_info('Se cierra el navegador')

    def url(self, url):
        """ funcion para que el browser abra la url deseada """
        self.__browser.get(url=url)
        self.__log_info('Se abre un tab con la url: "{}"'.format(url))

    def __search_element(self, by, value):
        """Metodo para buscar un elemento dentro de la pagina

        :param by: los argumentos son los mismos que tiene el
                   elemento By de selenium
        :param value: es el nombre del elemento que se quiere buscar
        :param return: devuelve un elemento si se encuentra,
                       sino devuelve None
        """
        self.__log_info('Se busca el elemento "{}" por {}'.format(value, by))
        try:
            elem = self.__browser.find_element(by, value)
            return elem
        except NoSuchElementException:
            self.__log_warning('No se encuentra el elemento '
                               '{}'.format(value))
            return None

    def search_ids(self, by, value):
        """
        Metodo para buscar varios elementos, y devolver un array
        con los ids de dichos elementos

        :param by: los argumentos de busqueda
        :param value: nombre del id
        :return: Devuelvo los id de los elementos en forma de array
        """
        elems = self.__search_many_elements(by, value)
        ids = []
        for elem in elems:
            if elem.is_displayed():
                ids.append(elem.get_attribute('id'))
        self.__log_info('se buscan los elementos {} con el parametro {}'.
                        format(value, by)
                        )
        if len(ids) > 1:
            self.__log_info('se encontro varios elementos')
        elif len(ids) == 1:
            self.__log_info('se encontro el elemento')
        else:
            self.__log_warning('No se encontro ningun elemento')
        return ids

    def __search_many_elements(self, by, value):
        """ buscador de conjunto de elementos por diferentes criterios
        Los parametros utilizado son los mismos que el
        metodo __search_element

        :param by: parametro de busqueda
        :param value: nombre del elemento que se esta buscando
        :return: devuelve una lista de los elementos encontrados
        """
        self.__log_info('Se buscan elementos {} por {}'.format(value, by))
        by = by.lower()
        elems = self.__browser.find_elements(by, value)
        if len(elems) == 0:
            self.__log_warning("No se encuentra ningun elemento {} con el "
                               "parametro {}".format(value, by))
        return elems

    def obtener_input_texto_error(self):
        """
        Metodo para buscar el error, este no es generico, sirve solo para
        el form de registro
        """
        try:
            input_errores = self.__browser.find_elements(
                By.XPATH, "//span[contains(@class,'error')]//ancestor::div"
                          "[1]//child::input"
            )
            for error in input_errores:
                # guardo el id del campo que muestra el error
                id_campo_error = error.get_attribute('id')
                # capturo el mensaje de error del input
                span_error = self.__browser.find_element(
                    By.XPATH, "//input[@id='{}']//ancestor::div"
                              "[1]//child::span".format(id_campo_error)
                )
                # guardo en el log, el campo y el mensaje de error
                self.__log_warning('Hay errores en el campo {}, '
                                   'con texto "{}"'.format(id_campo_error,
                                                           span_error.text)
                                   )
            return True
        except NoSuchElementException:
            self.__log_info("No se encuentra errores")
            return False

    def buscar_error(self):
        """
        Metodo para que se busque errores, pero sin utilizar el metodo de
        busqueda, ya que el otro metodo muestra un warning cuando no hay
        errores

        :return: Si es True, hay errores; si es False, no hay errores
        """
        try:
            self.__browser.find_elements_by_xpath(
                "//*[contains(@class,'error')]"
            )
            return True
        except NoSuchElementException:
            return False

    def is_visible(self, by, value):
        """
        Metodo para verificar si un elemento esta visible

        :param by: parametro para el metodo de busqueda
        :param value: nombre del elemento que se busca
        :return: booleano si el elemento esta visible o no
        """
        elem = self.__search_element(by, value)
        self.__log_info('Se verifica si el elemento {} esta visible'.
                        format(value))
        if elem.is_displayed():
            self.__log_info('El elemento esta visible')
            return True
        else:
            self.__log_warning('El elemento no esta visible')
            return False

    def is_enabled(self, by, value):
        """
        Metodo para verificar si un elemento esta habilitado
        :param by: parametro para el metodo de busqueda
        :param value: nombre del elemento que se busca
        :return: booleano si el elemento esta habilitado o no
        """
        elem = self.__search_element(by, value)
        self.__log_info('Se verifica si el elemento {} esta habilitado'.
                        format(value))
        if elem.is_enabled():
            self.__log_info('El elemento esta habilitado')
            return True
        else:
            self.__log_warning('El elemento no esta habilitado')
            return False

    def get_text(self, by, value):
        """
        Metodo para obtener el texto de un elemento

        :param by: parametro de busqueda
        :param value: nombre del elemento que se quiere buscar
        :return: devuelvo el texto que tiene el elemento
        """
        elem = self.__search_element(by, value)
        self.__log_info('se busca el texto del elemento {}'.format(value))
        return elem.text

    def __get_elements_in_element(self, by, value, class_names):
        """
        Metodo para obtener los elementos que se encuentran dentro
        de otro elemento

        :param by: parametro de busqueda
        :param value: nombre del elemento que contiene los elementos
        :param class_names: array con los nombres de las clases
                            que se quiere verificar
        :return: devuelvo un array con los elementos si es
                 que los tiene
        """
        elem = self.__search_element(by, value)
        elements = []
        for name in class_names:
            try:
                # busco por nombre de clase dentro del elemento
                elem_interno = elem.find_element(By.CLASS_NAME, name)
                # si el elemento se muestra, lo guardo en la lista
                if elem_interno.is_displayed():
                    elements.append(elem_interno)
            except NoSuchElementException:
                pass
        # devuelvo la lista con los elementos que se encuentran dentro
        # del elemento padre
        return elements

    @staticmethod
    def __compare_box(box1, box2):
        """
        Metodo para verificar que el box 2 esta dentro del box 1

        :param box1: Box que contiene el elemento del box 2
        :param box2: Box del elemento
        :return: devuelvo True si el box2 esta dentro del box1
                 devuelvo False si el box2 NO est dentro del box1
        """
        if box1['botton'] <= box2['botton']:
            return False
        if box1['top'] >= box2['top']:
            return False
        if box1['right'] <= box2['right']:
            return False
        if box1['left'] >= box2['left']:
            return False
        return True

    def check_boxs(self, by, value, class_names):
        """
        Metodo para chequear si el elemento esta dentro del boxs
        Tambien chequea que los elementos no se pisen entre si

        :param by: parametro de busqueda
        :param value: nombre del elemento que se busca
        :param class_names: array con los elementos internos que se busca
        :return: Si el elemento del array esta dentro del box, devuelvo
                 true, si un elemento se encuentra
        """
        elements = self.__get_elements_in_element(by, value, class_names)
        box = self.get_box(by, value)
        for element in elements:
            # Primero reviso que los elementos se encuentren dentro del boton
            elem_box = self.get_box(by=None, value=None, elem=element)
            if not self.__compare_box(box, elem_box):
                self.__log_warning('el elemento {} no esta dentro del '
                                   'box {}'.format(element.get_attibute(
                                       'class'),
                                       value)
                                   )
                return False
            # una vez revisado que los elementos se encuentran dentro del
            # boton, reviso que los elementos no se pisen entre ellos
            aux = elements
            # creo un array aux para pasar todas las clases, menos el mismo
            # elemento
            aux.remove(element)
            elem_aux = self.check_overlap_element(elem_box, aux)
            if elem_aux is not None:
                self.__log_warning('hay superposicion en el elemento {} '
                                   'con el elemento {}'.
                                   format(element.get_attribute('class'),
                                          elem_aux.get_attribute('class')
                                          )
                                   )
        return True

    @staticmethod
    def __check_lateral(box1, box2, filtro):
        """
        Metodo para comprobar si el box1 esta superpuesto sobre el box2
        en la direccion que se pasa en la variable quitar
        :param box1, box2: coordenadas de los boxes que se quiere verificar
        :param filtro: direccion en la que se quiere verificar
        :return: devuelvo True si hay superposicion
                 devuelvo False si NO hay superposicion
        """
        # si la direccion no es abajo, reviso si la parte inferior
        # del box1 se superpone con el box2
        if filtro != 'botton':
            if (not(box1['botton'] >= box2['top'] and
                    box1['botton'] <= box2['botton'])):
                return False
        # si la direccion no es arriba, reviso si la parte superior
        # del box1 se superpone con el box2
        if filtro != 'top':
            if (not(box1['top'] >= box2['top'] and
                    box1['top'] <= box2['botton'])):
                return False
        # si la direccion no es la izquierda, reviso si la parte izquierda
        # del box1 se superpone con el box2
        if filtro != 'left':
            if (not(box1['left'] >= box2['left'] and
                    box1['left'] <= box2['right'])):
                return False
        # si la direccion no es derecha, reviso si la parte inferior
        # del box1 se superpone con el box2
        if filtro != 'right':
            if (not(box1['right'] >= box2['left'] and
                    box1['right'] <= box2['right'])):
                return False
        return True

    def __lateral(self, box1, box2):
        """
        Metodo para verificar que el box1 se superpone con un costado
        del box2
        :param box1, box2: coordenadas de los boxes que se quiere verificar
        :return: devuelvo True si hay superposicion
                 devuelvo False si NO hay superposicion
        """
        # me fijo si el box1 esta en la parte superior del box2
        if box2['top'] >= box1['top'] and box2['top'] <= box1['botton']:
            if self.__check_lateral(box1, box2, "top"):
                return True
        # me fijo si el box1 esta en la parte derecha del box2
        elif box2['right'] >= box1['left'] and box2['right'] <= box1['right']:
            if self.__check_lateral(box1, box2, "right"):
                return True
        # me fijo si el box1 esta en la parte inferior del box2
        elif (box2['botton'] >= box1['top'] and
              box2['botton'] <= box1['botton']):
            if self.__check_lateral(box1, box2, "botton"):
                return True
        # me fijo si el box1 esta en la parte izquierda del box2
        elif box2['left'] >= box1['left'] and box2['left'] <= box1['right']:
            if self.__check_lateral(box1, box2, "left"):
                return True
        else:
            return False

    @staticmethod
    def __two_lateral(box1, box2):
        """
        Metodo para verificar si hay superposicion de los elementos
        en las puntas de ambos
        :param box1, box2: medidas para verificar que no se
                           superpongan entre si
        :return: devuelvo True, si hay superposicion
                 devuelvo False, si no hay superposicion
        """
        # pregunto por el area superior de la superposicion entre los
        # boxes
        area_top = (box2['top'] >= box1['top'] and
                    box2['top'] <= box1['botton'])
        # verifico que el area inferior de la superposicion se encuentre
        # dentro de los boxes
        area_botton = (box1['botton'] >= box2['top'] and
                       box1['botton'] <= box2['botton'])
        if area_top:
            if area_botton:
                # pregunto si el box1 se encuentra mas a la derecha que
                # el box2
                if (box2['right'] >= box1['left']and
                        box2['right'] <= box1['right']):
                    if (box2['left'] >= box1['left'] and
                            box2['left'] <= box1['right']):
                        return True
                # si el box1 esta mas a la izquierda que el box2, paso
                # por aca
                elif (box1['right'] >= box2['left'] and
                        box1['right'] <= box2['right']):
                    if (box2['left'] >= box1['left'] and
                            box2['left'] <= box1['right']):
                        return True
        return False

    def __compare_overlap(self, box1, box2):
        """
        Metodo para chequear si hay superposicion entre los 2 boxes
        :param box1, box2: dos medidas para verificar que no se
                           superpongan entre si
        :return: devuelvo False, si NO hay superposicion
                 devuelvo True, si hay superposicion
        """
        if self.__compare_box(box1, box2):
            return True
        elif self.__two_lateral(box1, box2):
            return True
        elif self.__lateral(box1, box2):
            return True
        else:
            return False

    def check_overlap_element(self, elem_box, class_names):
        """
        Metodo para revisar si hay superposicion de los elementos
        de un boton
        :param elem_box: elemento que se quiere revisar
        :param class_names: nombre de las clases que hay en el boton
        :return: si encuentro superposicion, devuelvo el elemento que
                 se hace la superposicion
        """
        for element in class_names:
            element_box = self.get_box(by=None, value=None, elem=element)
            if self.__compare_overlap(elem_box, element_box):
                # si hay superposicion, devuelvo el elemento
                return element
            else:
                # si no hay superposicion, devuelvo None
                return None

    def get_box(self, by, value, elem=None):
        """
        Metodo para obtener la medida de un box de un elemento

        :param by: parametro de busqueda
        :param value: nombre del elemento a buscar
        :param elem: Se puede pasar directamente un elemento
        :return: coordenadas del marco del box que se genera del box
        """
        if elem is None:  # si no paso un elemento, lo busco
            elem = self.__search_element(by, value)  # busco el elemento
        tamano = elem.size  # obtengo el tamano el elemento
        posicion = elem.location  # obtengo la posicion del elemento
        left = posicion['x']
        top = posicion['y']
        right = left + tamano['width']
        botton = top + tamano['height']
        box = {"left": left,
               "top": top,
               "right": right,
               "botton": botton}  # creo un box con las coordenadas
        return box

    def get_size(self, by, value):
        """
        Metodo para obtener la medida de un elemento

        :param by: parametro de busqueda
        :param value: nombre del elemento que se quiere buscar
        :return: tamano en [width, height] del elemento que se busco
        """
        elem = self.__search_element(by, value)
        return elem.size

    def get_location(self, by, value):
        """
        Metodos para obtener la coordenada que se encuentra un elemento
        :param by: parametro de busqueda
        :param value: nombre del elemento
        :return: coordenadas en [x,y] del elemento que busco
        """
        elem = self.__search_element(by, value)
        return elem.location

    def send_text_to_input(self, by, value, text):
        """ Funcion para buscar un elemento y mandarle por teclado el texto
        que se le quiere ingresar

        :param by: parametro para el metodo de busqueda
        :param value: parametro para el metodo de busqueda
        :param text: Es el texto que se le quiere ingresar
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        try:
            elem = self.__search_element(by, value)
        except NoSuchElementException:
            self.__log_error('El elemento "{}" no existe'.format(value))
            return False
        elem.send_keys(text)
        if elem.get_attribute('type') == 'password':
            # si es una contrasena, no muestro el valor en el log
            self.__log_info('Se ingresa un valor en {}'.format(value))
        else:
            self.__log_info('Se ingresa el valor "{}" en {}'.format(
                text, value))
        return True

    def click(self, by, value):
        """
        Click sobre el elemento buscado

        :param by: parametro de busqueda
        :param value: nombre del elemento que se quiere buscar
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        try:
            elem = self.__search_element(by, value)
            if self.is_enabled(by, value):
                elem.click()
        except ElementClickInterceptedException:
            self.__log_error('El elemento no se puede clickear')
            return False
        except ElementNotVisibleException:
            self.__log_error('Elemento no visible')
            return False
        else:
            self.__log_info('Se clickea el elemento {}'.format(value))
            return True

    def click_by_text(self, text, tagname='*'):
        """
        Click sobre un elemento por texto
        Se clickea el primer elemento que se encuentra con ese texto

        :param text: texto del elemento que se quiere clickear
        :param tagname: tagname del elemento, por default se deja *
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        xpath = '//{}[contains(text(),"{}")]'.format(tagname, text)
        varios = self.__search_many_elements('xpath', xpath)
        if len(varios) > 1:
            self.__log_info("Se encontraron varios elementos con el texto"
                            "{}".format(text))
            # se hace click sobre el primer elemento
            varios[0].click()
            return True
        elif len(varios) == 1:
            self.__log_info("Se encontro un solo elemento con el texto"
                            "{}".format(text))
            return True
        else:
            return False

    def __select_opction(self, by, value, texto):
        """Metodo para seleccionar una opcion del select
        :param by: parametro de busqueda
        :param value: nombre del select
        :param texto: texto del elemento que se quiere seleccionar"""
        select = Select(self.__browser.find_element(by, value))
        # uso el visible text, ya que si no se muestra el texto, no
        # tiene sentido el uso del select
        select.select_by_visible_text(texto)
        self.__log_info("Se selecciona el valor {} en el select "
                        "{}".format(texto, value))

    def select_by_text(self, by, value, valor):
        """ Seleccionar un elemento de un select, se busca por ID

        :param by: parametro de busqueda
        :param value: nombre del select, por lo general, se busca por id
        :param valor: el valor que se quiere seleccionar
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        # Obtengo las opciones dentro del select
        opciones = self.get_select_options(by, value)
        # Si opciones es None, es porque no existe
        if opciones is None:
            return False
        else:
            esta = False
            # Recorro las opciones para verificar que existe la opcion
            for opcion in opciones:
                if valor == opcion.text:
                    esta = True
            # Si esta, entonces lo selecciono
            if esta:
                self.__select_opction(by, value, valor)
                return True
            # Si no esta, devuelvo un False y lo escribo en el log
            else:
                self.__log_warning("No existe la opcion {} en el select"
                                   "{}".format(valor, value))
                return False

    def select_random(self, by, value):
        """ seleccionar un elemento de un select aleatoriamente

        :param by: parametro de busqueda
        :param value: nombre del Select que se quiere seleccionar
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        # Obtengo las opciones dentro del select
        opciones = self.get_select_options(by, value)
        # Si opciones es None, es porque no existe
        if opciones is None:
            return False
        else:
            # Selecciono una opcion cualquiera del select
            valor = choice(opciones)
            self.__select_opction(by, value, valor.text)
            return True

    def select_by_index(self, by, value, index):
        """
        Metodo para seleccionar una opcion del select utilizando
        el indice del elemento

        :param by: parametro de busqueda
        :param value: id del select
        :param index: indice del elemento que se quiere seleccionar
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        # obtengo los valores del select
        opciones = self.get_select_options(by, value)
        # Si opciones es None, es porque no existe
        if opciones is None:
            return False
        else:
            # Obtengo el valor de la posicion index y lo selecciono
            valor = opciones[index]
            self.__select_opction(by, value, valor.text)
            return True

    def select_by_value(self, by, value, select_value):
        """
        Metodo para seleccionar una opcion del select utlizando
        el value de la opcion

        :param by: parametro de busqueda
        :param value: id del select
        :param select_value:  value del elemento que se quiere seleccionar
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        # Obtengo las opciones dentro del select
        opciones = self.get_select_options(by, value)
        # Si opciones es None, es porque no existe
        if opciones is None:
            return False
        else:
            texto = ''
            # Recorro todas las opciones
            for opcion in opciones:
                # Obtengo el atributo "value" de la opcion
                valor = opcion.get_atributte('value')
                # Si el atributo coincide con el select_value guardo
                # el texto
                if valor == select_value:
                    texto = opcion.text()
            # Si el texto es '', es que no existe el select_value
            # ingresado
            if texto == '':
                return False
            # Sino, selecciono la opcion
            else:
                self.__select_opction(by, value, texto)
                return True

    def get_select_options(self, by, value):
        """
        Metodo para obtener todas las opciones dentro de un select
        las opciones se lee con el atributo text de cada opcion
        :param by: parametro de busqueda
        :param value: nombre del elemento que se quiere buscar
        :return: array con todas las opciones que se puede seleccionar
                 dentro del Select
        """
        select = Select(self.__search_element(by, value))
        return select.options

    def check(self, value):
        """ Funcion para seleccionar un checkbox

        :param value: nombre del checkbox que se quiere marcar, se
                          busca por id
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        try:
            self.__search_element(By.ID, value).send_keys(Keys.SPACE)
        except NoSuchElementException:
            self.__log_error('No se encuentra el elemento {}'.format(value))
            return False
        else:
            # si enceuntro el checkbox, lo marco
            self.__log_info('Se marca el checkbox {}'.format(value))
            return True

    def search_elem(self, by, value):
        """ Funcion publica para que el usuario pueda buscar un
        elemento que se encuentre en la pagina

        :param by: parametro de busqueda
        :param value: nombre del elemento que se busca
        :return: devuleve True si encontro el elemento, sino devuelve False
        """
        if self.__search_element(by, value) is None:
            return False
        else:
            return True

    def send_enter_key(self, by, value):
        """ Funcion para utilizar la tecla Enter en el input

        :param by: parametro de busqueda
        :param value: nombre del elemento que se busca
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        try:
            self.__search_element(by, value).send_keys(Keys.ENTER)
        except NoSuchElementException:
            self.__log_error('No se encuentra el elemento {}'.format(value))
            return False
        else:
            return True

    def change_tab(self, windows_name):
        """ se utiliza para cambiar de tab

        :param windows_name: nombre del tab que se quiere cambiar, hay que
                             utilizar el metodo tabs para obtener
                             los nombres
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        try:
            self.__browser.switch_to.window(windows_name)
        except NoSuchWindowException:
            self.__log_error('El tab que se quiere seleccionar, no existe')
            return False
        else:
            self.__log_info('Se cambia el tab activo')
            return True

    def tabs(self):
        """ Devuelve los handle de los tabs que estan abierto, esto se
        devuelve en formato de array. La pos 0, es el primer tab,
        el resto es el orden de la ultima pestana nueva

        :return: devuelvo las pestanas que tiene abierto el browser
        """
        return self.__browser.window_handles

    def new_tab(self, url='about:blank'):
        """ Abre una pestana nueva y se la deja como el tab activo

        :param url: url que se quiere abrir en el nuevo tab, por defecto
                    abre about:blank
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        self.__log_info('Se va a abrir un nuevo tab con la url: "{}"'.
                        format(url))
        script = "window.open('{}');".format(url)
        self.execute_script(script)
        tabs = self.tabs()
        self.change_tab(tabs[len(tabs) - 1])  # Cambio el tab activo
        return True

    def execute_script(self, script):
        """ Se ejecuta un script en javascript

        :param script: se pasa en un string el script de js que se quiere
                       ejecutar
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        self.__browser.execute_script(script)
        self.__log_info('Se ejecuta el scipt {}'.format(script))
        return True

    def close_tab(self):
        """ cierra el tab actual y deja activo el primer tab
        :return: devuelvo un booleano, por si se pudo realizar la accion"""
        try:
            self.__browser.close()
            self.change_tab(self.tabs()[0])
            self.__log_info('Se cierra el tab actual')
        except WebDriverException:
            self.__log_error('No hay ningun tab abierto para seleccionar')
            return False
        else:
            return True

    def screenshot(self, path):
        """ Saca un screenshot de la pantalla actual de la pagina y la
        guarda en el path ingresado, hay que ingresar el formato

        :param path: ubicacion donde se almacenara el screenshot,
        se le tiene que agregar una extension de imagen
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        if '.png' in path:
            self.__browser.save_screenshot(path)
        else:
            self.__browser.save_screenshot('{}.png'.format(path))
        self.__log_info('Se hace una captura de pantalla y se guarda en el '
                        'path  {}'.format(path))
        return True

    def elem_screenshot(self, by, value, path):
        """
        Metodo para capturar la pantalla completa del browser, y que
        contenga el elemento deseado
        :param by: metodo de busqueda
        :param value: id del elemento que se quiere capturar
        :param path: path de donde se guarda la imagen
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        try:
            # primero me fijo que exista el elemento
            self.__search_element(by, value)
        except NoSuchElementException:
            self.__log_error('No existe el elemento {}'.format(value))
            return False
        else:
            self.mouse_over(by, value)
            if '.png' in path:
                self.__browser.save_screenshot(path)
            else:
                self.__browser.save_screenshot('{}.png'.format(path))
            self.__log_info('Se hace una captura de pantalla del elemento'
                            '{} en el path {}'.format(value, path))
            return True

    @staticmethod
    def __combine_image(img1, img2):
        """
        Metodo para juntar 2 imagenes, combina en la parte inferior de
        la img1
        :param img1: imagen principal
        :param img2: imagen que se le quiere adjuntar a la imagen1
        :return: devuelvo una imagen combinada entre ambas
        """
        total_altura = img1.size[1] + img2.size[1]
        img = Image.new('RGB', (img1.size[0], total_altura))
        img.paste(img1, (0, 0))
        img.paste(img2, (0, img1.size[1]))
        return img

    def __capturar_pantalla(self):
        """ Metodo para crear una imagen del browser y dejarlo en memoria """
        return Image.open(BytesIO(self.__browser.get_screenshot_as_png()))

    @staticmethod
    def __validate_box(box):
        """
        Metodo para validar las medidas del box
        :param box: box con 4 medidas, left, top, right, botton
        :return: booleano para validar medidas del box
        """
        if box['left'] > box['right']:
            return False
        elif box['top'] > box['botton']:
            return False
        else:
            return True

    @staticmethod
    def __box_to_coordinate(box):
        """
        Metodo para pasar las coordenadas del box en dict a un
        conjunto de coordenadas

        :param box: coordenadas en forma de dict
        :return: conjunto de coordenadas para usar en el crop
        """
        box_aux = (box['left'],
                   box['top'],
                   box['right'],
                   box['botton'])
        return box_aux

    def element_to_png(self, by, value, dirname):
        """
        Metodo para hacer un screenshot de un elemento.
        Si el elemento que se quiere capturar es mas grande que
        la ventana del browser

        Se tiene que arreglar cuando la imagen es mas grande que la
        ventana, se puede utilizar el metodo set_windows_size para
        achicar la ventana y poder probar

        :param by: parametro de busqueda
        :param value: nombre del elemento
        :param dirname: ruta donde se guarda la imagen
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        if self.__search_element(by, value) is not None:
            self.mouse_over(by, value)  # dejo el cursor sobre el elemento
        else:
            # si la busqueda devuelve un None
            self.__log_error('No se encontro el elemento {}'.format(value))
            return False
        # Capturo la imagen de toda la pantalla
        img = self.__capturar_pantalla()

        # busco las coordenadas del box que se quiere capturar la pantalla
        box = self.get_box(by, value)
        if not self.__validate_box(box):
            self.__log_warning('La medida del box ingresado no son validos')
            print('{}La medida del box ingresado no son validos{}'.format(
                Fore.RED, Fore.RESET))
            sys.exit(1)
        altura = box['botton'] - box['top']
        browser_size = self.get_windows_size()
        browser_size['height'] -= self.__menu_size

        # me fijo si el elemento es mas grande que la pantalla
        # del browser
        if browser_size['height'] < altura:
            # scroll es la cantidad de pixeles que quiero mover

            scroll = browser_size['height']
            box_aux = {'left': box['left'],
                       'top': box['top'],
                       'right': box['right'],
                       'botton': browser_size['height']}
            if not self.__validate_box(box_aux):
                self.__log_warning(
                    'La medida del box ingresado no son validos')
                print('{}La medida del box ingresado no son validos{}'.
                      format(Fore.RED, Fore.RESET))
                sys.exit(1)
            img = img.crop(self.__box_to_coordinate(box_aux))
            # verifico que no sea la ultima pantalla
            while altura > scroll + browser_size['height']:
                # utilizo el metodo para desplazar X cantidad de pixeles
                self.mouse_scroll(by, value, 0, scroll)
                img2 = self.__capturar_pantalla()
                box_aux = {'left': box['left'],
                           'top': 0,
                           'right': box['right'],
                           'botton': browser_size['height']}
                if not self.__validate_box(box_aux):
                    self.__log_warning('La medida del box ingresado no '
                                       'son validos')
                    print('{}La medida del box ingresado no son validos{}'.
                          format(Fore.RED, Fore.RESET))
                    sys.exit(1)
                img2 = img2.crop(self.__box_to_coordinate(box_aux))
                img = self.__combine_image(img, img2)
                scroll += browser_size['height']

            # capturar el ultimo pedacito de la pagina
            self.mouse_scroll(by, value, 0, scroll)
            top = altura - scroll  # pixeles que faltan capturar
            # de la ultima pantalla, capturo solo los pixeles que necesito
            top = browser_size['height'] - top
            # creo un box con las coordenadas
            box = (box['left'], top, box['right'], browser_size['height'])
            img_aux = self.__capturar_pantalla()
            # corto de la pantalla, el pedacito que necesito
            img_aux = img_aux.crop(box)
            # combino la imagen con el pedacito
            img = self.__combine_image(img, img_aux)
        else:
            # si esta dentro de la ventana del navegador, creo un box
            box_aux = (box['left'], box['top'], box['right'],
                       box['botton'])
            # recorto la imagen en las coordenadas que paso en el box
            img = img.crop(box_aux)
        if '.png' not in dirname:
            dirname = dirname + '.png'
        img.save(dirname)  # guardo la imagen en el path
        self.__log_info('Se hace una captura de pantalla del elemento {}'
                        'en el path {}'.format(value, dirname))
        return True

    def get_image(self, by, value, dirname):
        """
        Metodo para guardar una imagen de la pagina. Almacena la imagen
        si esta en base64, o si tiene un str de la ubicacion
        :param by: parametro de busqueda
        :param value: nombre del elemento que se busca
        :param dirname: path de donde se guarda la imagen
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        # obtengo el source del elemento que se busca
        try:
            source = self.get_attribute(by, value, 'src')
            if "base64" in source:
                # get str
                source = source.split(',')[1]
                # decode
                source = b64decode(source)
                with open(dirname, "wb") as fh:
                    # save to a file
                    fh.write(source)
            else:
                # save to a file
                urlretrieve(source, dirname)
            img = Image.open(dirname)
            self.__log_info("Se encontro el elemento {} y se guardo en {}".
                            format(value, dirname))
            return img
        except NoSuchElementException:
            self.__log_error("No se encuentra el elemento para "
                             "guardar la img")
            return None

    def mouse_over(self, by, value):
        """ Mueve el mouse sobre el elemento buscado
        :return: devuelvo un booleano, por si se pudo realizar la accion"""
        try:
            elem = self.__search_element(by, value)
        except NoSuchElementException:
            self.__log_error('No existe el elemento {}'.format(value))
            return False
        else:
            mover = AC(self.__browser).move_to_element(elem)
            mover.perform()
            self.__log_info(
                'Se posiciona el mouse sobre el elemento {}'.format(
                    value))
            return True

    def double_click(self, by, value):
        """ Hace doble click en el elemento
        :return: devuelvo un booleano, por si se pudo realizar la accion"""
        try:
            elem = self.__search_element(by, value)
        except NoSuchElementException:
            self.__log_error('No se encuentra el elemento {}'.format(value))
            return False
        else:
            AC(self.__browser).double_click(elem)
            self.__log_info('Se hace doble click sobre el elemento {}'.format(
                value))
            return True

    def mouse_scroll(self, by, value, horizontal, vertical):
        """
        Metodo para simular el scroll del mouse en un elemento

        :param by: parametro de busqueda
        :param value: nombre del elemento
        :param horizontal: cantidad de scroll que se desea hacer horizontal
        :param vertical: cantidad de scroll que se desea hacer vertical
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        if self.mouse_over(by, value):
            self.__browser.execute_script("scrollTo({},{});".format(
                horizontal, vertical))
            return True
        else:
            return False

    def get_attribute(self, by, value, attribute):
        """ devuelvo el atributo especifico de un elemento

        :param by: parametros para la busqueda
        :param value: parametros para la busqueda
        :param attribute: nombre del atributo que se quiere obtener
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        try:
            elem = self.__search_element(by, value)
        except NoSuchElementException:
            self.__log_error('No se encuentra el elemento {}'.format(value))
            return None
        else:
            atributo = elem.get_attribute(attribute)
            # si atributo es nulo, es porque no existe el atributo ingresado
            if atributo is None:
                self.__log_warning('El atributo no existe')
            return atributo

    def clear(self, by, value):
        """ limpia el input buscado

        :param by: parametro de busqueda
        :param value: nombre del elemento que se busca
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        try:
            elem = self.__search_element(by, value)
        except (NoSuchElementException, InvalidElementStateException):
            self.__log_error('No se encuentra el elemento {}'.format(value))
            return False
        else:
            # si se encuentra el elemento, sigo
            elem.clear()
            self.__log_info('Se limpia el input del elemento {}'.format(
                value))
            return True

    def clear_all(self):
        """ limpia todos los input y los select que se muestra en
        la pagina
        :return: devuelvo un booleano, por si se pudo realizar la accion """
        elems_input = self.__search_many_elements('xpath',
                                                  '//input[starts-with('
                                                  '@id,"id")]')
        elems_select = self.__search_many_elements('xpath', '//select')
        for elem in elems_input:
            if not elem.clear():
                self.__log_error('No se pudo borrar el elemento {}'.format(
                    elem.get_attribute('id')))
        for elem in elems_select:
            select = Select(elem)
            select.select_by_index(0)  # En la pos 0, es la opcion en blanco
        return True

    def alert_confirm(self):
        """ Se acepta la alerta
        :return: devuelvo un booleano, por si se pudo realizar la accion"""
        try:
            alert = self.__browser.switch_to.alert
            alert.accept()
            self.__log_info('Se confirma la alerta')
            return True
        # si no se encuentra el alert devuelvo falso
        except NoAlertPresentException:
            self.__log_error('No se presenta la alerta')
            return False

    def alert_dismmis(self):
        """ Se rechaza la alerta
        :return: devuelvo un booleano, por si se pudo realizar la accion"""
        try:
            alert = self.__browser.switch_to.alert
            alert.dismiss()
            self.__log_info('Se rechaza la alerta')
            return True
        # si no se encuentra el alert devuelvo falso
        except NoAlertPresentException:
            self.__log_error('No se presenta la alerta')
            return False

    def input_alert(self, text):
        """ se ingresa texto en la alerta

        :param text: texto que se quiere ingresar al alert
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        try:
            alert = self.__browser.switch_to.alert
            alert.send_keys(text)
            self.__log_info('Se ingresa el valor {} en la alerta'.format(text))
            return True
        # si no se encuentra el alert devuelvo falso
        except (NoAlertPresentException, ElementNotSelectableException):
            self.__log_error('No se muestra la alerta')
            return False

    def back(self):
        """ Metodo para volver una pagina atras en el historial
        No se usa el metodo back, ya que este rompe el navegador, si
        es que no tiene una pagina anterior, y no se puede capturar el error
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        self.__browser.execute_script("window.history.go(-1)")
        return True

    def forward(self):
        """ Metodo para adelantar una pagina en el historial
        :return: devuelvo un booleano, por si se pudo realizar la accion """
        self.__browser.forward()
        return True

    def __log_info(self, text):
        """ Se utiliza solo para escribir algun mensaje al log

        :param text: texto que se quiere escribir en el log
        """
        self.__log.info(text)

    def __log_error(self, text=''):
        """ Se utiliza para escribir un error en el log

        :param text: texto que se quiere escribir en el log
        """
        self.__log.error(text)

    def __log_warning(self, text):
        """ Se utiliza para escribir un warning en el log

        :param text: texto que se quiere escribir en el log
        """
        self.__log.warning(text)

    def set_windows_size(self, size):
        """ Metodo para cambiar el tamano de la ventana

        :param size: un dict que contenga el ancho y el alto
                     de las pantallas que se quiere utilizar
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        self.__browser.set_window_size(size['ancho'], size['alto'])
        self.__log_info('Se establece el tamano de la pantalla a '
                        '{}x{}'.format(size['ancho'],
                                       size['alto']))
        return True

    def get_windows_size(self):
        """ Metodo para obtener el tamano de la ventana del navegador """
        return self.__browser.get_window_size()

    def maximize_windows(self):
        """ Metodo para maximizar la ventana
        :return: devuelvo un booleano, por si se pudo realizar la accion"""
        self.__browser.maximize_window()
        self.__log_info('Se maximiza la ventana')
        return True

    def to_pdf(self, dirname, option='string'):
        """
        Convierte la pagina actual en un pdf. Este metodo suele tardar
        bastante tiempo en la conversion a pdf
        :param dirname: direccion en la que se quiere guardar el pdf
        :return: devuelvo un booleano si se pudo generar el pdf
        """
        pdf_option = {
            'page-size': 'A4',
            'encoding': 'UTF-8'
        }
        # si se ingresa con la opcion de string, se genera el pdf desde
        # el string del html. Tener en cuenta que este procedimiento
        # no guarda en el pdf las imagenes
        if option == 'string':
            try:
                from_string(self.get_html(), dirname, options=pdf_option)
                self.__log_info("Se crea el pdf de la pagina en la ubicacion"
                                "{}".format(dirname))
                return True
            except OSError:
                print('{}Ocurrio un error en la conversion a pdf, '
                      'revisar el log{}'.format(Fore.RED, Fore.RESET))
                self.__log_error()
                return False
        # si se ingresa con la opcion de url, se genera el pdf desde la url
        # de la pagina.
        elif option == 'url':
            try:
                from_url(self.get_url(), dirname, options=pdf_option)
                self.__log_info("Se crea el pdf de la pagina en la ubicacion"
                                "{}".format(dirname))
                return True
            except OSError:
                print('{}Ocurrio un error en la conversion a pdf, '
                      'revisar el log{}'.format(Fore.RED, Fore.RESET))
                self.__log_error()
                return False
        else:
            self.__log_warning("No se ingreso una opcion valida")
            return False

    def get_html(self):
        """
        Metodo para obtener el codigo html de la pagina web
        :return: devuelvo el string del html de la pagina web
        """
        elem = self.__browser.find_element('xpath', '//*')
        source_code = elem.get_attribute('outerHTML')
        self.__log_info("Se obtiene el codigo html de la pagina")
        return source_code

    def get_url(self):
        """
        Metodo para obtener la url actual
        :return: devuelvo el string con la url actual
        """
        self.__log_info("Se obtiene la url actual del navegador")
        return self.__browser.current_url
