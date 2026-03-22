import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.details_page import DetailsPage
import time

class TestMakeMyTripDetails:

    @pytest.mark.flights
    def test_flight_details(self, driver):
        home = HomePage(driver)
        results = SearchResultsPage(driver)
        details = DetailsPage(driver)

        home.close_login_popup()
        home.search_flights("Mumbai", "Delhi")
        
        results.select_first_flight()
        
        flight_info = details.get_flight_details()
        
        # Validations
        assert flight_info["airline"] is not None, "Airline name should be displayed"
        assert flight_info["timing"] is not None, "Flight timing should be displayed"
        assert flight_info["price"] is not None, "Flight price should be displayed"

    @pytest.mark.hotels
    def test_hotel_details(self, driver):
        home = HomePage(driver)
        results = SearchResultsPage(driver)
        details = DetailsPage(driver)

        home.close_login_popup()
        home.search_hotels("Mumbai")
        
        results.select_first_hotel()
        
        hotel_info = details.get_hotel_details()
        
        # Validations
        assert hotel_info["name"] is not None, "Hotel name should be displayed"
        assert hotel_info["price"] is not None, "Hotel price should be displayed"
        assert hotel_info["rating"] is not None, "Hotel rating should be displayed"

    @pytest.mark.buses
    def test_bus_details(self, driver):
        home = HomePage(driver)
        results = SearchResultsPage(driver)
        details = DetailsPage(driver)

        home.close_login_popup()
        home.search_buses("Mumbai", "Pune")
        
        results.select_first_bus()
        
        bus_info = details.get_bus_details()
        
        # Validations
        assert bus_info["operator"] is not None, "Bus operator name should be displayed"
        assert bus_info["timing"] is not None, "Departure and arrival timing should be displayed"
        assert bus_info["price"] is not None, "Ticket price should be displayed"
