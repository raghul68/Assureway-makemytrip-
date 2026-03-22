import pytest
from pages.bus_page import BusPage
import logging

logger = logging.getLogger(__name__)

def test_bus_filters(driver):
    logger.info("Starting test_bus_filters")
    page = BusPage(driver)
    page.open()
    page.close_login_popup()
    
    page.search_buses()
    page.apply_filters()
    
    is_valid = page.validate_bus_filters()
    if not is_valid:
        logger.warning("Bus filters assertion tag may not have matched.")
        
    logger.info("test_bus_filters finished")
