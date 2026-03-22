from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class SearchResultsPage(BasePage):
    # Locators
    FLIGHT_RESULTS = (By.CSS_SELECTOR, "div.listingCard, .fli-list")
    VIEW_PRICES_BTN = (By.CSS_SELECTOR, "button.viewFareBtn, .btn-primary")
    BOOK_NOW_FLIGHT = (By.CSS_SELECTOR, "button.bookNow")
    
    HOTEL_RESULTS = (By.CSS_SELECTOR, "div.listingRow, .prmProperty")
    FIRST_HOTEL_CARD = (By.CSS_SELECTOR, "div.listingRow:first-child, .listingRow:first-of-type")
    
    BUS_RESULTS = (By.CSS_SELECTOR, "div.busCard")
    SELECT_SEATS_BTN = (By.CSS_SELECTOR, "a.select-seats")

    def __init__(self, driver):
        super().__init__(driver)

    def select_first_flight(self):
        time.sleep(8)
        self.dismiss_potential_overlays()
        # Wait for any loading overlays to disappear
        self.wait_for_invisibility_of_overlays()
        
        try:
            btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'VIEW PRICES')]")))
            self.click_element((By.XPATH, "//button[contains(.,'VIEW PRICES')]"))
        except:
            self.click_element((By.CSS_SELECTOR, ".viewFareBtn, button.btn-primary"))
        
        time.sleep(2)
        try:
            self.click_element((By.XPATH, "//button[contains(.,'BOOK NOW')]"))
        except:
            self.click_element((By.CSS_SELECTOR, "button.bookNow"))
        
        self.switch_to_new_tab()

    def select_first_hotel(self):
        time.sleep(10)
        self.dismiss_potential_overlays()
        self.wait_for_invisibility_of_overlays()
        self.click_element(self.FIRST_HOTEL_CARD)
        self.switch_to_new_tab()

    def select_first_bus(self):
        time.sleep(10)
        self.dismiss_potential_overlays()
        self.wait_for_invisibility_of_overlays()
        self.click_element(self.BUS_RESULTS)
