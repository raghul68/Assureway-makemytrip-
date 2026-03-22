import pytest
from main_page import MainPage

def test_flight_search(driver):
    """Flight: Search and Validate Price."""
    main_page = MainPage(driver)
    main_page.open_module("flight")
    # Use standard cities DEL and BOM for stability inSuggestions
    main_page.search_flight("Delhi", "Mumbai")
    assert main_page.validate_flight_price(), "Flight prices are not displayed in search results."

def test_hotel_search(driver):
    """Hotel: Search and Validate Name/Price."""
    main_page = MainPage(driver)
    main_page.open_module("hotel")
    main_page.search_hotel("Goa")
    hotel_name, hotel_price = main_page.get_hotel_details()
    assert hotel_name is not None and len(hotel_name) > 0, "Hotel name not found."
    assert hotel_price is not None and len(hotel_price) > 0, "Hotel price not found."
    print(f"Hotel Result: {hotel_name} at price {hotel_price}")

def test_bus_search(driver):
    """Bus: Search and Validate Operator/Price."""
    main_page = MainPage(driver)
    main_page.open_module("bus")
    main_page.search_bus("Delhi", "Chandigarh")
    operator_name, bus_price = main_page.get_bus_details()
    assert operator_name is not None and len(operator_name) > 0, "Bus operator name not found."
    assert bus_price is not None and len(bus_price) > 0, "Bus price not found."
    print(f"Bus Result: {operator_name} at price {bus_price}")
