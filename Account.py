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
import Customer




class Account():
    """
    Object handle the webdriver session which perform the automated actions

    :param email: (str) email used for login
    :param password: (str) password used for login
    """

    EMBASSY_URL = r"https://ais.usvisa-info.com/he-il/niv/users/sign_in"

    def __init__(self, driver, email, password):
        # attributes
        self.driver = driver
        self.email = email
        self.password = password

        # functions
        self.login()
        customers = self.list_customers()
        self.reschedule_customers(customers)
        time.sleep(10)
        self.driver.close()


    def login(self):
        """
        Login into use visa site with the object's credentials.
        The result is driver's signed in session.

        :returns: None
        """

        print("--- login ---")
        self.driver.get(self.EMBASSY_URL)
        email_field = self.driver.find_element(By.ID, "user_email")
        email_field.send_keys(self.email)
        password_field = self.driver.find_element(By.ID, "user_password")
        password_field.send_keys(self.password)
        policy_field = self.driver.find_element(By.ID, "policy_confirmed")
        actions = ActionChains(self.driver)
        actions.move_to_element(policy_field).perform()
        self.driver.execute_script("arguments[0].click();", policy_field)
        self.driver.find_element(By.NAME, "commit").click()


    def parse_date(self, raw_string):
        """
        Extract date and location from string

        :date: (str) raw location and date string

        :returns:
        :date: (datetime) date of the original appointment
        :location: (str) Tel Aviv or Jerusalem
        """
        print("--- parse_date ---")
        MONTHS = {
            'ינואר': 'Jan',
            'פברואר': 'Feb',
            'מרץ': 'Mar',
            'אפריל': 'Apr',
            'מאי': 'May',
            'יוני': 'Jun',
            'יולי': 'Jul',
            'אוגוסט': 'Aug',
            'ספטמבר': 'Sep',
            'אוקטובר': 'Oct',
            'נובמבר': 'Nov',
            'דצמבר': 'Dec',
        }

        
        for key, value in MONTHS.items():
            raw_string = raw_string.replace(key, value)
        raw_string = re.sub("[^a-zA-Z0-9]", "",raw_string)
        if "TelAviv" in raw_string: location="Tel Aviv"
        if "Jerusalem" in raw_string: location="Jerusalem"
        raw_string = re.sub("TelAvivatTelAviv", "00",raw_string)
        raw_string = re.sub("JerusalematJerusalem", "00",raw_string)
        date = datetime.strptime(raw_string, '%d%b%Y%H%M%S')
        
        return date,location


    def list_customers(self):
        """
        Get all customers details under the selected account.

        :returns:
        :urls: (list of atr) urls of reschedule appointment
        :current_date: (datetime) date of the original appointment
        :location: (str) Tel Aviv or Jerusalem
        """
        print("--- list_customers ---")
        customers_details = []
        customers = self.driver.find_elements(By.CSS_SELECTOR, ".application.attend_appointment.card.success")
        if customers == []: raise Exception("No user waiting for interview in this account")
        for customer in customers:
            url = customer.find_element(By.CSS_SELECTOR, ".button.primary.small").get_attribute("href")
            current_appointment = customer.find_element(By.CLASS_NAME, "consular-appt").text
            name = customer.find_element(By.XPATH, "./table[@class='medium-12 columns margin-bottom-20']/tbody/tr/td[1]").text
            current_date,location = self.parse_date(current_appointment)
            customers_details.append({"name": name, "date": current_date, "location":location, "url":url})
        return(customers_details)


    def reschedule_customers(self, customers):
        while True:
            for customer in customers:
                print("Name: {}, Date: {}, Location: {}".format(customer["name"],customer["date"],customer["location"]))
                Customer.Customer(self.driver, customer["name"], customer["date"], customer["location"], customer["url"])
                time.sleep(60)


def set_chrome_options() -> None:
    """
    Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """

    print("--- set_chrome_options ---")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options