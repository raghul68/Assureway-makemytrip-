import pytest
import time
from pages.home_page import HomePage
from pages.details_page import DetailsPage

class TestMakeMyTripDetails:
    """Test Suite for checking search result details on MakeMyTrip."""

    def test_search_result_details(self, driver):
        """
        Steps:
        1. Open MakeMyTrip Home Page.
        2. Enter 'Delhi' to 'Mumbai' and select a Departure Date.
        3. Click Search and wait for Results.
        4. Select/Expand the first result.
        5. Validate: Price, Airline Name, and Timing details are displayed.
        """
        home_page = HomePage(driver)
        home_page.load()
        
        # 1. Perform a flight search
        home_page.enter_cities("Delhi", "Mumbai")
        home_page.select_departure_date()
        home_page.click_search()
        
        # 2. Results Interaction
        time.sleep(10)  # Wait for results to stabilize
        details_page = DetailsPage(driver)
        details_page.select_first_result()
        
        # 3. Validation module
        details = details_page.get_result_details()
        
        # Perform Assertions
        assert details['name'] is not None and details['name'] != "Not found", "Airline name is missing or could not be found."
        assert details['price'] is not None and details['price'] != "Not found", "Price is missing or could not be found."
        assert details['timing'] is not None and details['timing'] != "Not found", "Timing is missing or could not be found."
        
        print(f"Validation successful: '{details['name']}' at price '{details['price']}'")

