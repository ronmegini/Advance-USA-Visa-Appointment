from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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
        self.driver.get("https://ais.usvisa-info.com/he-il/niv/users/sign_in")
        email_field = self.driver.find_element(By.ID, "user_email")
        email_field.send_keys(self.email)
        password_field = self.driver.find_element(By.ID, "user_password")
        password_field.send_keys(self.password)
        policy_field = self.driver.find_element(By.ID, "policy_confirmed")
        actions = ActionChains(self.driver)
        actions.move_to_element(policy_field).perform()
        self.driver.execute_script("arguments[0].click();", policy_field)
        submit = self.driver.find_element(By.NAME, "commit").click()


    def parse_date(self, raw_string):
        """
        Extract date and location from string

        :date: (str) raw location and date string

        :returns:
        :date: (datetime) date of the original appointment
        :location: (str) Tel Aviv or Jerusalem
        """
        
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

        customers_details = []
        customers = self.driver.find_elements(By.CSS_SELECTOR, ".application.attend_appointment.card.success")
        for customer in customers:
            url = customer.find_element(By.CSS_SELECTOR, ".button.primary.small").get_attribute("href")
            current_appointment = customer.find_element(By.CLASS_NAME, "consular-appt").text
            name = customer.find_element(By.XPATH, "./table[@class='medium-12 columns margin-bottom-20']/tbody/tr/td[1]").text
            current_date,location = self.parse_date(current_appointment)

            print("Name: {}, Date: {}, Location: {}, URL: {}".format(name,current_date,location,url))
            customers_details.append({"name": name, "date": current_date, "location":location, "url":url})
        return(customers_details)


    def reschedule_customers(self, customers):
        for customer in customers:
            Customer(self.driver, customer["name"], customer["date"], customer["location"], customer["url"])


class Customer():
    def __init__(self, driver, name, date, location, url):
        # attributes
        self.driver = driver
        self.name = name
        self.date = date
        self.location = location
        self.url = url

        #functions
        self.reschedule()
    

    def reschedule(self):
        
        DATE_FOUND = False
        
        self.driver.get(self.url)
        self.driver.find_element(By.XPATH, "/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[3]/a").click()
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[3]/div/div/div[2]/p[2]/a")))
        self.driver.find_element(By.XPATH, "/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[3]/div/div/div[2]/p[2]/a").click()
        
        
        # V under delelopment V
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH('//a[contains(@href,"#select")]'))))
        print(self.driver.find_element(By.XPATH('//a[contains(@href,"#select")]')))
        dates_table = self.driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/table")
        self.find_date(dates_table)
        #while DATE_FOUND == False:
        #    dates_table = self.driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/table/")
        #    self.find_date(dates_table)

    def find_date(self, table):
        free_dates = table.find_elements(By.XPATH("//td[@_data-handler='selectDay']"))
        for date in free_dates:
            year = date.get_attribute("data-year")
            month = date.get_attribute("data-month")
            day = date.find_elements(By.CLASS_NAME("ui-state-default")).text
            print("Free date: year={}, month={}, day={}".format(year,month,day))
        return None


        

#<td class=" undefined" data-handler="selectDay" data-event="click" data-month="3" data-year="2023"><a class="ui-state-default" href="#">27</a></td>


if __name__ == '__main__':
    robot = Account("afikbh229@gmail.com","***********")
