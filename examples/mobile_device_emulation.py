from time import sleep
from Web_Driver import Driver
from constants.constants import ID, DEVICE_ARRAY, CLASS_NAME


def main():
    driver = Driver(device=DEVICE_ARRAY[9])
    driver.url('https://google.com')
    sleep(1)
    driver.send_text_to_input(CLASS_NAME, 'gLFyf', 'Hello World!')
    driver.send_enter_key(CLASS_NAME, 'gLFyf')
    driver.close()

if __name__ == '__main__':
    main()
