try:
    from settings_local import (path_chromedriver, path_firefoxdriver,
                                path_operadriver, opera_binary_location)
except ImportError:
    pass

# Pdf_options
pdf_option = {
    'page-size': 'A4',
    'encoding': 'UTF-8'
}

# Log
LOG_FILE = 'web_driver.log'
