from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import time

class DetailsPage(BasePage):
    """Page Object for extracting search result details on MakeMyTrip."""
    
    # Locators for Flight/Hotel Search Results
    FIRST_RESULT_CARD = (By.CSS_SELECTOR, ".listingCard, .hotelCard")
    VIEW_PRICES_BTN = (By.XPATH, "(//button[contains(text(),'View Prices') or contains(text(),'VIEW PRICES') or contains(text(),'Book Now')])[1]")
    
    # Result Details Locators (Flight specific example)
    AIRLINE_NAME = (By.CSS_SELECTOR, ".airlineName")
    FLIGHT_PRICE = (By.CSS_SELECTOR, ".priceSection .blackText, .hotelPrice")
    FLIGHT_TIMING = (By.CSS_SELECTOR, ".timingOption, .checkInDate")
    
    # Explicit Details Panel
    FLIGHT_DETAILS_LINK = (By.XPATH, "(//span[contains(text(),'Flight Details')])[1]")
    DETAILS_CONTENT = (By.CSS_SELECTOR, ".flightDetails, .hotelDetails")
    
    # Generic container for results to ensure page has loaded
    RESULTS_CONTAINER = (By.CSS_SELECTOR, "#listing-id, .listingCard")
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def wait_for_results(self):
        """Waits for the initial results container to appear."""
        print("Waiting for search results container to appear...")
        return self.wait_for_element_visible(self.RESULTS_CONTAINER) is not None
        
    def select_first_result(self):
        """Clicks on the first result or 'View Prices' to expand it."""
        try:
            # First ensure results are even present
            if not self.wait_for_results():
                print("Results did not appear within 15s. Checking for potential error overlays.")
                return False
                
            # Try to see if View Prices is required
            view_prices = self.wait_for_element_visible(self.VIEW_PRICES_BTN)
            if view_prices:
                print("Found 'View Prices' button, clicking...")
                self.click_element(self.VIEW_PRICES_BTN)
            else:
                print("No 'View Prices' button, clicking first result card...")
                self.click_element(self.FIRST_RESULT_CARD)
            time.sleep(3)
            return True
        except Exception as e:
            print(f"Error selecting first result: {e}")
            return False
            
    def get_result_details(self):
        """Extracts Name, Price, and Timing/Itinerary details with assertive waits."""
        results = {}
        try:
            # We try to get each element
            name_el = self.wait_for_element_visible(self.AIRLINE_NAME)
            price_el = self.wait_for_element_visible(self.FLIGHT_PRICE)
            timing_el = self.wait_for_element_visible(self.FLIGHT_TIMING)
            
            # Map values with default fallbacks if scraping is blocked
            results['name'] = name_el.text if name_el else "Not found"
            results['price'] = price_el.text if price_el else "Not found"
            results['timing'] = timing_el.text if timing_el else "Not found"
            
            print(f"Scrapped Data -> Name: {results['name']} | Price: {results['price']}")
        except Exception as e:
            print(f"Scraping error: {e}")
            results['name'] = results['price'] = results['timing'] = None
            
        return results



