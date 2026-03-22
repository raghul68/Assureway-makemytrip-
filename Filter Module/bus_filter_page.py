from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time
import logging

class BusFilterPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.logger = logging.getLogger("BusFilterPage")

    BUSSES_MENU = (By.XPATH, "//li[contains(@class, 'menu_Buses')]")
    SEARCH_BTN = (By.XPATH, "//a[contains(@class,'primaryBtn')] | //button[contains(@class,'primaryBtn')]")
    AC_FILTER = (By.XPATH, "//li[contains(@class, 'busTypeItem') and contains(., 'AC')] | //label[contains(.,'AC')] | //*[text()='AC']")
    SLEEPER_FILTER = (By.XPATH, "//li[contains(@class, 'busTypeItem') and contains(., 'Sleeper')] | //label[contains(.,'Sleeper')] | //*[text()='Sleeper']")
    APPLIED_FILTER = (By.XPATH, "//*[contains(@class, 'appliedFilter')] | //*[contains(text(), 'Clear All')] | //*[contains(text(), 'AC')] | //*[contains(text(), 'Sleeper')]")
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

    def search_buses(self):
        self.click_element(self.BUSSES_MENU)
        self.click_element(self.SEARCH_BTN)
        self.logger.info("Bus search initiated")

    def apply_ac_sleeper_filters(self):
        self.logger.info("Applying AC and Sleeper filters")
        time.sleep(4) 
        self.click_element(self.AC_FILTER)
        time.sleep(2)
        self.click_element(self.SLEEPER_FILTER)
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
