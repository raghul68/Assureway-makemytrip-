from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import time

class BookingPage(BasePage):
    """Page Object for Booking flow."""
    
    # Locators
    BOOK_NOW_BTN = (By.XPATH, "(//button[contains(text(),'Book Now') or contains(text(),'BOOK NOW')])[1]")
    CONTINUE_BTN = (By.XPATH, "//button[contains(text(),'Continue')]")
    # Booking page headers can vary; handle multiple possibilities
    BOOKING_HEADERS = [
        (By.XPATH, "//h2[contains(text(),'Complete your booking')]"),
        (By.XPATH, "//h2[contains(text(),'Review your booking')]"),
        (By.XPATH, "//div[contains(@class,'review_header')]")
    ]
    SUMMARY_DETAILS = (By.CSS_SELECTOR, ".fareSmry-sctn")
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def click_book_now(self):
        """Clicks Book Now and switches to the new tab that opens."""
        try:
            current_windows = self.driver.window_handles
            self.click_element(self.BOOK_NOW_BTN)
            
            # Wait for new window to open
            max_wait = 10
            while len(self.driver.window_handles) == len(current_windows) and max_wait > 0:
                time.sleep(1)
                max_wait -= 1
            
            # Switch to new tab if booking opens in a new tab
            if len(self.driver.window_handles) > len(current_windows):
                new_window = [w for w in self.driver.window_handles if w not in current_windows][0]
                self.driver.switch_to.window(new_window)
                print("Switched to booking tab.")
                time.sleep(3)
        except Exception as e:
            print(f"Failed to initiate booking: {e}")
            
    def is_booking_page_displayed(self):
        """Validates if the booking checkout page is loaded."""
        for locator in self.BOOKING_HEADERS:
            try:
                if self.is_element_displayed(locator):
                    return True
            except:
                continue
        return False
            
    def get_booking_summary(self):
        """Gets text of the booking summary details block."""
        try:
            summary = self.wait_for_element_visible(self.SUMMARY_DETAILS)
            if summary:
                print(f"Booking Summary Found: {summary.text[:50]}...")
                return summary.text
            return ""
        except:
            return ""

