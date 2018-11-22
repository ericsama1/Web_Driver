"""Get Google logo from website"""
from Web_Driver import Driver
from time import sleep
from constants.constants import ID


def main():
    driver = Driver()
    driver.url('https://google.com')
    sleep(1)
    driver.get_image(ID, 'hplogo', 'google_logo.png')


if __name__ == "__main__":
    main()
