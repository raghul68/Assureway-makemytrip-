from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class DetailsPage(BasePage):
    # --- Flight Details Locators ---
    AIRLINE_NAME = (By.CSS_SELECTOR, ".airlineName, .flt-info b")
    FLIGHT_TIMING = (By.CSS_SELECTOR, ".timeInfo, .flight-time")
    FLIGHT_PRICE = (By.CSS_SELECTOR, ".font24.blackFont, .actualPrice")

    # --- Hotel Details Locators ---
    HOTEL_NAME = (By.ID, "detpg_hotel_name")
    HOTEL_PRICE = (By.ID, "detpg_headerright_book_now") # The button often has price
    HOTEL_RATING = (By.CSS_SELECTOR, ".ratingStar, .hotelRating")
    HOTEL_LOCATION = (By.ID, "detpg_hotel_location")

    # --- Bus Details Locators ---
    BUS_OPERATOR = (By.CSS_SELECTOR, ".busName, .op-name")
    BUS_TIMING = (By.CSS_SELECTOR, ".busTiming, .time-info")
    BUS_PRICE = (By.CSS_SELECTOR, ".busPrice, .fare-info")

    def __init__(self, driver):
        super().__init__(driver)

    # Validations for Flight
    def get_flight_details(self):
        time.sleep(3)
        details = {
            "airline": self.get_text(self.AIRLINE_NAME),
            "timing": self.get_text(self.FLIGHT_TIMING),
            "price": self.get_text(self.FLIGHT_PRICE)
        }
        self.logger.info(f"Flight Details Found: {details}")
        return details

    # Validations for Hotel
    def get_hotel_details(self):
        time.sleep(3)
        details = {
            "name": self.get_text(self.HOTEL_NAME),
            "price": self.get_text((By.CSS_SELECTOR, "#detpg_cart_total, .priceText, .hp-price-tag")),
            "rating": self.get_text(self.HOTEL_RATING),
            "location": self.get_text(self.HOTEL_LOCATION)
        }
        self.logger.info(f"Hotel Details Found: {details}")
        return details

    # Validations for Bus
    def get_bus_details(self):
        time.sleep(3)
        details = {
            "operator": self.get_text(self.BUS_OPERATOR),
            "timing": self.get_text(self.BUS_TIMING),
            "price": self.get_text(self.BUS_PRICE)
        }
        self.logger.info(f"Bus Details Found: {details}")
        return details
