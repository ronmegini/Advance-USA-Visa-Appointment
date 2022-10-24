from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
import re
import os
import Account




def set_chrome_options() -> None:
    """
    Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """

    print("set_chrome_options")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


if __name__ == '__main__':
    print("I'm starting")
    driver = webdriver.Chrome(options=set_chrome_options())
    EMAIL = os.getenv('VISA_EMAIL')
    PASSWORD = os.getenv('VISA_PASSWORD')
    robot = Account(driver,EMAIL,PASSWORD)