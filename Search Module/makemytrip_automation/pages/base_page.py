"""
pages/base_page.py
BasePage — shared utilities inherited by every page class.
"""

import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config_reader import ConfigReader
from utils.logger import get_logger

cfg = ConfigReader()


class BasePage:
    """
    Abstract base class that wraps common Selenium operations with logging
    and explicit waits.  All page classes inherit from this.
    """

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, cfg.timeout)
        self.logger = get_logger(self.__class__.__name__)

    # ------------------------------------------------------------------ #
    # Navigation
    # ------------------------------------------------------------------ #

    def open(self, url: str = None) -> None:
        """Navigate to a URL (defaults to base_url from config)."""
        target = url or cfg.base_url
        self.logger.info("Navigating to: %s", target)
        self.driver.get(target)

    def get_title(self) -> str:
        return self.driver.title

    def get_current_url(self) -> str:
        return self.driver.current_url

    # ------------------------------------------------------------------ #
    # Element interactions
    # ------------------------------------------------------------------ #

    def find(self, locator: tuple, timeout: int = None) -> WebElement:
        """Wait for element to be present and return it."""
        t = timeout or cfg.timeout
        return WebDriverWait(self.driver, t).until(
            EC.presence_of_element_located(locator),
            message=f"Element not found: {locator}",
        )

    def find_visible(self, locator: tuple, timeout: int = None) -> WebElement:
        """Wait for element to be visible."""
        t = timeout or cfg.timeout
        return WebDriverWait(self.driver, t).until(
            EC.visibility_of_element_located(locator),
            message=f"Element not visible: {locator}",
        )

    def find_clickable(self, locator: tuple, timeout: int = None) -> WebElement:
        """Wait for element to be clickable."""
        t = timeout or cfg.timeout
        return WebDriverWait(self.driver, t).until(
            EC.element_to_be_clickable(locator),
            message=f"Element not clickable: {locator}",
        )

    def find_all(self, locator: tuple, timeout: int = None) -> list:
        """Return all matching elements after waiting for at least one."""
        t = timeout or cfg.timeout
        WebDriverWait(self.driver, t).until(
            EC.presence_of_all_elements_located(locator),
            message=f"Elements not found: {locator}",
        )
        return self.driver.find_elements(*locator)

    def is_present(self, locator: tuple, timeout: int = 5) -> bool:
        """Return True if element exists within timeout, False otherwise."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def click(self, locator: tuple) -> None:
        """Click a clickable element — falls back to JS click on intercept."""
        self.logger.debug("Clicking element: %s", locator)
        try:
            el = self.find_clickable(locator)
            el.click()
        except ElementClickInterceptedException:
            self.logger.warning("Standard click intercepted, using JS click on %s", locator)
            el = self.find(locator)
            self.driver.execute_script("arguments[0].click();", el)

    def js_click(self, locator: tuple) -> None:
        """Force a JavaScript click (bypasses overlays)."""
        el = self.find(locator)
        self.driver.execute_script("arguments[0].click();", el)

    def type_text(self, locator: tuple, text: str, clear: bool = True) -> None:
        """Click, optionally clear, then type text into a field."""
        self.logger.debug("Typing '%s' into %s", text, locator)
        el = self.find_visible(locator)
        if clear:
            el.clear()
        el.send_keys(text)

    def type_and_wait(self, locator: tuple, text: str, pause: float = 0.5) -> None:
        """Type text then wait briefly for suggestions to appear."""
        self.type_text(locator, text)
        time.sleep(pause)  # brief pause ONLY for suggestion popups

    def press_escape(self) -> None:
        """Send ESC key to the body to dismiss modals."""
        self.logger.debug("Pressing ESC key")
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

    def wait_for_overlay_disappear(self, locator: tuple, timeout: int = 10) -> None:
        """Wait for an overlay or backdrop to disappear."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            self.logger.debug("Overlay %s disappeared", locator)
        except TimeoutException:
            self.logger.warning("Overlay %s did not disappear within %ds", locator, timeout)

    def scroll_to(self, locator: tuple) -> None:
        el = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)

    def hover(self, locator: tuple) -> None:
        el = self.find(locator)
        ActionChains(self.driver).move_to_element(el).perform()

    def get_text(self, locator: tuple) -> str:
        return self.find_visible(locator).text.strip()

    def get_attribute(self, locator: tuple, attr: str) -> str:
        return self.find(locator).get_attribute(attr)

    # ------------------------------------------------------------------ #
    # Date helpers
    # ------------------------------------------------------------------ #

    @staticmethod
    def get_future_date(days_offset: int) -> datetime:
        """Return a datetime object N days from today."""
        return datetime.now() + timedelta(days=days_offset)

    @staticmethod
    def format_date(dt: datetime, fmt: str = "%d %b %Y") -> str:
        """Format datetime as e.g. '07 Apr 2025'."""
        return dt.strftime(fmt)

    # ------------------------------------------------------------------ #
    # Wait helpers
    # ------------------------------------------------------------------ #

    def wait_for_url_change(self, current_url: str, timeout: int = 30) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_changes(current_url))
            return True
        except TimeoutException:
            return False

    def wait_for_url_contains(self, fragment: str, timeout: int = 30) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_contains(fragment))
            return True
        except TimeoutException:
            return False

    def wait_for_element_disappear(self, locator: tuple, timeout: int = 10) -> None:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
        except TimeoutException:
            pass

    # ------------------------------------------------------------------ #
    # Screenshot
    # ------------------------------------------------------------------ #

    def take_screenshot(self, name: str = "screenshot") -> str:
        """
        Save a screenshot to the screenshots/ folder.

        Returns the absolute path of the saved image.
        """
        folder = Path(cfg.screenshots_path)
        folder.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = folder / f"{name}_{timestamp}.png"
        self.driver.save_screenshot(str(filename))
        self.logger.info("Screenshot saved: %s", filename)
        return str(filename)
