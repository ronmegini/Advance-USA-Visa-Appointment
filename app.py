from selenium import webdriver
import os
import Account


def maindesktop():
    email = input("Email: ")
    password = input("Password: ")
    driver = webdriver.Chrome()
    return(email,password,driver)


def maincontainer():
    email = os.getenv('VISA_EMAIL')
    password = os.getenv('VISA_PASSWORD')
    driver = webdriver.Chrome(options=Account.set_chrome_options())
    return(email,password,driver)


if __name__ == '__main__':
    
    print("--- Robot start scanning... ---")

    try:

        if os.getenv("CONTAINER_RUNNING") == "true":
            robot = Account.Account(maincontainer())    
        else:
            robot = Account.Account(maindesktop())
                    
    except Exception as e:
        print("Failed due to: {}".format(e))
    