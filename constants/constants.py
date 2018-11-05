from selenium.webdriver.common.by import By
import locale

if 'es' in locale.getlocale()[0]:
    from constants.message_spanish import *
else:
    from constants.message_english import *

# Browsers
OPERA = 'opera'
CHROME = 'chrome'
FIREFOX = 'firefox'

# Commands
INCOGNITO = '--incognito'
PRIVATE = '--private'
HEADLESS = '--headless'
FULLSCREEN = '--start-fullscreen'
HIDE_SCROLLBAR = '--hide-scrollbar'
WINDOW_POSITION = '--window-position={},{}'

# Direction
TOP = 'top'
BOTTON = 'botton'
LEFT = 'left'
RIGHT = 'right'
HEIGHT = 'height'
WIDTH = 'width'

# Log
LOG_FILE = 'web_driver.log'

# JS
BACK = 'window.history.go(-1)'
SCROLL = 'scrollTo({},{});'
NEW_TAB = 'window.open("{}");'

# By
XPATH = By.XPATH
ID = By.ID
CLASS_NAME = By.CLASS_NAME

# Pdf_options
STRING = 'string'
URL = 'url'

