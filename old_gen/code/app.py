from selenium import webdriver
import os
import Account
import utils

def maindesktop():
    email = input("Email: ")
    password = input("Password: ")
    accepted_location = input("Accepted Location (or 'any'): ")
    runon = input("Specific user in account (or 'all'): ")
    driver = webdriver.Chrome()
    return(driver,email,password,accepted_location,runon)


def maincontainer():
    email = os.getenv('VISA_EMAIL')
    password = utils.get_secret(email,'password')
    accepted_location = os.getenv('ACCEPTED_LOCATION')
    runon = os.getenv('RUN_ON')
    driver = webdriver.Chrome(options=utils.set_chrome_options())
    return(driver,email,password,accepted_location,runon)


if __name__ == '__main__':
    
    print("--- Robot start scanning ---")

    if os.getenv("CONTAINER_RUNNING") == "true":
        driver,email,password,accepted_location,runon = maincontainer()
        robot = Account.Account(driver,email,password,-1,accepted_location,runon)
    else:
        driver,email,password,accepted_location,runon = maindesktop()
        robot = Account.Account(driver,email,password,2400,accepted_location,runon)
    
    print("Finish Successfully")