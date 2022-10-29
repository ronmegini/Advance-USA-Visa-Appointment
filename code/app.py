from selenium import webdriver
import os
import Account


def maindesktop():
    email = input("Email: ")
    password = input("Password: ")
    accepted_location = input("Accepted Location: ")
    driver = webdriver.Chrome()
    return(driver,email,password,accepted_location)


def maincontainer():
    email = os.getenv('VISA_EMAIL')
    password = os.getenv('VISA_PASSWORD')
    accepted_location = os.getenv('ACCEPTED_LOCATION')
    driver = webdriver.Chrome(options=Account.set_chrome_options())
    return(driver,email,password,accepted_location)


if __name__ == '__main__':
    
    print("--- Robot start scanning ---")

    if os.getenv("CONTAINER_RUNNING") == "true":
        driver,email,password,accepted_location = maincontainer()
        robot = Account.Account(driver,email,password,-1,accepted_location)    
    else:
        driver,email,password,accepted_location = maindesktop()
        robot = Account.Account(driver,email,password,2400,accepted_location)
    