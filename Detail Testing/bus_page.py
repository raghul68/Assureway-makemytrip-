from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class BusPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        
    # Locators
    CLOSE_POP_BTN = (By.CSS_SELECTOR, "span.commonModal__close")
    FROM_CITY = (By.ID, "fromCity")
    # After clicking fromCity, an input box appears
    FROM_INPUT = (By.CSS_SELECTOR, "input[placeholder='From']")
    TO_CITY = (By.ID, "toCity")
    TO_INPUT = (By.CSS_SELECTOR, "input[placeholder='To']")
    # Suggestion
    SUGGESTION_ITEM = (By.CSS_SELECTOR, ".react-autosuggest__suggestion:first-child")
    # Date
    TRAVEL_DATE = (By.ID, "travelDate")
    DAY_SELECT = (By.XPATH, "(//div[contains(@class,'DayPicker-Day') and not(contains(@class,'disabled'))])[1]")
    # Search
    SEARCH_BTN = (By.ID, "search_button")
    # Results
    BUS_CARD = (By.XPATH, "//div[contains(@class, 'busCard')]")
    OPERATOR_NAME = (By.XPATH, ".//p[contains(@class,'makeFlex')]/span[1]")
    PRICE = (By.ID, "price")

    def open_url(self, url):
        self.driver.get(url)

    def close_popup_if_exists(self):
        try:
            # Short wait for popup
            time.sleep(2)
            close = self.driver.find_element(*self.CLOSE_POP_BTN)
            close.click()
            print("Login popup closed.")
        except:
            print("No login popup detected.")
            # Click body to dismiss any overlays
            try: self.driver.find_element(By.TAG_NAME, "body").click()
            except: pass

    def enter_bus_details(self, from_city, to_city):
        # From City
        self.wait.until(EC.element_to_be_clickable(self.FROM_CITY)).click()
        f_in = self.wait.until(EC.visibility_of_element_located(self.FROM_INPUT))
        f_in.send_keys(from_city)
        time.sleep(2)
        self.wait.until(EC.element_to_be_clickable(self.SUGGESTION_ITEM)).click()

        # To City
        self.wait.until(EC.element_to_be_clickable(self.TO_CITY)).click()
        t_in = self.wait.until(EC.visibility_of_element_located(self.TO_INPUT))
        t_in.send_keys(to_city)
        time.sleep(2)
        self.wait.until(EC.element_to_be_clickable(self.SUGGESTION_ITEM)).click()

        # Select Date (usually opens after To City)
        try:
            self.wait.until(EC.element_to_be_clickable(self.DAY_SELECT)).click()
        except:
            pass

    def click_search(self):
        self.wait.until(EC.element_to_be_clickable(self.SEARCH_BTN)).click()

    def get_first_bus_info(self):
        # Results load
        card = self.wait.until(EC.visibility_of_element_located(self.BUS_CARD))
        self.driver.execute_script("arguments[0].scrollIntoView();", card)
        op_name = card.find_element(*self.OPERATOR_NAME).text
        price = card.find_element(*self.PRICE).text
        return op_name, price
