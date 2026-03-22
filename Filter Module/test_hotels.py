import pytest
from hotel_filter_page import HotelFilterPage
import logging

logger = logging.getLogger(__name__)

def test_hotel_filter_and_sort(driver):
    logger.info("Starting test_hotel_filter_and_sort")
    page = HotelFilterPage(driver)
    
    page.open()
    page.close_login_popup()
    
    page.search_hotels()
    page.apply_rating_filter()
    page.sort_hotels_by_price()
    
    is_valid = page.validate_filter_applied()
    assert is_valid, "Hotel filters or sorting were not successfully applied!"
    logger.info("test_hotel_filter_and_sort passed successfully")
