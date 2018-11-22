from time import sleep
from Web_Driver import Driver
from constants.constants import OPERA, NAME


def main():
    driver = Driver(browser=OPERA)
    driver.url('https://youtube.com')
    driver.new_tab('https://google.com')
    driver.new_tab('https://facebook.com')
    driver.change_tab(driver.tabs()[0])
    sleep(1)
    driver.close_tab()
    sleep(1)
    driver.send_text_to_input(NAME, 'q', 'Hello World!')
    driver.send_enter_key(NAME, 'q')
    sleep(1)
    driver.close()

if __name__ == '__main__':
    main()
