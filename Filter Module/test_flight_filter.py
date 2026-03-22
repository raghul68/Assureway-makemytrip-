import pytest
from flight_filter_page import FlightFilterPage
import logging

logger = logging.getLogger(__name__)

def test_flight_filter_non_stop(driver):
    logger.info("Starting test_flight_filter_non_stop")
    page = FlightFilterPage(driver)
    
    # 1. Open MakeMyTrip
    page.open()
    page.close_login_popup()
    
    # 2. Perform flight search
    page.search_flights()
    
    # 3. Apply non-stop filter
    page.apply_non_stop_filter()
    
    # 4. Validate filtered results
    is_valid = page.validate_filter_applied()
    
    assert is_valid, "Flight filters were not successfully applied!"
    logger.info("test_flight_filter_non_stop passed successfully")
