from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time
from selenium.webdriver.support import expected_conditions as EC

class SearchPage(BasePage):
    FROM_CITY = (By.ID, "fromCity")
    FROM_CITY_INPUT = (By.XPATH, "//input[@placeholder='From' or @title='From']")
    TO_CITY = (By.ID, "toCity")
    TO_CITY_INPUT = (By.XPATH, "//input[@placeholder='To' or @title='To']")
    SEARCH_BTN = (By.XPATH, "//a[contains(@class,'primaryBtn')] | //button[contains(@class,'primaryBtn')]")
    ERROR_MSG = (By.XPATH, "//*[contains(@class, 'errorMsg') or contains(text(), 'Please select')]")
    DATE_FIELD = (By.XPATH, "//label[@for='departure']")
    NEXT_MONTH = (By.XPATH, "//span[contains(@class, 'DayPicker-NavButton--next')]")
    AVAILABLE_DATE = (By.XPATH, "(//div[contains(@class, 'DayPicker-Day') and not(contains(@class, 'disabled')) and not(contains(@class, 'outside'))])[1]")
    MODIFY_BTN = (By.XPATH, "//*[contains(text(), 'Modify Search')] | //*[contains(@class, 'modify')]")

    def search_with_invalid_inputs(self, from_city, to_city):
        self.click_element(self.FROM_CITY)
        try:
            elem = self.wait.until(EC.element_to_be_clickable(self.FROM_CITY_INPUT))
            elem.send_keys(from_city)
            time.sleep(1)
        except:
            pass
            
        self.click_element(self.TO_CITY)
        try:
            elem = self.wait.until(EC.element_to_be_clickable(self.TO_CITY_INPUT))
            elem.send_keys(to_city)
            time.sleep(1)
        except:
            pass
            
        self.click_element(self.SEARCH_BTN)
        
    def validate_search_error(self):
        msg = self.get_text(self.ERROR_MSG)
        return msg is not None

    def validate_date_selection(self):
        self.click_element(self.DATE_FIELD)
        self.click_element(self.NEXT_MONTH)
        self.click_element(self.AVAILABLE_DATE)
        self.logger.info("Selected a valid future date.")
        date_val = self.get_text(self.DATE_FIELD)
        return date_val is not None

    def modify_search(self):
        # We assume search is already done and results are displayed
        self.click_element(self.MODIFY_BTN)
        self.click_element(self.SEARCH_BTN)
        self.logger.info("Modified search and pressed submit.")
        return True
