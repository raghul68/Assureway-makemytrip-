from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class HomePage(BasePage):
    # Locators
    LOGIN_MODAL_CLOSE = (By.CSS_SELECTOR, "span.commonModal__close")
    FLIGHTS_MENU = (By.CSS_SELECTOR, "li.menu_Flights a")
    HOTELS_MENU = (By.CSS_SELECTOR, "li.menu_Hotels a")
    BUSSES_MENU = (By.CSS_SELECTOR, "li.menu_Buses a")
    
    # Generic search locators
    SEARCH_CITY_INPUT = (By.ID, "fromCity")
    TO_CITY_INPUT = (By.ID, "toCity")
    CITY_SEARCH_FIELD = (By.CSS_SELECTOR, "input[placeholder*='From'], input[placeholder*='From City']")
    TO_CITY_SEARCH_FIELD = (By.CSS_SELECTOR, "input[placeholder*='To'], input[placeholder*='To City']")
    SUGGESTION_LIST = (By.CSS_SELECTOR, "ul.react-autosuggest__suggestions-list li")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "a.primaryBtn, button.primaryBtn")

    def __init__(self, driver):
        super().__init__(driver)

    def close_login_popup(self):
        time.sleep(2)
        self.dismiss_potential_overlays()
        # More aggressive dismissal
        try:
            self.driver.execute_script("document.body.click();")
        except: pass

    def select_module(self, module_name):
        self.dismiss_potential_overlays()
        locators = {
            "flights": (By.CSS_SELECTOR, "li.menu_Flights a"),
            "hotels": (By.CSS_SELECTOR, "li.menu_Hotels a"),
            "buses": (By.CSS_SELECTOR, "li.menu_Buses a")
        }
        self.click_element(locators.get(module_name.lower(), locators["flights"]))
        time.sleep(2)

    def search_flights(self, from_city, to_city):
        self.select_module("flights")
        self.dismiss_potential_overlays()
        # Click and wait for input to be interactable
        self.click_element(self.SEARCH_CITY_INPUT)
        input_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.CITY_SEARCH_FIELD)
        )
        input_field.send_keys(from_city)
        time.sleep(2)
        self.click_element(self.SUGGESTION_LIST)
        
        self.click_element(self.TO_CITY_INPUT)
        input_field_to = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.TO_CITY_SEARCH_FIELD)
        )
        input_field_to.send_keys(to_city)
        time.sleep(2)
        self.click_element(self.SUGGESTION_LIST)
        
        # Click search
        self.click_element(self.SEARCH_BUTTON)

    def search_hotels(self, city):
        self.select_module("hotels")
        self.dismiss_potential_overlays()
        self.click_element((By.ID, "city"))
        input_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder*='city']"))
        )
        input_field.send_keys(city)
        time.sleep(2)
        self.click_element(self.SUGGESTION_LIST)
        self.click_element(self.SEARCH_BUTTON)

    def search_buses(self, from_city, to_city):
        self.select_module("buses")
        self.dismiss_potential_overlays()
        self.click_element(self.SEARCH_CITY_INPUT)
        input_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.CITY_SEARCH_FIELD)
        )
        input_field.send_keys(from_city)
        time.sleep(2)
        self.click_element(self.SUGGESTION_LIST)
        
        self.click_element(self.TO_CITY_INPUT)
        input_field_to = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.TO_CITY_SEARCH_FIELD)
        )
        input_field_to.send_keys(to_city)
        time.sleep(2)
        self.click_element(self.SUGGESTION_LIST)
        
        self.click_element((By.ID, "travelDate"))
        # Just select today or next available
        self.click_element((By.CSS_SELECTOR, ".DayPicker-Day--today"))
        
        self.click_element(self.SEARCH_BUTTON)
