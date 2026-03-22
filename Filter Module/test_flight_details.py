import pytest
from flight_details_page import FlightDetailsPage

def test_flight_details(driver):
    flight_page = FlightDetailsPage(driver)
    
    flight_page.open()
    flight_page.close_login_popup()
    flight_page.search_flights()
    flight_page.click_first_result()
    
    details = flight_page.get_flight_details()
    
    assert details["airline"], "Airline name is missing"
    assert details["timing"], "Flight timing is missing"
    assert details["price"], "Flight price is missing"
    
    print(f"\nSuccessfully validated flight details: {details}")
