from selenium.webdriver.common.by import By
import locale as __locale

if 'es' in __locale.getlocale()[0]:
    from constants.message_spanish import *
elif 'jp' in __locale.getlocale()[0]:
    from constants.message_japanese import *
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

# Device Emulation
DEVICE_NAME = 'deviceName'
MOBILE_EMULATION = 'mobileEmulation'

# Direction
TOP = 'top'
BOTTON = 'botton'
LEFT = 'left'
RIGHT = 'right'
HEIGHT = 'height'
WIDTH = 'width'
X = 'x'
Y = 'y'

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

# Img
BASE64 = 'base64'
SOURCE = 'src'
PNG = '.png'

# Attribute
CLASS = 'class'
VALUE = 'value'
TYPE = 'type'
PASSWORD = 'password'
