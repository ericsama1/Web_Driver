"""Create tabs and use them"""
from Web_Driver import Driver
from time import sleep


def main():
    driver = Driver()
    driver.url('https://google.com')
    driver.new_tab('https://youtube.com')
    driver.new_tab('https://facebook.com')
    driver.change_tab(driver.tabs()[0])
    sleep(1)
    driver.send_text_to_input('id', 'lst-ib', 'Hello World!')
    driver.send_enter_key('id', 'lst-ib')
    sleep(1)
    driver.close_tab()
    sleep(1)
    driver.close()


if __name__ == '__main__':
    main()
