"""
pages/flight_search_page.py
FlightSearchPage — automates the Flights search workflow on MakeMyTrip.
"""

import time
from datetime import datetime

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.flight_locators import FlightLocators
from pages.base_page import BasePage
from utils.config_reader import ConfigReader
from utils.logger import get_logger

cfg = ConfigReader()
logger = get_logger(__name__)


class FlightSearchPage(BasePage):
    """
    Encapsulates all interactions on the MakeMyTrip flight search section.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.loc = FlightLocators

    # ------------------------------------------------------------------ #
    # High-level action: perform a complete flight search
    # ------------------------------------------------------------------ #

    def search_flight(self, from_city: str, to_city: str, depart_date: datetime) -> None:
        """
        Perform a one-way flight search end-to-end.

        Args:
            from_city:   Departure city (e.g. 'Delhi')
            to_city:     Arrival city (e.g. 'Mumbai')
            depart_date: Python datetime for the departure date
        """
        logger.info("=== Starting Flight Search ===")
        logger.info("Route: %s → %s | Date: %s", from_city, to_city,
                    self.format_date(depart_date))

        self._enter_from_city(from_city)
        self._enter_to_city(to_city)
        self._select_departure_date(depart_date)
        self._click_search()
        logger.info("Flight search submitted.")

    # ------------------------------------------------------------------ #
    # Step methods
    # ------------------------------------------------------------------ #

    def _enter_from_city(self, city: str) -> None:
        logger.info("Entering FROM city: %s", city)
        # Try clicking the "From" field box first
        from_clicked = self._click_city_field(
            [self.loc.FROM_FIELD, self.loc.FROM_FIELD_V2], label="FROM"
        )

        # Type in the search box that appears
        try:
            field = self.find_visible(self.loc.FROM_INPUT, timeout=10)
            field.clear()
            field.send_keys(city)
        except TimeoutException:
            logger.warning("FROM input not found after field click; typing directly")
            self.type_text(self.loc.FROM_FIELD_V2, city)

        self._select_from_suggestion(city)

    def _enter_to_city(self, city: str) -> None:
        logger.info("Entering TO city: %s", city)
        self._click_city_field(
            [self.loc.TO_FIELD, self.loc.TO_FIELD_V2], label="TO"
        )
        try:
            field = self.find_visible(self.loc.TO_INPUT, timeout=10)
            field.clear()
            field.send_keys(city)
        except TimeoutException:
            self.type_text(self.loc.TO_FIELD_V2, city)

        self._select_from_suggestion(city)

    def _click_city_field(self, locators: list, label: str) -> bool:
        for loc in locators:
            try:
                self.click(loc)
                logger.debug("Clicked %s field with locator %s", label, loc)
                return True
            except Exception:
                continue
        logger.warning("Could not click %s field with any locator", label)
        return False

    def _select_from_suggestion(self, city: str) -> None:
        """Wait for auto-complete suggestions and pick the first one using click or keys."""
        logger.info("Selecting suggestion for '%s'...", city)
        time.sleep(1.2)  # Wait for API and animation
        
        # Strategy 1: Find and click the first suggestion
        try:
            # Wait for suggestion item to be present
            first = self.find_visible(self.loc.SUGGESTION_ITEM, timeout=8)
            self.click(self.loc.SUGGESTION_ITEM)
            logger.info("Successfully clicked suggestion for '%s'", city)
            return
        except Exception as e:
            logger.warning("Click on suggestion failed: %s. Trying keyboard fallback.", e)

        # Strategy 2: Keyboard navigation (Arrow Down + Enter)
        try:
            from selenium.webdriver.common.keys import Keys
            active = self.driver.switch_to.active_element
            active.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.3)
            active.send_keys(Keys.ENTER)
            logger.info("Selected suggestion for '%s' via ENTER key", city)
        except Exception as ke:
            logger.error("All suggestion selection strategies failed: %s", ke)
            raise

    def _select_departure_date(self, date: datetime) -> None:
        """Click the departure date field and pick the correct date from calendar."""
        logger.info("Selecting departure date: %s", self.format_date(date))
        # Open calendar
        for loc in [self.loc.DEPART_DATE_FIELD]:
            try:
                self.click(loc)
                break
            except Exception:
                pass

        self._pick_calendar_date(date)

    def _pick_calendar_date(self, date: datetime) -> None:
        """Navigate month-by-month in the calendar and click the desired date."""
        # Format aria-label e.g. 'Mon Apr 07 2025'
        aria_date = date.strftime("%a %b %d %Y").replace(" 0", " ")  # remove zero-pad
        date_xpath = (By.XPATH,
                      f"//div[@aria-label='{aria_date}' and not(contains(@class,'disabled'))] | "
                      f"//p[@aria-label='{aria_date}']")

        # Try to click date (navigate forward at most 12 months)
        for _ in range(12):
            if self.is_present(date_xpath, timeout=2):
                self.click(date_xpath)
                logger.info("Date picked: %s", aria_date)
                return
            try:
                self.click(self.loc.CALENDAR_NEXT_BTN)
                time.sleep(0.3)
            except Exception:
                break

        logger.error("Could not select date %s on calendar", aria_date)

    def _click_search(self) -> None:
        logger.info("Clicking Search button")
        for loc in [self.loc.SEARCH_BTN, self.loc.SEARCH_BTN_XPATH]:
            try:
                self.click(loc)
                return
            except Exception:
                continue
        logger.error("Search button not found for flights")
        raise RuntimeError("Flight search button not clickable")

    # ------------------------------------------------------------------ #
    # Validation
    # ------------------------------------------------------------------ #

    def are_results_displayed(self) -> bool:
        """
        Return True if at least one flight result card is visible
        on the results page.
        """
        logger.info("Verifying flight results are displayed…")
        # Wait for URL to change away from home page
        self.wait_for_url_contains("flights", timeout=30)
        try:
            results = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located(self.loc.FLIGHT_CARD)
            )
            logger.info("Found %d flight result(s).", len(results))
            return len(results) > 0
        except TimeoutException:
            logger.error("No flight results found on page.")
            return False

    def get_result_count(self) -> int:
        """Return the number of flight cards on the results page."""
        try:
            cards = self.driver.find_elements(*self.loc.FLIGHT_CARD)
            return len(cards)
        except Exception:
            return 0
