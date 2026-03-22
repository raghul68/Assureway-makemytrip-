import pytest
from flight_filter_page import FlightFilterPage
import logging

logger = logging.getLogger(__name__)

def test_flight_filter(driver):
    logger.info("Starting test_flight_filter")
    page = FlightFilterPage(driver)
    
    page.open()
    page.close_login_popup()
    
    page.search_flights()
    page.apply_non_stop_filter()
    
    is_valid = page.validate_filter_applied()
    assert is_valid, "Flight filters (Non-Stop/Airline) were not successfully applied!"
    logger.info("test_flight_filter passed successfully")
