"""
tests/test_flight_search.py
===========================
Pytest test cases for MakeMyTrip Flight Search functionality.

Scenarios covered:
  TC_FLIGHT_001 — Valid one-way flight search (DEL → BOM)
  TC_FLIGHT_002 — Search with different route (BLR → DEL)
  TC_FLIGHT_003 — Title/URL validation after flight search
"""

import pytest

from pages.home_page import HomePage
from pages.flight_search_page import FlightSearchPage
from utils.config_reader import ConfigReader
from utils.logger import get_logger

logger = get_logger(__name__)
cfg = ConfigReader()


@pytest.mark.flight
class TestFlightSearch:
    """Test suite for MakeMyTrip Flight search module."""

    # ------------------------------------------------------------------ #
    # TC_FLIGHT_001 — Valid one-way flight search from config
    # ------------------------------------------------------------------ #
    @pytest.mark.smoke
    def test_valid_flight_search_from_config(self, driver):
        """
        TC_FLIGHT_001: Verify that a valid one-way flight search
        returns results for the route defined in config.yaml.

        Steps:
          1. Open MakeMyTrip homepage
          2. Dismiss login popup if shown
          3. Click Flights tab
          4. Enter FROM and TO cities from config
          5. Select departure date (config offset from today)
          6. Click Search
          7. Assert results page is shown and flight cards are present
        """
        logger.info("TC_FLIGHT_001: Valid flight search from config")

        # Read search data from config
        flight_data = cfg.get_flight_data()
        from_city = flight_data["from_city"]
        to_city = flight_data["to_city"]
        offset = int(flight_data.get("departure_date_offset", 7))

        # Arrange
        home = HomePage(driver)
        home.load()
        home.click_flights_tab()

        # Act
        flight_page = FlightSearchPage(driver)
        depart_date = flight_page.get_future_date(offset)
        flight_page.search_flight(from_city, to_city, depart_date)

        # Assert
        assert flight_page.are_results_displayed(), (
            f"Expected flight results to be displayed for "
            f"{from_city} → {to_city} on {flight_page.format_date(depart_date)}"
        )
        logger.info("TC_FLIGHT_001 PASSED ✓")

    # ------------------------------------------------------------------ #
    # TC_FLIGHT_002 — Alternate route search (BLR → DEL)
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    def test_alternate_route_flight_search(self, driver):
        """
        TC_FLIGHT_002: Verify flight search for Bangalore → Delhi
        returns results on the search results page.

        Steps:
          1. Load homepage, dismiss popup
          2. Navigate to Flights tab
          3. Search BLR → DEL with a date 14 days ahead
          4. Verify results are visible
        """
        logger.info("TC_FLIGHT_002: Alternate route flight search BLR → DEL")

        home = HomePage(driver)
        home.load()
        home.click_flights_tab()

        flight_page = FlightSearchPage(driver)
        depart_date = flight_page.get_future_date(14)
        flight_page.search_flight("Bangalore", "Delhi", depart_date)

        assert flight_page.are_results_displayed(), (
            "Expected flight results for Bangalore → Delhi"
        )
        logger.info("TC_FLIGHT_002 PASSED ✓")

    # ------------------------------------------------------------------ #
    # TC_FLIGHT_003 — URL validation after search
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    def test_flight_search_url_contains_flights(self, driver):
        """
        TC_FLIGHT_003: Verify the URL changes to a flights-related page
        after submitting the search form.

        Steps:
          1. Load homepage
          2. Perform flight search
          3. Assert 'flights' appears in current URL
        """
        logger.info("TC_FLIGHT_003: URL should contain 'flights' after search")

        home = HomePage(driver)
        home.load()
        home.click_flights_tab()

        flight_page = FlightSearchPage(driver)
        depart_date = flight_page.get_future_date(10)
        flight_page.search_flight("Delhi", "Mumbai", depart_date)

        # Wait for URL change
        flight_page.wait_for_url_contains("flight", timeout=30)
        current_url = driver.current_url.lower()

        assert "flight" in current_url, (
            f"Expected 'flight' in URL, got: {current_url}"
        )
        logger.info("TC_FLIGHT_003 PASSED ✓ | URL: %s", current_url)
