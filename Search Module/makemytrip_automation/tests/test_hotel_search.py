"""
tests/test_hotel_search.py
==========================
Pytest test cases for MakeMyTrip Hotel Search functionality.

Scenarios covered:
  TC_HOTEL_001 — Valid hotel search (from config data)
  TC_HOTEL_002 — Hotel search for Mumbai
  TC_HOTEL_003 — URL validation after hotel search
"""

import pytest

from pages.home_page import HomePage
from pages.hotel_search_page import HotelSearchPage
from utils.config_reader import ConfigReader
from utils.logger import get_logger

logger = get_logger(__name__)
cfg = ConfigReader()


@pytest.mark.hotel
class TestHotelSearch:
    """Test suite for MakeMyTrip Hotel search module."""

    # ------------------------------------------------------------------ #
    # TC_HOTEL_001 — Valid search from config
    # ------------------------------------------------------------------ #
    @pytest.mark.smoke
    def test_valid_hotel_search_from_config(self, driver):
        """
        TC_HOTEL_001: Verify hotel search using city/dates from config.yaml
        returns visible hotel result cards.

        Steps:
          1. Open MakeMyTrip homepage and dismiss popup
          2. Click Hotels tab
          3. Enter city, check-in, check-out from config
          4. Click Search
          5. Assert hotel cards are present on results page
        """
        logger.info("TC_HOTEL_001: Valid hotel search from config")

        hotel_data = cfg.get_hotel_data()
        city = hotel_data["city"]
        checkin_offset = int(hotel_data.get("checkin_date_offset", 7))
        checkout_offset = int(hotel_data.get("checkout_date_offset", 9))
        rooms = int(hotel_data.get("rooms", 1))
        adults = int(hotel_data.get("adults", 2))

        home = HomePage(driver)
        home.load()
        home.click_hotels_tab()

        hotel_page = HotelSearchPage(driver)
        checkin = hotel_page.get_future_date(checkin_offset)
        checkout = hotel_page.get_future_date(checkout_offset)

        hotel_page.search_hotel(city, checkin, checkout, rooms, adults)

        assert hotel_page.are_results_displayed(), (
            f"Expected hotel results for '{city}' "
            f"({hotel_page.format_date(checkin)} — {hotel_page.format_date(checkout)})"
        )
        logger.info("TC_HOTEL_001 PASSED ✓")

    # ------------------------------------------------------------------ #
    # TC_HOTEL_002 — Mumbai hotel search
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    def test_hotel_search_mumbai(self, driver):
        """
        TC_HOTEL_002: Search hotels in Mumbai for a 3-night stay
        and verify results are displayed.

        Steps:
          1. Open homepage, click Hotels tab
          2. Search Mumbai with check-in +10, check-out +13 days
          3. Verify result count > 0
        """
        logger.info("TC_HOTEL_002: Hotel search for Mumbai")

        home = HomePage(driver)
        home.load()
        home.click_hotels_tab()

        hotel_page = HotelSearchPage(driver)
        checkin = hotel_page.get_future_date(10)
        checkout = hotel_page.get_future_date(13)

        hotel_page.search_hotel("Mumbai", checkin, checkout, rooms=1, adults=2)

        count = hotel_page.get_result_count()
        assert count > 0, f"Expected > 0 hotel results for Mumbai, got {count}"
        logger.info("TC_HOTEL_002 PASSED ✓ | Hotels found: %d", count)

    # ------------------------------------------------------------------ #
    # TC_HOTEL_003 — URL validation
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    def test_hotel_search_url_validation(self, driver):
        """
        TC_HOTEL_003: Verify URL changes to a hotels-related page
        after submitting the search form.

        Steps:
          1. Load homepage, click Hotels tab
          2. Perform hotel search for Goa
          3. Assert 'hotel' appears in URL
        """
        logger.info("TC_HOTEL_003: URL validation after hotel search")

        home = HomePage(driver)
        home.load()
        home.click_hotels_tab()

        hotel_page = HotelSearchPage(driver)
        checkin = hotel_page.get_future_date(7)
        checkout = hotel_page.get_future_date(10)

        hotel_page.search_hotel("Goa", checkin, checkout)
        hotel_page.wait_for_url_contains("hotel", timeout=30)

        current_url = driver.current_url.lower()
        assert "hotel" in current_url, (
            f"Expected 'hotel' in URL, got: {current_url}"
        )
        logger.info("TC_HOTEL_003 PASSED ✓ | URL: %s", current_url)
