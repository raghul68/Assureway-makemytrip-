from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import logging
import time

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.logger = logging.getLogger(self.__class__.__name__)

    def open(self, url="https://www.makemytrip.com/"):
        self.driver.get(url)
        self.logger.info(f"Opened {url}")

    def close_login_popup(self):
        from selenium.webdriver.common.by import By
        try:
            loc = (By.CSS_SELECTOR, "span.commonModal__close, [data-cy='closeModal']")
            elem = self.wait.until(EC.element_to_be_clickable(loc))
            self.driver.execute_script("arguments[0].click();", elem)
            self.logger.info("Closed login popup.")
        except TimeoutException:
            try:
                self.driver.execute_script("document.body.click();")
            except:
                pass

    def click_element(self, locator, retries=3):
        for attempt in range(retries):
            try:
                elem = self.wait.until(EC.presence_of_element_located(locator))
                elem = self.wait.until(EC.element_to_be_clickable(locator))
                self.driver.execute_script("arguments[0].click();", elem)
                return True
            except StaleElementReferenceException:
                time.sleep(1)
            except Exception as e:
                time.sleep(1)
        self.logger.error(f"Failed to click {locator}")
        return False

    def get_text(self, locator, retries=3):
        for attempt in range(retries):
            try:
                elem = self.wait.until(EC.visibility_of_element_located(locator))
                return elem.text
            except StaleElementReferenceException:
                time.sleep(1)
            except Exception as e:
                time.sleep(1)
        return None
