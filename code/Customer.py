from os import times_result
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from datetime import datetime
import time




class Customer():
    """
    Object handle each customer inside the account and find the earlier appointment time

    :param driver: (driver) selenium web driver
    :param name: (str) the name of the customer
    :param current_date: (datetime) the current date
    :param location: (str) Current appointment location
    :param url: (str) action page's url
    """

    def __init__(self, driver, name, current_date, location, url, accepted_location):
        # attributes
        self.driver = driver
        self.name = name
        self.current_date = current_date
        self.location = location
        self.url = url
        if accepted_location.lower() == "tel aviv":
            self.accepted_location = ["Tel Aviv"]
        elif accepted_location.lower() == "jerusalem":
            self.accepted_location = ["Jerusalem"]
        else:
            self.accepted_location = ["Tel Aviv","Jerusalem"]
        

        # functions
        self.reschedule()
    

    def reschedule(self):
        """
        Reschedule the appointment to the earlier time possible

        :returns:
        :new_date: (datetimer) The updated date
        """

        print("--- reschedule ---")
        # Hold the earliest time found, until that false
        DATE_FOUND = False
        
        # Open options page for the specific account
        self.driver.get(self.url)
        # Get into the reschedule page
        self.driver.find_element(By.XPATH, "/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[3]/a").click()
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[3]/div/div/div[2]/p[2]/a"))).click()
        
        for location in self.accepted_location:
            
            time.sleep(1)
            print("Current location looking for: {}".format(location))
            
            # Choose location
            Select(self.driver.find_element(By.ID,'appointments_consulate_appointment_facility_id')).select_by_visible_text(location)

            # Get into free dates table
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
                #WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.ID, "appointments_submit"))).click()
                #WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div/div/a[2]"))).click()
                print("Updated - The meeting rescheduled from: {}, to: {}".format(self.current_date.date(),suggested_date.date()))
                break

            else:
                suggested_date_web_object.click()
                print("Not updated - Current time: {}, suggested time: {}".format(self.current_date.date(), suggested_date.date()))


    def find_date(self, table):
        """
        Get dates table and return what is the earliest free date

        Arguments:
        :table: (selenium web object) month table

        :returns:
        :date: (datetime) earliest free date
        :date_object: (selenium web object) day feild in table
        """ 

        print("--- find date ---")
        free_dates = table.find_elements(By.XPATH, "//td[@data-handler='selectDay']")
        for date_object in free_dates:
            year = date_object.get_attribute("data-year")
            month = int(date_object.get_attribute("data-month")) + 1
            day = date_object.find_element(By.CLASS_NAME, "ui-state-default").text
            date_string = "{}/{}/{} 10:00:00".format(day,month,year)
            date = datetime.strptime(date_string, '%d/%m/%Y %H:%M:%S')
            return date, date_object

        return False
    
