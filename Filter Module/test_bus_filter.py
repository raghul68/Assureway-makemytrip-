import pytest
from bus_filter_page import BusFilterPage
import logging

logger = logging.getLogger(__name__)

def test_bus_filter_ac_sleeper(driver):
    logger.info("Starting test_bus_filter_ac_sleeper")
    page = BusFilterPage(driver)
    
    # 1. Open MakeMyTrip
    page.open()
    page.close_login_popup()
    
    # 2. Perform bus search
    page.search_buses()
    
    # 3. Apply AC and Sleeper filter
    page.apply_ac_sleeper_filters()
    
    # 4. Validate filtered results
    is_valid = page.validate_filter_applied()
    
    assert is_valid, "Bus filters (AC/Sleeper) were not successfully applied!"
    logger.info("test_bus_filter_ac_sleeper passed successfully")
