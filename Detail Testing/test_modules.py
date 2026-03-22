import pytest
from main_page import MainPage

def test_flight_search(driver):
    """
    Flight:
    - Open makemytrip website
    - Close popup
    - Search flight (use sample cities)
    - Click first result
    - Validate price is visible
    """
    main_page = MainPage(driver)
    main_page.open()
    main_page.select_module("flight")
    main_page.search_flight("Delhi", "Mumbai")
    
    # Check flight results and visibility of prices
    assert main_page.validate_flight_price(), "Flight prices are not displayed in search results."

def test_hotel_search(driver):
    """
    Hotel:
    - Click Hotels section
    - Search hotel (sample city)
    - Click first result
    - Validate hotel name and price
    """
    main_page = MainPage(driver)
    main_page.open() # Already handles popup closing
    main_page.select_module("hotel")
    main_page.search_hotel("Goa")
    
    hotel_name, hotel_price = main_page.get_hotel_details()
    assert hotel_name is not None and len(hotel_name) > 0, "Hotel name not found."
    assert hotel_price is not None and len(hotel_price) > 0, "Hotel price not found."
    print(f"Found Hotel: {hotel_name} at price {hotel_price}")

def test_bus_search(driver):
    """
    Bus:
    - Click Bus section
    - Search bus (sample cities)
    - Click first result
    - Validate bus operator name and price
    """
    main_page = MainPage(driver)
    main_page.open()
    main_page.select_module("bus")
    main_page.search_bus("Delhi", "Chandigarh")
    
    operator_name, bus_price = main_page.get_bus_details()
    assert operator_name is not None and len(operator_name) > 0, "Bus operator name not found."
    assert bus_price is not None and len(bus_price) > 0, "Bus price not found."
    print(f"Found Bus Operator: {operator_name} at price {bus_price}")
