from selenium import webdriver
import os
import Account


def maindesktop():
    email = input("Email: ")
    password = input("Password: ")
    driver = webdriver.Chrome()
    return(driver,email,password)


def maincontainer():
    email = os.getenv('VISA_EMAIL')
    password = os.getenv('VISA_PASSWORD')
    driver = webdriver.Chrome(options=Account.set_chrome_options())
    return(driver,email,password)


if __name__ == '__main__':
    
    print("--- Robot start scanning ---")

    try:

        if os.getenv("CONTAINER_RUNNING") == "true":
            driver,email,password = maincontainer()
            robot = Account.Account(driver,email,password,-1)    
        else:
            driver,email,password = maindesktop()
            robot = Account.Account(driver,email,password,2400)
    
    except Exception as e:
        print("Failed due to:")
        print(e)
    