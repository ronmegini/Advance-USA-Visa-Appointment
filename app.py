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



class Account():
    """
    Object handle the webdriver session which perform the automated actions

    :param email: (str) email used for login
    :param password: (str) password used for login
    """
    def __init__(self, email, password):
        # attributes
        self.driver = webdriver.Chrome() # Locate the right version of chromedriver in the same directory
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
        print("login")
        self.driver.get("https://ais.usvisa-info.com/he-il/niv/users/sign_in")
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
        print("parse_date")
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
        print("list_customers")
        customers_details = []
        customers = self.driver.find_elements(By.CSS_SELECTOR, ".application.attend_appointment.card.success")
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
                Customer(self.driver, customer["name"], customer["date"], customer["location"], customer["url"])



class Customer():
    """
    Object handle each customer inside the account and find the earlier appointment time

    :param driver: (driver) selenium web driver
    :param name: (str) the name of the customer
    :param current_date: (datetime) the current date
    :param location: (str) Current appointment location
    :param url: (str) action page's url
    """

    def __init__(self, driver, name, current_date, location, url):
        # attributes
        self.driver = driver
        self.name = name
        self.current_date = current_date
        self.location = location
        self.url = url

        # functions
        self.reschedule()
    

    def reschedule(self):
        """
        Reschedule the appointment to the earlier time possible

        :returns:
        :new_date: (datetimer) The updated date
        """
        print("reschedule")
        # Hold the earliest time found, until that false
        DATE_FOUND = False
        
        # Open options page for the specific account
        self.driver.get(self.url)
        # Get into the reschedule page
        self.driver.find_element(By.XPATH, "/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[3]/a").click()
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[3]/div/div/div[2]/p[2]/a"))).click()
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/main/div[4]/div/div/form/fieldset/ol/fieldset/div/div[2]/div[3]/li'))).click()
        
        # Iterate over the dates table to find free date
        dates_table = self.driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/table")
        DATE_FOUND = self.find_date(dates_table)
        
        while DATE_FOUND == False:
            self.driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div/a").click()
            dates_table = self.driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/table/tbody")
            output = self.find_date(dates_table)
            if output is not False:
                suggested_date, suggested_date_web_object= output
                DATE_FOUND = True

        print("Earlier date found: {}".format(suggested_date.date()))

        # If the suggested time is sooner than the original
        if suggested_date.date() < self.current_date.date():

            # Pick the new date
            suggested_date_web_object.click()

            # Choose the earliest hour possible
            select = Select(self.driver.find_element(By.ID, 'appointments_consulate_appointment_time'))
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/main/div[4]/div/div/form/fieldset/ol/fieldset/div/div[2]/div[3]/li/select/option[2]")))
            select.select_by_index(1)
            # Don't remove comment until the product is ready for tests!!!
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.ID, "appointments_submit"))).click()
            print("The meeting was postponed to: {}".format(suggested_date.date()))

        else:
            print("Not updated. Current time: {}, suggested time: {}".format(self.current_date.date(), suggested_date.date()))


    def find_date(self, table):
        """
        Get dates table and return what is the earliest free date

        Arguments:
        :table: (selenium web object) month table

        :returns:
        :date: (datetime) earliest free date
        :date_object: (selenium web object) day feild in table
        """
        print("find_date")
        free_dates = table.find_elements(By.XPATH, "//td[@data-handler='selectDay']")
        for date_object in free_dates:
            year = date_object.get_attribute("data-year")
            month = int(date_object.get_attribute("data-month")) + 1
            day = date_object.find_element(By.CLASS_NAME, "ui-state-default").text
            date_string = "{}/{}/{} 10:00:00".format(day,month,year)
            date = datetime.strptime(date_string, '%d/%m/%Y %H:%M:%S')
            return date, date_object

        return False
    

if __name__ == '__main__':
    print("I'm starting")
    robot = Account("afikbh229@gmail.com","Afikbh229")