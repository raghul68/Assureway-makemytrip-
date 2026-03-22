from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class FlightDetailsPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)

    # Locators
    LOGIN_CLOSE = (By.CSS_SELECTOR, "span.commonModal__close, [data-cy='closeModal']")
    FLIGHTS_MENU = (By.CSS_SELECTOR, "li.menu_Flights")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "a.primaryBtn, button.primaryBtn")
    
    VIEW_PRICES_BTN = (By.XPATH, "//button[contains(.,'VIEW PRICES')]")
    BOOK_NOW_BTN = (By.XPATH, "//button[contains(.,'BOOK NOW')]")
    VIEW_FARE_BTN = (By.CSS_SELECTOR, ".viewFareBtn, button.bookNow")
    
    # Details locators
    AIRLINE_NAME = (By.CSS_SELECTOR, ".airlineName, .flt-info b")
    FLIGHT_TIMING = (By.CSS_SELECTOR, ".timeInfo, .flight-time")
    FLIGHT_PRICE = (By.CSS_SELECTOR, ".font24.blackFont, .actualPrice")

    def open(self):
        self.driver.get("https://www.makemytrip.com/")

    def close_login_popup(self):
        time.sleep(3)
        try:
            btn = self.driver.find_element(*self.LOGIN_CLOSE)
            btn.click()
        except:
            # Fallback for overlays
            self.driver.execute_script("document.body.click();")

    def search_flights(self):
        # Click flights menu
        self.wait.until(EC.element_to_be_clickable(self.FLIGHTS_MENU)).click()
        time.sleep(2)
        # Using default cities (Delhi to Mumbai usually) and click search
        self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON)).click()

    def click_first_result(self):
        time.sleep(8) # Wait for search results
        try:
            # Handle possible variations in MMT layout
            btn = self.wait.until(EC.element_to_be_clickable(self.VIEW_PRICES_BTN))
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(2)
            book_btn = self.wait.until(EC.element_to_be_clickable(self.BOOK_NOW_BTN))
            self.driver.execute_script("arguments[0].click();", book_btn)
        except:
            view_fare = self.wait.until(EC.element_to_be_clickable(self.VIEW_FARE_BTN))
            self.driver.execute_script("arguments[0].click();", view_fare)
            
        time.sleep(3)
        # Switch to new tab if a new tab is opened
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])

    def get_flight_details(self):
        time.sleep(5) # Wait for details page to render
        airline = self.wait.until(EC.presence_of_element_located(self.AIRLINE_NAME)).text
        timing = self.wait.until(EC.presence_of_element_located(self.FLIGHT_TIMING)).text
        price = self.wait.until(EC.presence_of_element_located(self.FLIGHT_PRICE)).text
        
        return {
            "airline": airline,
            "timing": timing,
            "price": price
        }
