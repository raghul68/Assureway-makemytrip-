import pytest
from details_page import DetailsPage
import logging

logger = logging.getLogger(__name__)

def test_flight_details(driver):
    logger.info("Starting test_flight_details")
    page = DetailsPage(driver)
    page.open()
    page.close_login_popup()
    
    page.perform_search("flight")
    page.select_first_result("flight")
    
    details = page.get_details("flight")
    assert "airline" in details and details["airline"], "Airline name should be present"
    assert "price" in details and details["price"], "Price should be present"
    assert "timing" in details and details["timing"], "Timing should be present"
    logger.info("test_flight_details passed successfully")

def test_hotel_details(driver):
    logger.info("Starting test_hotel_details")
    page = DetailsPage(driver)
    page.open()
    page.close_login_popup()
    
    page.perform_search("hotel")
    page.select_first_result("hotel")
    
    details = page.get_details("hotel")
    assert "name" in details and details["name"], "Hotel name should be present"
    assert "price" in details and details["price"], "Price should be present"
    assert "rating" in details and details["rating"], "Rating should be present"
    logger.info("test_hotel_details passed successfully")

def test_bus_details(driver):
    logger.info("Starting test_bus_details")
    page = DetailsPage(driver)
    page.open()
    page.close_login_popup()
    
    page.perform_search("bus")
    page.select_first_result("bus")
    
    details = page.get_details("bus")
    assert "operator" in details and details["operator"], "Operator name should be present"
    assert "timing" in details and details["timing"], "Timing should be present"
    assert "price" in details and details["price"], "Price should be present"
    logger.info("test_bus_details passed successfully")
