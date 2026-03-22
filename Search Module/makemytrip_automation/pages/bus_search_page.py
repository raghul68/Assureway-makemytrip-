"""
pages/bus_search_page.py
BusSearchPage — automates the Bus search workflow on MakeMyTrip.
"""

import time
from datetime import datetime

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.bus_locators import BusLocators
from pages.base_page import BasePage
from utils.config_reader import ConfigReader
from utils.logger import get_logger

cfg = ConfigReader()
logger = get_logger(__name__)


class BusSearchPage(BasePage):
    """
    Encapsulates all interactions on the MakeMyTrip bus search section.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.loc = BusLocators

    # ------------------------------------------------------------------ #
    # High-level action
    # ------------------------------------------------------------------ #

    def search_bus(self, from_city: str, to_city: str, travel_date: datetime) -> None:
        """
        Perform a complete bus search.

        Args:
            from_city:    Departure city
            to_city:      Destination city
            travel_date:  Travel date
        """
        logger.info("=== Starting Bus Search ===")
        logger.info("Route: %s → %s | Date: %s", from_city, to_city,
                    self.format_date(travel_date))

        self._enter_from_city(from_city)
        self._enter_to_city(to_city)
        self._select_travel_date(travel_date)
        self._click_search()
        logger.info("Bus search submitted.")

    # ------------------------------------------------------------------ #
    # Step methods
    # ------------------------------------------------------------------ #

    def _enter_from_city(self, city: str) -> None:
        logger.info("Entering bus FROM city: %s", city)
        for loc in [self.loc.FROM_FIELD, self.loc.FROM_FIELD_CSS]:
            try:
                field = self.find_clickable(loc, timeout=10)
                field.clear()
                field.send_keys(city)
                time.sleep(0.8)
                break
            except Exception:
                continue
        self._select_first_suggestion()

    def _enter_to_city(self, city: str) -> None:
        logger.info("Entering bus TO city: %s", city)
        for loc in [self.loc.TO_FIELD, self.loc.TO_FIELD_CSS]:
            try:
                field = self.find_clickable(loc, timeout=10)
                field.clear()
                field.send_keys(city)
                time.sleep(0.8)
                break
            except Exception:
                continue
        self._select_first_suggestion()

    def _select_first_suggestion(self) -> None:
        """Wait for auto-complete suggestions and pick the first one."""
        logger.info("Selecting bus suggestion...")
        time.sleep(1.2)  # Wait for API

        # Strategy 1: Click
        try:
            first = self.find_visible(self.loc.FIRST_OPTION, timeout=8)
            self.click(self.loc.FIRST_OPTION)
            logger.info("Bus suggestion clicked successfully.")
            return
        except Exception:
            logger.warning("Bus suggestion click failed; trying keyboard fallback.")

        # Strategy 2: Keyboard
        try:
            from selenium.webdriver.common.keys import Keys
            active = self.driver.switch_to.active_element
            active.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.3)
            active.send_keys(Keys.ENTER)
            logger.info("Bus suggestion selected via keyboard.")
        except Exception as e:
            logger.error("Failed to select bus suggestion: %s", e)

    def _select_travel_date(self, date: datetime) -> None:
        logger.info("Selecting travel date: %s", self.format_date(date))
        for loc in [self.loc.DATE_FIELD, self.loc.DATE_FIELD_XPATH]:
            try:
                self.click(loc)
                break
            except Exception:
                continue
        self._pick_calendar_date(date)

    def _pick_calendar_date(self, date: datetime) -> None:
        """Navigate calendar and click the desired date cell."""
        aria_date = date.strftime("%a %b %d %Y").replace(" 0", " ")
        date_xpath = (By.XPATH,
                      f"//div[@aria-label='{aria_date}' and not(contains(@class,'disabled'))] | "
                      f"//p[@aria-label='{aria_date}']")

        for _ in range(12):
            if self.is_present(date_xpath, timeout=2):
                self.click(date_xpath)
                logger.info("Picked travel date: %s", aria_date)
                return
            try:
                self.click(self.loc.CALENDAR_NEXT)
                time.sleep(0.3)
            except Exception:
                break

        logger.error("Could not pick date %s on bus calendar", aria_date)

    def _click_search(self) -> None:
        logger.info("Clicking Bus Search button")
        for loc in [self.loc.SEARCH_BTN, self.loc.SEARCH_BTN_XPATH]:
            try:
                self.click(loc)
                return
            except Exception:
                continue
        raise RuntimeError("Bus search button not clickable")

    # ------------------------------------------------------------------ #
    # Validation
    # ------------------------------------------------------------------ #

    def are_results_displayed(self) -> bool:
        """Return True if bus result cards are visible."""
        logger.info("Verifying bus results are displayed…")
        self.wait_for_url_contains("bus", timeout=30)
        try:
            results = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located(self.loc.BUS_CARD)
            )
            logger.info("Found %d bus result(s).", len(results))
            return len(results) > 0
        except TimeoutException:
            logger.error("No bus results found.")
            return False

    def get_result_count(self) -> int:
        try:
            return len(self.driver.find_elements(*self.loc.BUS_CARD))
        except Exception:
            return 0
