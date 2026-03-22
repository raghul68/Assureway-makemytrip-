from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class ValidationPage(BasePage):
    """Page Object for input validations and error handling on MakeMyTrip."""
    
    # Locators
    SEARCH_BTN = (By.XPATH, "//a[contains(text(),'Search')]")
    SAME_CITY_ERROR = (By.CSS_SELECTOR, "[data-cy='sameCityError']")
    # Makemytrip often uses tooltips or specific error elements for empty fields
    ERROR_CONTAINER = (By.CSS_SELECTOR, ".errorMessage, .error-msg, [data-cy*='Error']")
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def trigger_validation_error(self):
        """Attempts to click search without fulfilling criteria to trigger validation UI."""
        try:
            # First ensure search button is reachable
            btn = self.wait_for_element_visible(self.SEARCH_BTN)
            if btn:
                self.click_element(self.SEARCH_BTN)
                time.sleep(2)
        except Exception as e:
            print(f"Failed to trigger search validation: {e}")
        
    def is_error_displayed(self):
        """Checks if any validation error message or same-city error is currently displayed."""
        if self.is_element_displayed(self.SAME_CITY_ERROR):
            print("Found 'Same City' error.")
            return True
            
        try:
            # Check for general error containers
            errors = self.driver.find_elements(*self.ERROR_CONTAINER)
            if any(e.is_displayed() for e in errors):
                print("Found validation error message.")
                return True
        except:
            pass
            
        return False

