from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time
import logging

class FlightFilterPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.logger = logging.getLogger("FlightFilterPage")

    # Locators
    FLIGHTS_MENU = (By.XPATH, "//li[contains(@class, 'menu_Flights')]")
    SEARCH_BTN = (By.XPATH, "//a[contains(@class,'primaryBtn')] | //button[contains(@class,'primaryBtn')]")
    NON_STOP_FILTER = (By.XPATH, "//p[contains(text(), 'Non Stop')]/preceding-sibling::span | //label[contains(.,'Non Stop')]")
    APPLIED_FILTER = (By.XPATH, "//*[contains(@class, 'appliedFilter')] | //*[contains(text(), 'Clear All')] | //*[contains(text(), 'Non Stop')]")
    LOGIN_CLOSE = (By.CSS_SELECTOR, "span.commonModal__close, [data-cy='closeModal']")

    def open(self):
        self.driver.get("https://www.makemytrip.com/")
        
    def close_login_popup(self):
        try:
            elem = self.wait.until(EC.element_to_be_clickable(self.LOGIN_CLOSE))
            self.driver.execute_script("arguments[0].click();", elem)
        except:
            try:
                self.driver.execute_script("document.body.click();")
            except:
                pass

    def click_element(self, locator, retries=3):
        for _ in range(retries):
            try:
                elem = self.wait.until(EC.element_to_be_clickable(locator))
                self.driver.execute_script("arguments[0].click();", elem)
                return True
            except StaleElementReferenceException:
                time.sleep(1)
            except Exception:
                time.sleep(1)
        return False

    def search_flights(self):
        self.click_element(self.FLIGHTS_MENU)
        self.click_element(self.SEARCH_BTN)
        self.logger.info("Flight search initiated")

    def apply_non_stop_filter(self):
        self.logger.info("Applying non-stop flight filter")
        time.sleep(4) 
        self.click_element(self.NON_STOP_FILTER)
        time.sleep(2)

    def validate_filter_applied(self):
        for _ in range(3):
            try:
                elem = self.wait.until(EC.visibility_of_element_located(self.APPLIED_FILTER))
                if elem.text:
                    return True
            except:
                time.sleep(1)
        return False
