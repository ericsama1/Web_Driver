import logging


class Log:
    def __init__(self, path):
        self.__logger = logging.getLogger(__name__)
        self.__formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-7s | %(message)s')
        self.__logger.setLevel(logging.INFO)
        self.__handler_info = logging.FileHandler(path)
        self.__handler_info.setLevel(logging.INFO)
        self.__handler_info.setFormatter(self.__formatter)
        self.__logger.addHandler(self.__handler_info)

    def info(self, text):
        self.__logger.info(text)

    def error(self, text):
        self.__logger.error(text, exc_info=True)

    def warning(self, text):
        self.__logger.warning(text)
