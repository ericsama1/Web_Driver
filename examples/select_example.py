"""Select a option for select tag element"""
from Web_Driver import Driver
from time import sleep
from constants.constants import NAME


def main():
    driver = Driver()
    driver.url('http://www.htmlquick.com/reference/tags/select.html')
    sleep(1)
    driver.select_by_text(NAME, 'sport', 'Tennis')
    sleep(1)
    driver.select_by_index(NAME, 'sport', 0)
    sleep(1)
    driver.select_random(NAME, 'sport')
    sleep(1)
    driver.close()

if __name__ == '__main__':
    main()
