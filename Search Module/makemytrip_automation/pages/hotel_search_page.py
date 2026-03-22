"""
pages/hotel_search_page.py
HotelSearchPage — automates the Hotels search workflow on MakeMyTrip.
"""

import time
from datetime import datetime

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.hotel_locators import HotelLocators
from pages.base_page import BasePage
from utils.config_reader import ConfigReader
from utils.logger import get_logger

cfg = ConfigReader()
logger = get_logger(__name__)


class HotelSearchPage(BasePage):
    """
    Encapsulates all interactions on the MakeMyTrip hotel search section.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.loc = HotelLocators

    # ------------------------------------------------------------------ #
    # High-level action
    # ------------------------------------------------------------------ #

    def search_hotel(
        self,
        city: str,
        checkin_date: datetime,
        checkout_date: datetime,
        rooms: int = 1,
        adults: int = 2,
    ) -> None:
        """
        Perform a complete hotel search.

        Args:
            city:          Destination city
            checkin_date:  Check-in date
            checkout_date: Check-out date
            rooms:         Number of rooms
            adults:        Number of adults
        """
        logger.info("=== Starting Hotel Search ===")
        logger.info("City: %s | Check-in: %s | Check-out: %s | Rooms: %d | Adults: %d",
                    city, self.format_date(checkin_date), self.format_date(checkout_date),
                    rooms, adults)

        self._enter_city(city)
        self._select_checkin_date(checkin_date)
        self._select_checkout_date(checkout_date)
        self._click_search()
        logger.info("Hotel search submitted.")

    # ------------------------------------------------------------------ #
    # Step methods
    # ------------------------------------------------------------------ #

    def _enter_city(self, city: str) -> None:
        logger.info("Entering hotel city: %s", city)
        for loc in [self.loc.CITY_FIELD, self.loc.CITY_FIELD_XPATH]:
            try:
                field = self.find_clickable(loc, timeout=10)
                field.click()
                field.clear()
                field.send_keys(city)
                time.sleep(1.2)
                break
            except Exception:
                continue

        # Strategy 1: Click first suggestion
        try:
            first = self.find_visible(self.loc.CITY_FIRST_ITEM, timeout=8)
            self.click(self.loc.CITY_FIRST_ITEM)
            logger.info("City suggestion clicked for: %s", city)
            return
        except Exception:
            logger.warning("Suggestion click failed; trying keyboard fallback.")

        # Strategy 2: Keyboard fallback
        try:
            from selenium.webdriver.common.keys import Keys
            active = self.driver.switch_to.active_element
            active.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.3)
            active.send_keys(Keys.ENTER)
            logger.info("City selected via keyboard for: %s", city)
        except Exception as e:
            logger.error("Failed to select hotel city suggestion: %s", e)

    def _select_checkin_date(self, date: datetime) -> None:
        logger.info("Selecting check-in date: %s", self.format_date(date))
        for loc in [self.loc.CHECKIN_FIELD, self.loc.CHECKIN_FIELD_CSS]:
            try:
                self.click(loc)
                break
            except Exception:
                continue
        self._pick_calendar_date(date)

    def _select_checkout_date(self, date: datetime) -> None:
        logger.info("Selecting check-out date: %s", self.format_date(date))
        # Calendar may remain open after check-in selection
        if not self.is_present(self.loc.CALENDAR_NEXT_BTN, timeout=3):
            for loc in [self.loc.CHECKOUT_FIELD, self.loc.CHECKOUT_FIELD_CSS]:
                try:
                    self.click(loc)
                    break
                except Exception:
                    continue
        self._pick_calendar_date(date)

    def _pick_calendar_date(self, date: datetime) -> None:
        """Navigate calendar and select the given date."""
        aria_date = date.strftime("%a %b %d %Y").replace(" 0", " ")
        date_xpath = (By.XPATH,
                      f"//div[@aria-label='{aria_date}' and not(contains(@class,'disabled'))] | "
                      f"//p[@aria-label='{aria_date}']")

        for _ in range(12):
            if self.is_present(date_xpath, timeout=2):
                self.click(date_xpath)
                logger.info("Picked date: %s", aria_date)
                return
            try:
                self.click(self.loc.CALENDAR_NEXT_BTN)
                time.sleep(0.3)
            except Exception:
                break

        logger.error("Could not select date %s", aria_date)

    def _click_search(self) -> None:
        logger.info("Clicking Hotel Search button")
        for loc in [self.loc.SEARCH_BTN, self.loc.SEARCH_BTN_XPATH]:
            try:
                self.click(loc)
                return
            except Exception:
                continue
        raise RuntimeError("Hotel search button not clickable")

    # ------------------------------------------------------------------ #
    # Validation
    # ------------------------------------------------------------------ #

    def are_results_displayed(self) -> bool:
        """Return True if hotel result cards are visible."""
        logger.info("Verifying hotel results are displayed…")
        self.wait_for_url_contains("hotels", timeout=30)
        try:
            results = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located(self.loc.HOTEL_CARD)
            )
            logger.info("Found %d hotel result(s).", len(results))
            return len(results) > 0
        except TimeoutException:
            logger.error("No hotel results found.")
            return False

    def get_result_count(self) -> int:
        try:
            return len(self.driver.find_elements(*self.loc.HOTEL_CARD))
        except Exception:
            return 0
