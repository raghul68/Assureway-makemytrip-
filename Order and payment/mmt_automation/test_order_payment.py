import pytest
import json
from order_payment_page import MMTPage

import os

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path) as f:
        return json.load(f)

@pytest.fixture
def config():
    return load_config()

@pytest.mark.usefixtures("driver")
class TestMMTBooking:

    def test_booking_and_payment_flow(self, driver, config):
        mmt = MMTPage(driver)
        
        # 1. Open makemytrip website
        driver.get(config['baseUrl'])
        
        # 2. Close popup
        mmt.close_popup()
        
        # 3. Perform flight search (use cities from config)
        mmt.search_flights(config['search']['from'], config['search']['to'])
        
        # 4. Click first result and Book Now
        mmt.select_first_flight()
        
        # 5. Validate booking/order page is displayed
        # Moving to Booking page switch window/tab
        driver.switch_to.window(driver.window_handles[-1])
        assert "Review Your Booking" in driver.title or "Flight" in driver.title
        
        # 6. Fill details and continue to payment page
        mmt.fill_traveler_details(config['traveler'])
        
        # 7. Validate: Price is displayed
        price = mmt.get_price()
        assert price != ""
        print(f"Total Price: {price}")
        
        # 8. Validate: Payment options (UPI/Card) are visible
        assert mmt.are_payment_options_visible()
        print("Payment options are visible.")

