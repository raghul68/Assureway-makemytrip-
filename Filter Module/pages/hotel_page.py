from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HotelPage(BasePage):
    HOTELS_MENU = (By.XPATH, "//li[contains(@class, 'menu_Hotels')]")
    SEARCH_BTN = (By.XPATH, "//a[contains(@class,'primaryBtn')] | //button[contains(@class,'primaryBtn')]")
    USER_RATING_FILTER = (By.XPATH, "//label[contains(.,'4.5 & above') or contains(.,'Excellent')]")
    PRICE_SORT = (By.XPATH, "//span[contains(text(), 'Price') or contains(text(), 'Price - Low to High')]")

    def search_hotels(self):
        self.click_element(self.HOTELS_MENU)
        self.click_element(self.SEARCH_BTN)
        self.logger.info("Hotel search initiated")

    def apply_rating_filter(self):
        import time
        time.sleep(3)
        self.logger.info("Applying hotel rating filter")
        self.click_element(self.USER_RATING_FILTER)

    def sort_hotels(self):
        self.logger.info("Sorting hotels by price")
        self.click_element(self.PRICE_SORT)
        
    def validate_features(self):
        tags = self.get_text((By.XPATH, "//*[contains(text(), 'Clear All')] | //*[contains(@class, 'appliedFilter')]"))
        return tags is not None
