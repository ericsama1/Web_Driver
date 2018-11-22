"""Search "Hello World!" in Google website"""
from Web_Driver import Driver
from time import sleep
from constants.constants import NAME


def main():
    driver = Driver()
    driver.url('https://google.com')
    sleep(1)
    driver.send_text_to_input(NAME, 'q', 'Hello World!')
    driver.send_enter_key(NAME, 'q')
    sleep(4)


if __name__ == '__main__':
    main()
