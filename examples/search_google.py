"""Search "Hello World!" in Google website"""
from Web_Driver import Driver
from time import sleep


def main():
    driver = Driver()
    driver.url('https://google.com')
    sleep(1)
    driver.send_text_to_input('id', 'lst-ib', 'Hello World!')
    driver.send_enter_key('id', 'lst-ib')
    sleep(4)


if __name__ == '__main__':
    main()
