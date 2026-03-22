from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class BusPage(BasePage):
    BUSSES_MENU = (By.XPATH, "//li[contains(@class, 'menu_Buses')]")
    SEARCH_BTN = (By.XPATH, "//a[contains(@class,'primaryBtn')] | //button[contains(@class,'primaryBtn')]")
    AC_FILTER = (By.XPATH, "//li[contains(@class, 'busTypeItem') and contains(., 'AC')] | //label[contains(.,'AC')]")
    SLEEPER_FILTER = (By.XPATH, "//li[contains(@class, 'busTypeItem') and contains(., 'Sleeper')] | //label[contains(.,'Sleeper')]")

    def search_buses(self):
        self.click_element(self.BUSSES_MENU)
        self.click_element(self.SEARCH_BTN)
        self.logger.info("Bus search initiated")

    def apply_filters(self):
        time.sleep(3)
        self.logger.info("Applying AC and Sleeper filters")
        self.click_element(self.AC_FILTER)
        time.sleep(1)
        self.click_element(self.SLEEPER_FILTER)
        
    def validate_bus_filters(self):
        tags = self.get_text((By.XPATH, "//*[contains(text(), 'Clear All')] | //*[contains(@class, 'appliedFilter')]"))
        return tags is not None
