#    Libreria para poder utilizar las funciones de selenium, permitiendo
#    que se pueda utilizar en Chrome, Firefox y en Opera
#    Todavia hay funciones que no son compatibles en Firefox y Opera, 
#    pero en Chrome si estan funcionando
from sys import exit
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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from constants.constants import *
from log.Log import Log
from settings import (path_firefoxdriver, path_chromedriver, path_operadriver,
                      opera_binary_location, pdf_option, LOG_FILE)


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
                     'width' y 'height'
        :param incognito: flag para habilitar el modo incognito
        :param commands: se puede ingresar manualmente comandos para utilizar
                         en el driver
        :param position: posicion que se quiere abrir el browser, utiliza un
                         dict con 'x' e 'y', solo funciona con chrome
        :param fullscreen: flag para habilitar el modo fullscreen, solo
                           funciona con chrome
        """
        self.__log = Log(LOG_FILE)  # se crea un log en la ubicacion
        self.__menu_size = 0
        # se deja 1920x1080 como tamano por defecto de las pantallas
        # si se usa el headless
        if headless and size is None:
            size = {
                WIDTH: 1920,
                HEIGHT: 1080
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
                print(Fore.RED, MSJ_ERROR_DRIVER, Fore.RESET)
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
                print(Fore.RED, MSJ_ERROR_DRIVER, Fore.RESET)
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
            print(Fore.RED, MSJ_INVALID_BROWSER, Fore.RESET)
            exit(1)
        self.__log_info(MSJ_BROWSER.format(browser))

        # si el device es None, entonces no se emula
        # la emulacion solo funciona en chrome
        if device is not None:
            if browser == CHROME:
                # la emulacion de mobile
                mobile_emulation = {DEVICE_NAME: device}
                browser_options.add_experimental_option(MOBILE_EMULATION,
                                                        mobile_emulation)
                self.__log_info(MSJ_MOBILE_EMULATION.format(device))
            else:
                self.__log_warning(MSJ_INVALID_EMULATION.format(browser))

        # si el flag estan en True, se abre el navegador en modo incognito
        # el argumento es diferente respecto al browser utilizado
        if incognito:
            if browser == CHROME:
                browser_options.add_argument(INCOGNITO)
            elif (browser == FIREFOX or browser == OPERA):
                browser_options.add_argument(PRIVATE)

        # si el flag esta en True, se habilita el modo headless
        # el headless no funciona como corresponde en opera
        if headless:
            if browser == OPERA:
                self.__log_warning(MSJ_INVALID_HEADLESS)
            else:
                browser_options.add_argument(HEADLESS)

        # dejo esta opcion para que el usuario pueda ingresar a mano los
        # comandos que quiere ingresar manualmente
        if commands is not None:
            browser_options.add_argument(commands)

        # se puede pasar por parametro la posicion del navegador, funciona con
        # chrome
        if position is not None:
            if browser == CHROME:
                browser_options.add_argument(WINDOW_POSITION.format(
                                                position[X], position[Y]))
            else:
                self.__log_warning(MSJ_INVALID_WINDOW_POSITION.format(browser))

        # si el flag esta en True, se hace un f11 al browser para dejarlo en
        # fullscreen, solo funciona en chrome
        if fullscreen:
            if browser == CHROME:
                browser_options.add_argument(FULLSCREEN)
            else:
                self.__log_warning(MSJ_INVALID_FULLSCREEN.format(browser))

        # agrego este argumento para que se quite la barra de scroll en las
        # capturas de pantalla
        browser_options.add_argument(HIDE_SCROLLBAR)
        return browser_options

    def close(self):
        """ Metodo para cerrar el navegador que se esta utilizando """
        self.__browser.quit()
        self.__log_info(MSJ_CLOSE_BROWSER)

    def url(self, url):
        """ funcion para que el browser abra la url deseada """
        self.__browser.get(url=url)
        self.__log_info(MSJ_URL.format(url))

    def __search_element(self, by, value):
        """Metodo para buscar un elemento dentro de la pagina

        :param by: los argumentos son los mismos que tiene el
                   elemento By de selenium
        :param value: es el nombre del elemento que se quiere buscar
        :param return: devuelve un elemento si se encuentra,
                       sino devuelve None
        """
        self.__log_info(MSJ_SEARCH_ELEMENT.format(value, by))
        try:
            # busco el elemento
            elem = self.__browser.find_element(by, value)
            # Me fijo si el elemento esta visible y esta habilitado
            if elem is None:
                return None
            else:
                self.__log_info(MSJ_FIND_ELEMENT)
                if self.__is_enabled(elem) and self.__is_visible(elem):
                    return elem
                else:
                    # si no esta visible y no esta habilitado devuelvo
                    # None
                    return None
        except NoSuchElementException:
            self.__log_warning(MSJ_INVALID_ELEMENT.format(value))
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
                ids.append(elem.get_attribute(ID))
        self.__log_info(MSJ_SEARCH_ELEMENT.format(value, by))
        if len(ids) > 1:
            self.__log_info(MSJ_FIND_ELEMENTS)
        elif len(ids) == 1:
            self.__log_info(MSJ_FIND_ELEMENT)
        else:
            self.__log_warning(MSJ_INVALID_ELEMENT)
        return ids

    def __search_many_elements(self, by, value):
        """ buscador de conjunto de elementos por diferentes criterios
        Los parametros utilizado son los mismos que el
        metodo __search_element

        :param by: parametro de busqueda
        :param value: nombre del elemento que se esta buscando
        :return: devuelve una lista de los elementos encontrados
        """
        self.__log_info(MSJ_SEARCH_ELEMENTS.format(value, by))
        by = by.lower()
        elems = self.__browser.find_elements(by, value)
        if len(elems) == 0:
            self.__log_warning(MSJ_ERROR_SEARCH.format(value, by))
        return elems

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

    def __is_visible(self, element):
        """
        Metodo privado para verificar que un elemento esta visible, sin
        tener que pasar por el metodo de busqueda y no tener que repetir
        la busqueda"""
        if element.is_displayed():
            self.__log_info(MSJ_IS_VISIBLE)
            return True
        else:
            self.__log_warning(MSJ_IS_NOT_VISIBLE)
            return False

    def is_visible(self, by, value):
        """
        Metodo para verificar si un elemento esta visible

        :param by: parametro para el metodo de busqueda
        :param value: nombre del elemento que se busca
        :return: booleano si el elemento esta visible o no
        """
        elem = self.__search_element(by, value)
        self.__log_info(MSJ_ELEMENT_IS_VISIBLE.format(value))
        if self.__is_visible(elem):
            return True
        else:
            return False

    def __is_enabled(self, element):
        """
        Metodo privado para verificar que un elemento esta
        habilitado, sin tener que pasar por el metodo de busqueda
        y no quede repetido la busqueda"""
        if element.is_enabled():
            self.__log_info(MSJ_IS_ENABLED)
            return True
        else:
            self.__log_warning(MSJ_IS_NOT_ENABLED)
            return False

    def is_enabled(self, by, value):
        """
        Metodo para verificar si un elemento esta habilitado
        :param by: parametro para el metodo de busqueda
        :param value: nombre del elemento que se busca
        :return: booleano si el elemento esta habilitado o no
        """
        elem = self.__search_element(by, value)
        self.__log_info(MSJ_ELEMENT_IS_ENABLED.format(value))
        if self.__is_enabled(elem):
            return True
        else:
            return False

    def get_text(self, by, value):
        """
        Metodo para obtener el texto de un elemento

        :param by: parametro de busqueda
        :param value: nombre del elemento que se quiere buscar
        :return: devuelvo el texto que tiene el elemento
        """
        elem = self.__search_element(by, value)
        self.__log_info(MSJ_GET_TEXT.format(value))
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
                elem_interno = elem.find_element(CLASS_NAME, name)
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
        if box1[BOTTON] <= box2[BOTTON]:
            return False
        if box1[TOP] >= box2[TOP]:
            return False
        if box1[RIGHT] <= box2[RIGHT]:
            return False
        if box1[LEFT] >= box2[LEFT]:
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
                self.__log_warning(MSJ_IN_BOX.format(element.get_attibute(
                                                        CLASS), value)
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
                self.__log_warning(MSJ_OVERLAP.format(
                                          element.get_attribute(CLASS),
                                          elem_aux.get_attribute(CLASS)
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
        if filtro != BOTTON:
            if (not(box1[BOTTON] >= box2[TOP] and
                    box1[BOTTON] <= box2[BOTTON])):
                return False
        # si la direccion no es arriba, reviso si la parte superior
        # del box1 se superpone con el box2
        if filtro != TOP:
            if (not(box1[TOP] >= box2[TOP] and
                    box1[TOP] <= box2[BOTTON])):
                return False
        # si la direccion no es la izquierda, reviso si la parte izquierda
        # del box1 se superpone con el box2
        if filtro != LEFT:
            if (not(box1[LEFT] >= box2[LEFT] and
                    box1[LEFT] <= box2[RIGHT])):
                return False
        # si la direccion no es derecha, reviso si la parte inferior
        # del box1 se superpone con el box2
        if filtro != RIGHT:
            if (not(box1[RIGHT] >= box2[LEFT] and
                    box1[RIGHT] <= box2[RIGHT])):
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
        if box2[TOP] >= box1[TOP] and box2[TOP] <= box1[BOTTON]:
            if self.__check_lateral(box1, box2, TOP):
                return True
        # me fijo si el box1 esta en la parte derecha del box2
        elif box2[RIGHT] >= box1[LEFT] and box2[RIGHT] <= box1[RIGHT]:
            if self.__check_lateral(box1, box2, RIGHT):
                return True
        # me fijo si el box1 esta en la parte inferior del box2
        elif (box2[BOTTON] >= box1[TOP] and
              box2[BOTTON] <= box1[BOTTON]):
            if self.__check_lateral(box1, box2, BOTTON):
                return True
        # me fijo si el box1 esta en la parte izquierda del box2
        elif box2[LEFT] >= box1[LEFT] and box2[LEFT] <= box1[RIGHT]:
            if self.__check_lateral(box1, box2, LEFT):
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
        area_top = (box2[TOP] >= box1[TOP] and
                    box2[TOP] <= box1[BOTTON])
        # verifico que el area inferior de la superposicion se encuentre
        # dentro de los boxes
        area_botton = (box1[BOTTON] >= box2[TOP] and
                       box1[BOTTON] <= box2[BOTTON])
        if area_top:
            if area_botton:
                # pregunto si el box1 se encuentra mas a la derecha que
                # el box2
                if (box2[RIGHT] >= box1[LEFT]and
                        box2[RIGHT] <= box1[RIGHT]):
                    if (box2[LEFT] >= box1[LEFT] and
                            box2[LEFT] <= box1[RIGHT]):
                        return True
                # si el box1 esta mas a la izquierda que el box2, paso
                # por aca
                elif (box1[RIGHT] >= box2[LEFT] and
                        box1[RIGHT] <= box2[RIGHT]):
                    if (box2[LEFT] >= box1[LEFT] and
                            box2[LEFT] <= box1[RIGHT]):
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
        left = posicion[X]
        top = posicion[Y]
        right = left + tamano[WIDTH]
        botton = top + tamano[HEIGHT]
        box = {LEFT: left,
               TOP: top,
               RIGHT: right,
               BOTTON: botton}  # creo un box con las coordenadas
        return box

    def get_size(self, by, value):
        """
        Metodo para obtener la medida de un elemento

        :param by: parametro de busqueda
        :param value: nombre del elemento que se quiere buscar
        :return: tamano en [width, height] del elemento que se busco
        """
        elem = self.__search_element(by, value)
        self.__log_info(MSJ_GET_SIZE.format(elem.size))
        return elem.size

    def get_location(self, by, value):
        """
        Metodos para obtener la coordenada que se encuentra un elemento
        :param by: parametro de busqueda
        :param value: nombre del elemento
        :return: coordenadas en [x,y] del elemento que busco
        """
        elem = self.__search_element(by, value)
        self.__log_info(MSJ_GET_LOCATION.format(elem.location))
        return elem.location

    def send_text_to_input(self, by, value, text):
        """ Funcion para buscar un elemento y mandarle por teclado el texto
        que se le quiere ingresar

        :param by: parametro para el metodo de busqueda
        :param value: parametro para el metodo de busqueda
        :param text: Es el texto que se le quiere ingresar
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        elem = self.__search_element(by, value)
        if elem is None:
            return False
        else:
            elem.send_keys(text)
            if elem.get_attribute(TYPE) == PASSWORD:
                # si es una contrasena, no muestro el valor en el log
                self.__log_info(MSJ_INPUT_PASSWORD.format(value))
            else:
                self.__log_info(MSJ_INPUT_TEXT.format(text, value))
            return True

    def __click(self, element):
        """
        Metodo privado para hacer click sobre el elemento
        """
        element.click()

    def click(self, by, value):
        """
        Click sobre el elemento buscado

        :param by: parametro de busqueda
        :param value: nombre del elemento que se quiere buscar
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        elem = self.__search_element(by, value)
        if elem is None:
            return False
        else:
            self.__click(elem)
            self.__log_info(MSJ_CLICK.format(value))
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
        varios = self.__search_many_elements(XPATH, xpath)
        if len(varios) > 1:
            self.__log_info(MSJ_FIND_MANY_BTN_TEXT.format(text))
        elif len(varios) == 1:
            self.__log_info(MSJ_FIND_BTN_TEXT.format(text))
        else:
            # Si no se encuentra ningun boton con el texto
            return False
        # Si se encuentra por lo menos 1 elemento, se hace click sobre
        # el primer elemento
        self.__click(varios[0])
        self.__log_info(MSJ_CLICK)
        return True

    def __select_opction(self, by, value, texto):
        """Metodo para seleccionar una opcion del select
        :param by: parametro de busqueda
        :param value: nombre del select
        :param texto: texto del elemento que se quiere seleccionar"""
        select = Select(self.__browser.find_element(by, value))
        # uso el visible text, ya que si no se muestra el texto, no
        # tiene sentido el uso del select
        select.select_by_visible_text(texto)
        self.__log_info(MSJ_SELECT_OPTION.format(texto, value))

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
                self.__log_warning(MSJ_INVALID_OPTION.format(valor, value))
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
                valor = opcion.get_atributte(VALUE)
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
        elem = self.__search_element(ID, value)
        if elem is None:
            return False
        else:
            elem.send_keys(Keys.SPACE)
            self.__log_info(MSJ_CHECKBOX)
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
        elem = self.__search_element(by, value)
        if elem is None:
            return False
        else:
            elem.send_keys(Keys.ENTER)
            self.__log_info(MSJ_SEND_ENTER)
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
            self.__log_error(MSJ_INVALID_TAB)
            return False
        else:
            url = self.__get_url()
            self.__log_info(MSJ_CHANGE_TAB.format(url))
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
        self.__log_info(MSJ_NEW_TAB.format(url))
        script = NEW_TAB.format(url)
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
        self.__log_info(MSJ_EXECUTE_SCRIPT.format(script))
        return True

    def close_tab(self):
        """ cierra el tab actual y deja activo el primer tab
        :return: devuelvo un booleano, por si se pudo realizar la accion"""
        try:
            self.__browser.close()
            self.__log_info(MSJ_CLOSE_TAB)
            self.change_tab(self.tabs()[0])
        except WebDriverException:
            self.__log_error(MSJ_INVALID_CLOSE_TAB)
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
        if PNG in path:
            self.__browser.save_screenshot(path)
        else:
            self.__browser.save_screenshot('{}{}'.format(path, PNG))
        self.__log_info(MSJ_SAVE_SCREENSHOT.format(path))
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
        elem = self.__search_element(by, value)
        if elem is None:
            return False
        else:
            self.mouse_over(by, value)
            if PNG in path:
                self.__browser.save_screenshot(path)
            else:
                self.__browser.save_screenshot('{}{}'.format(path, PNG))
            self.__log_info(MSJ_ELEMENT_SCREENSHOT.format(value, path))
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
        if box[LEFT] > box[RIGHT]:
            return False
        elif box[TOP] > box[BOTTON]:
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
        box_aux = (box[LEFT],
                   box[TOP],
                   box[RIGHT],
                   box[BOTTON])
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
        elem = self.__search_element(by, value)
        if elem is not None:
            self.mouse_over(by, value)  # dejo el cursor sobre el elemento
        else:
            return False
        # Capturo la imagen de toda la pantalla
        img = self.__capturar_pantalla()

        # busco las coordenadas del box que se quiere capturar la pantalla
        box = self.get_box(by, value)
        if not self.__validate_box(box):
            self.__log_warning(MSJ_INVALID_BOX_SIZE)
            print(Fore.RED, MSJ_INVALID_BOX_SIZE, Fore.RESET)
            exit(1)
        altura = box[BOTTON] - box[TOP]
        browser_size = self.get_windows_size()
        browser_size[HEIGHT] -= self.__menu_size

        # me fijo si el elemento es mas grande que la pantalla
        # del browser
        if browser_size[HEIGHT] < altura:
            # scroll es la cantidad de pixeles que quiero mover

            scroll = browser_size[HEIGHT]
            box_aux = {LEFT: box[LEFT],
                       TOP: box[TOP],
                       RIGHT: box[RIGHT],
                       BOTTON: browser_size[HEIGHT]}
            if not self.__validate_box(box_aux):
                self.__log_warning(MSJ_INVALID_BOX_SIZE)
                print(Fore.RED, MSJ_INVALID_BOX_SIZE, Fore.RESET)
                exit(1)
            img = img.crop(self.__box_to_coordinate(box_aux))
            # verifico que no sea la ultima pantalla
            while altura > scroll + browser_size[HEIGHT]:
                # utilizo el metodo para desplazar X cantidad de pixeles
                self.mouse_scroll(by, value, 0, scroll)
                img2 = self.__capturar_pantalla()
                box_aux = {LEFT: box[LEFT],
                           TOP: 0,
                           RIGHT: box[RIGHT],
                           BOTTON: browser_size[HEIGHT]}
                if not self.__validate_box(box_aux):
                    self.__log_warning(MSJ_INVALID_BOX_SIZE)
                    print(Fore.RED, MSJ_INVALID_BOX_SIZE, Fore.RESET)
                    exit(1)
                img2 = img2.crop(self.__box_to_coordinate(box_aux))
                img = self.__combine_image(img, img2)
                scroll += browser_size[HEIGHT]

            # capturar el ultimo pedacito de la pagina
            self.mouse_scroll(by, value, 0, scroll)
            top = altura - scroll  # pixeles que faltan capturar
            # de la ultima pantalla, capturo solo los pixeles que necesito
            top = browser_size[HEIGHT] - top
            # creo un box con las coordenadas
            box = (box[LEFT], top, box[RIGHT], browser_size[HEIGHT])
            img_aux = self.__capturar_pantalla()
            # corto de la pantalla, el pedacito que necesito
            img_aux = img_aux.crop(box)
            # combino la imagen con el pedacito
            img = self.__combine_image(img, img_aux)
        else:
            # si esta dentro de la ventana del navegador, creo un box
            box_aux = (box[LEFT], box[TOP], box[RIGHT],
                       box[BOTTON])
            # recorto la imagen en las coordenadas que paso en el box
            img = img.crop(box_aux)
        if PNG not in dirname:
            dirname = dirname + PNG
        img.save(dirname)  # guardo la imagen en el path
        self.__log_info(MSJ_ELEMENT_SCREENSHOT.format(value, dirname))
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
            source = self.get_attribute(by, value, SOURCE)
            if BASE64 in source:
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
            self.__log_info(MSJ_GET_IMAGE.format(value, dirname))
            return img
        except NoSuchElementException:
            self.__log_error(MSJ_INVALID_IMAGE)
            return None

    def mouse_over(self, by, value):
        """ Mueve el mouse sobre el elemento buscado
        :return: devuelvo un booleano, por si se pudo realizar la accion"""
        elem = self.__search_element(by, value)
        if elem is None:
            return False
        else:
            mover = AC(self.__browser).move_to_element(elem)
            mover.perform()
            self.__log_info(MSJ_MOUSE_OVER.format(value))
            return True

    def double_click(self, by, value):
        """ Hace doble click en el elemento
        :return: devuelvo un booleano, por si se pudo realizar la accion"""
        elem = self.__search_element(by, value)
        if elem is None:
            return False
        else:
            AC(self.__browser).double_click(elem)
            self.__log_info(MSJ_DOUBLE_CLICK.format(value))
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
            self.__browser.execute_script(SCROLL.format(horizontal, vertical))
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
        elem = self.__search_element(by, value)
        if elem is None:
            return False
        else:
            atributo = elem.get_attribute(attribute)
            # si atributo es nulo, es porque no existe el atributo ingresado
            if atributo is None:
                self.__log_warning(MSJ_INVALID_ATTRIBUTE)
            return atributo

    def clear(self, by, value):
        """ limpia el input buscado

        :param by: parametro de busqueda
        :param value: nombre del elemento que se busca
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        elem = self.__search_element(by, value)
        if elem is None:
            return False
        else:
            # si se encuentra el elemento, sigo
            elem.clear()
            self.__log_info(MSJ_CLEAR.format(value))
            return True

    def clear_all(self):
        """ limpia todos los input y los select que se muestra en
        la pagina
        :return: devuelvo un booleano, por si se pudo realizar la accion """
        elems_input = self.__search_many_elements(XPATH,
                                                  '//input[starts-with('
                                                  '@id,"id")]')
        elems_select = self.__search_many_elements(XPATH, '//select')
        for elem in elems_input:
            if not elem.clear():
                self.__log_error(MSJ_CANT_CLEAR.format(elem.get_attribute(ID)))
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
            self.__log_info(MSJ_CONFIRM_ALERT)
            return True
        # si no se encuentra el alert devuelvo falso
        except NoAlertPresentException:
            self.__log_error(MSJ_INVALID_ALERT)
            return False

    def alert_dismmis(self):
        """ Se rechaza la alerta
        :return: devuelvo un booleano, por si se pudo realizar la accion"""
        try:
            alert = self.__browser.switch_to.alert
            alert.dismiss()
            self.__log_info(MSJ_REJECT_ALERT)
            return True
        # si no se encuentra el alert devuelvo falso
        except NoAlertPresentException:
            self.__log_error(MSJ_INVALID_ALERT)
            return False

    def input_alert(self, text):
        """ se ingresa texto en la alerta

        :param text: texto que se quiere ingresar al alert
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        try:
            alert = self.__browser.switch_to.alert
            alert.send_keys(text)
            self.__log_info(MSJ_INPUT_ALERT.format(text))
            return True
        # si no se encuentra el alert devuelvo falso
        except (NoAlertPresentException, ElementNotSelectableException):
            self.__log_error(MSJ_INVALID_ALERT)
            return False

    def back(self):
        """ Metodo para volver una pagina atras en el historial
        No se usa el metodo back, ya que este rompe el navegador, si
        es que no tiene una pagina anterior, y no se puede capturar el error
        :return: devuelvo un booleano, por si se pudo realizar la accion
        """
        self.__browser.execute_script(BACK)
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
        self.__browser.set_window_size(size[WIDTH], size[HEIGHT])
        self.__log_info(MSJ_SET_WINDOW_SIZE.format(size[WIDTH],
                                                   size[HEIGHT]))
        return True

    def get_windows_size(self):
        """ Metodo para obtener el tamano de la ventana del navegador """
        return self.__browser.get_window_size()

    def maximize_windows(self):
        """ Metodo para maximizar la ventana
        :return: devuelvo un booleano, por si se pudo realizar la accion"""
        self.__browser.maximize_window()
        self.__log_info(MSJ_MAXIMIZE_WINDOW)
        return True

    def to_pdf(self, dirname, option=STRING):
        """
        Convierte la pagina actual en un pdf. Este metodo suele tardar
        bastante tiempo en la conversion a pdf
        :param dirname: direccion en la que se quiere guardar el pdf
        :return: devuelvo un booleano si se pudo generar el pdf
        """
        # si se ingresa con la opcion de string, se genera el pdf desde
        # el string del html. Tener en cuenta que este procedimiento
        # no guarda en el pdf las imagenes
        if option == STRING:
            try:
                from_string(self.__get_html(), dirname, options=pdf_option)
                self.__log_info(MSJ_PDF.format(dirname))
                return True
            except OSError:
                print(Fore.RED, MSJ_ERROR_PDF, Fore.RESET)
                self.__log_error()
                return False
        # si se ingresa con la opcion de url, se genera el pdf desde la url
        # de la pagina.
        elif option == URL:
            try:
                from_url(self.__get_url(), dirname, options=pdf_option)
                self.__log_info(MSJ_PDF.format(dirname))
                return True
            except OSError:
                print(Fore.RED, MSJ_ERROR_PDF, Fore.RESET)
                self.__log_error()
                return False
        else:
            self.__log_warning(MSJ_INVALID_OPTION)
            return False

    def __get_html(self):
        elem = self.__browser.find_element(XPATH, '//*')
        source_code = elem.get_attribute('outerHTML')
        self.__log_info(MSJ_GET_HTML)
        return source_code

    def get_html(self):
        """
        Metodo para obtener el codigo html de la pagina web
        :return: devuelvo el string del html de la pagina web
        """
        return self.__get_html()

    def __get_url(self):
        return self.__browser.current_url

    def get_url(self):
        """
        Metodo para obtener la url actual
        :return: devuelvo el string con la url actual
        """
        self.__log_info(MSJ_GET_URL)
        return self.__get_url()
