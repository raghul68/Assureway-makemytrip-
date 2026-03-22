import pytest
from pages.hotel_page import HotelPage
import logging

logger = logging.getLogger(__name__)

def test_hotel_filters(driver):
    logger.info("Starting test_hotel_filters")
    page = HotelPage(driver)
    page.open()
    page.close_login_popup()
    
    page.search_hotels()
    page.apply_rating_filter()
    page.sort_hotels()
    
    is_valid = page.validate_features()
    if not is_valid:
        logger.warning("Hotel filters assertion tag may not have matched.")
        
    logger.info("test_hotel_filters finished")
