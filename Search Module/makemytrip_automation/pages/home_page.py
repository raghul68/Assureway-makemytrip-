"""
pages/home_page.py
HomePage — manages landing page navigation and login popup dismissal.
"""

import time

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.home_locators import HomeLocators
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class HomePage(BasePage):
    """Represents the MakeMyTrip homepage (https://www.makemytrip.com)."""

    def __init__(self, driver):
        super().__init__(driver)
        self.loc = HomeLocators

    # ------------------------------------------------------------------ #
    # Public interface
    # ------------------------------------------------------------------ #

    def load(self) -> "HomePage":
        """Open the homepage and dismiss any pop-ups."""
        self.open()
        self._dismiss_login_popup()
        return self

    def click_flights_tab(self) -> None:
        """Click the Flights navigation tab."""
        logger.info("Clicking Flights tab")
        self._safe_tab_click([self.loc.FLIGHTS_TAB, self.loc.FLIGHTS_TAB_ALT, self.loc.FLIGHTS_TEXT])

    def click_hotels_tab(self) -> None:
        """Click the Hotels navigation tab."""
        logger.info("Clicking Hotels tab")
        self._safe_tab_click([self.loc.HOTELS_TAB, self.loc.HOTELS_TAB_ALT, self.loc.HOTELS_TEXT])

    def click_bus_tab(self) -> None:
        """Click the Buses navigation tab."""
        logger.info("Clicking Bus tab")
        self._safe_tab_click([self.loc.BUS_TAB, self.loc.BUS_TAB_ALT, self.loc.BUS_TEXT])

    # ------------------------------------------------------------------ #
    # Private helpers
    # ------------------------------------------------------------------ #

    def _dismiss_login_popup(self) -> None:
        """
        Dismiss the login/sign-in modal if it appears on page load.
        """
        logger.info("Checking for login popup…")
        
        # Strategy 1: Click close button
        close_locators = [self.loc.LOGIN_CLOSE_BTN, self.loc.CLOSE_MODAL_BTN]
        for locator in close_locators:
            try:
                btn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(locator))
                btn.click()
                logger.info("Login popup dismissed via click on %s", locator)
                self.wait_for_overlay_disappear(self.loc.LOGIN_POPUP, timeout=5)
                return
            except TimeoutException:
                continue

        # Strategy 2: Press ESC
        logger.info("Click dismissal failed or not needed; trying ESC key fallback.")
        self.press_escape()
        time.sleep(1)

        # Strategy 3: Check visibility of backdrop
        if self.is_present(self.loc.LOGIN_POPUP, timeout=2):
            logger.warning("Login modal backdrop still visible; trying one last JS click.")
            try:
                self.js_click(self.loc.LOGIN_CLOSE_BTN)
                time.sleep(1)
            except:
                pass

    def _safe_tab_click(self, locators: list) -> None:
        """Try clicking tab locators in order; fall back to JS click."""
        for locator in locators:
            try:
                logger.debug("Trying tab click on %s", locator)
                self.click(locator)
                return
            except Exception:
                continue
        
        # Ultimate fallback: JS click
        logger.warning("Standard tab clicks failed; using JS click as last resort.")
        try:
            self.js_click(locators[0])
        except Exception as e:
            logger.error("All tab click strategies failed: %s", e)
            raise
