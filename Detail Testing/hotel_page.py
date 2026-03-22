from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class HotelPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        
    # Locators
    CLOSE_POP_BTN = (By.CSS_SELECTOR, "span.commonModal__close")
    CITY_INPUT = (By.ID, "city")
    CITY_FIELD = (By.CSS_SELECTOR, "input[placeholder='Where do you want to stay?']")
    SUGGESTION_DIV = (By.CSS_SELECTOR, ".react-autosuggest__suggestion:first-child")
    # Date
    CHECKIN = (By.ID, "checkin")
    DAY_SELECT = (By.XPATH, "(//div[contains(@class,'DayPicker-Day') and not(contains(@class,'disabled'))])[1]")
    SEARCH_BTN = (By.ID, "hlistpg_search_btn")
    # Results
    HOTEL_CARD = (By.CSS_SELECTOR, ".hotelCard, div[id*='hotel-id']")
    HOTEL_NAME = (By.ID, "hlistpg_hotel_name")
    HOTEL_PRICE = (By.ID, "hlistpg_hotel_shown_price")

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

    def enter_hotel_details(self, city):
        # City selection
        self.wait.until(EC.element_to_be_clickable(self.CITY_INPUT)).click()
        c_in = self.wait.until(EC.visibility_of_element_located(self.CITY_FIELD))
        c_in.send_keys(city)
        time.sleep(2)
        self.wait.until(EC.element_to_be_clickable(self.SUGGESTION_DIV)).click()

        # Dates (usually opens after City)
        try:
            self.wait.until(EC.element_to_be_clickable(self.DAY_SELECT)).click()
            # Click next day for checkout
            self.wait.until(EC.element_to_be_clickable(self.DAY_SELECT)).click()
        except:
            pass

    def click_search(self):
        self.wait.until(EC.element_to_be_clickable(self.SEARCH_BTN)).click()

    def get_first_hotel_info(self):
        # Results load
        card = self.wait.until(EC.visibility_of_element_located(self.HOTEL_CARD))
        self.driver.execute_script("arguments[0].scrollIntoView();", card)
        h_name = card.find_element(*self.HOTEL_NAME).text
        h_price = card.find_element(*self.HOTEL_PRICE).text
        return h_name, h_price
