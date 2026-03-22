from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class FlightPage(BasePage):
    FLIGHTS_MENU = (By.XPATH, "//li[contains(@class, 'menu_Flights')]")
    SEARCH_BTN = (By.XPATH, "//a[contains(@class,'primaryBtn')] | //button[contains(@class,'primaryBtn')]")
    NON_STOP_FILTER = (By.XPATH, "//p[contains(text(), 'Non Stop')]/preceding-sibling::span | //label[contains(.,'Non Stop')]")
    AIRLINE_FILTER = (By.XPATH, "(//p[contains(text(), 'Airlines') or contains(text(), 'Airlines')]/following::label)[1]")
    PRICE_SORT = (By.XPATH, "//span[contains(text(), 'Price') and contains(@class, 'pointer')] | //span[contains(text(),'Cheapest')]")

    def search_flights(self):
        self.click_element(self.FLIGHTS_MENU)
        self.click_element(self.SEARCH_BTN)
        self.logger.info("Flight search initiated")

    def apply_filters(self):
        self.logger.info("Applying flight filters")
        # May need to wait for filters to load
        import time
        time.sleep(3)
        self.click_element(self.NON_STOP_FILTER)
        time.sleep(1)
        self.click_element(self.AIRLINE_FILTER)

    def sort_by_price(self):
        self.click_element(self.PRICE_SORT)
        self.logger.info("Sorted flights by price")
        
    def validate_filters_applied(self):
        # We can validate by checking if reset filters button appears or checking the active filters tags
        tags = self.get_text((By.XPATH, "//*[contains(@class, 'appliedFilter')] | //*[contains(text(), 'Clear')]"))
        return tags is not None
