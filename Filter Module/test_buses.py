import pytest
from bus_filter_page import BusFilterPage
import logging

logger = logging.getLogger(__name__)

def test_bus_filter(driver):
    logger.info("Starting test_bus_filter")
    page = BusFilterPage(driver)
    
    page.open()
    page.close_login_popup()
    
    page.search_buses()
    page.apply_ac_sleeper_filters()
    
    is_valid = page.validate_filter_applied()
    assert is_valid, "Bus filters (AC/Sleeper) were not successfully applied!"
    logger.info("test_bus_filter passed successfully")
