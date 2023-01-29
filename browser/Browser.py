from time import sleep

from selenium import webdriver

from refs import Global
from refs.pages import PopupsPage

driver = webdriver.Chrome(executable_path=Global.path('browser/chromedriver.exe'))

def start(max=False):
    driver.start_client()
    if max:
        driver.maximize_window()


def go_to(url):
    driver.get(url)
    sleep(0.5)
    try:
        PopupsPage.cookie_popup().click()
    except:
        pass


def get_driver():
    return driver


def quit():
    driver.close()
    driver.quit()

