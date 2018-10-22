"""Get Google logo from website"""
from Web_Driver import Driver
from time import sleep


def main():
    driver = Driver()
    driver.url('https://google.com')
    sleep(1)
    driver.get_image('id', 'hplogo', 'google_logo.png')


if __name__ == "__main__":
    main()
