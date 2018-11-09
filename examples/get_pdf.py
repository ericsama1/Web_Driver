"""Convert a website to pdf"""
from Web_Driver import Driver
from time import sleep
from constants.constants import ID, URL


def main():
    driver = Driver()
    driver.url('https://google.com')
    sleep(1)
    driver.send_text_to_input(ID, 'lst-ib', 'Hello World!')
    driver.send_enter_key(ID, 'lst-ib')
    driver.to_pdf('example.pdf', URL)


if __name__ == '__main__':
    main()
