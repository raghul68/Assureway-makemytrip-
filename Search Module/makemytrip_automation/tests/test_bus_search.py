"""
tests/test_bus_search.py
========================
Pytest test cases for MakeMyTrip Bus Search functionality.

Scenarios covered:
  TC_BUS_001 — Valid bus search (from config data)
  TC_BUS_002 — Bus search for Hyderabad → Bangalore
  TC_BUS_003 — URL validation after bus search
"""

import pytest

from pages.home_page import HomePage
from pages.bus_search_page import BusSearchPage
from utils.config_reader import ConfigReader
from utils.logger import get_logger

logger = get_logger(__name__)
cfg = ConfigReader()


@pytest.mark.bus
class TestBusSearch:
    """Test suite for MakeMyTrip Bus search module."""

    # ------------------------------------------------------------------ #
    # TC_BUS_001 — Valid search from config
    # ------------------------------------------------------------------ #
    @pytest.mark.smoke
    def test_valid_bus_search_from_config(self, driver):
        """
        TC_BUS_001: Verify bus search using route/date from config.yaml
        returns visible bus result cards.

        Steps:
          1. Open MakeMyTrip homepage and dismiss popup
          2. Click Buses tab
          3. Enter FROM and TO cities from config
          4. Select travel date (config offset from today)
          5. Click Search
          6. Assert bus result cards are present
        """
        logger.info("TC_BUS_001: Valid bus search from config")

        bus_data = cfg.get_bus_data()
        from_city = bus_data["from_city"]
        to_city = bus_data["to_city"]
        offset = int(bus_data.get("travel_date_offset", 5))

        home = HomePage(driver)
        home.load()
        home.click_bus_tab()

        bus_page = BusSearchPage(driver)
        travel_date = bus_page.get_future_date(offset)
        bus_page.search_bus(from_city, to_city, travel_date)

        assert bus_page.are_results_displayed(), (
            f"Expected bus results for {from_city} → {to_city} "
            f"on {bus_page.format_date(travel_date)}"
        )
        logger.info("TC_BUS_001 PASSED ✓")

    # ------------------------------------------------------------------ #
    # TC_BUS_002 — Hyderabad → Bangalore route
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    def test_bus_search_hyderabad_to_bangalore(self, driver):
        """
        TC_BUS_002: Search buses from Hyderabad to Bangalore
        for a date 7 days in future and verify results.

        Steps:
          1. Load homepage, click Buses tab
          2. Search HYD → BLR with +7 days offset
          3. Verify result count > 0
        """
        logger.info("TC_BUS_002: Bus search HYD → BLR")

        home = HomePage(driver)
        home.load()
        home.click_bus_tab()

        bus_page = BusSearchPage(driver)
        travel_date = bus_page.get_future_date(7)
        bus_page.search_bus("Hyderabad", "Bangalore", travel_date)

        count = bus_page.get_result_count()
        assert count > 0, f"Expected > 0 bus results (HYD → BLR), got {count}"
        logger.info("TC_BUS_002 PASSED ✓ | Buses found: %d", count)

    # ------------------------------------------------------------------ #
    # TC_BUS_003 — URL validation
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    def test_bus_search_url_validation(self, driver):
        """
        TC_BUS_003: Verify the URL changes to a bus-related page
        after submitting the bus search form.

        Steps:
          1. Load homepage, click Buses tab
          2. Perform bus search Bangalore → Chennai
          3. Assert 'bus' appears in current URL
        """
        logger.info("TC_BUS_003: URL validation after bus search")

        home = HomePage(driver)
        home.load()
        home.click_bus_tab()

        bus_page = BusSearchPage(driver)
        travel_date = bus_page.get_future_date(5)
        bus_page.search_bus("Bangalore", "Chennai", travel_date)
        bus_page.wait_for_url_contains("bus", timeout=30)

        current_url = driver.current_url.lower()
        assert "bus" in current_url, (
            f"Expected 'bus' in URL, got: {current_url}"
        )
        logger.info("TC_BUS_003 PASSED ✓ | URL: %s", current_url)
