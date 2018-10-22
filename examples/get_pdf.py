"""Convert a website to pdf"""
from Web_Driver import Driver
from time import sleep


def main():
    driver = Driver()
    driver.url('https://google.com')
    sleep(1)
    driver.send_text_to_input('id', 'lst-ib', 'Hello World!')
    driver.send_enter_key('id', 'lst-ib')
    driver.to_pdf('example.pdf', 'url')


if __name__ == '__main__':
    main()
