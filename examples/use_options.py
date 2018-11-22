"""Use firefox browser and incognito mode"""
from Web_Driver import Driver
from time import sleep
from constants.constants import FIREFOX, NAME


def main():
    driver = Driver(browser=FIREFOX, incognito='True')
    driver.url('https://google.com')
    sleep(1)
    driver.send_text_to_input(NAME, 'q', 'Hello World!')
    driver.send_enter_key(NAME, 'q')
    sleep(1)
    driver.close()

if __name__ == '__main__':
    main()
