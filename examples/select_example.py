"""Select a option for select tag element"""
from Web_Driver import Driver
from time import sleep


def main():
    driver = Driver()
    driver.url('http://www.htmlquick.com/reference/tags/select.html')
    sleep(1)
    driver.select_by_text('name', 'sport', 'Tennis')
    sleep(1)
    driver.select_by_index('name', 'sport', 0)
    sleep(1)
    driver.select_random('name', 'sport')
    sleep(1)
    driver.close()

if __name__ == '__main__':
    main()
