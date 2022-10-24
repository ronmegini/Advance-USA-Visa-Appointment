from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import os
import Account



if __name__ == '__main__':
    
    print("I'm starting")
    try:
        if os.getenv("CONTAINER_RUNNING") == "true":
            email = os.getenv('VISA_EMAIL')
            password = os.getenv('VISA_PASSWORD')
            driver = webdriver.Chrome(options=Account.set_chrome_options())
        else:
            email = input("Email: ")
            password = input("Password: ")
            driver = webdriver.Chrome()
        robot = Account.Account(driver,email,password)
    except Exception as e:
        print("Failed due to: {}".format(e))
    