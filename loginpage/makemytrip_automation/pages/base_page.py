"""
pages/base_page.py
─────────────────────────────────────────────────────────────────────────────
BasePage — parent class inherited by ALL page objects.

Provides common low-level interactions so individual page classes stay clean
and DRY.  Every method logs the action being performed.

Usage (inside a page class):
    class LoginPage(BasePage):
        def click_login_button(self):
            self.click(self.BTN_LOGIN)
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from utils.logger import get_logger
from utils.helpers import wait_for_element, safe_click, scroll_to_element

log = get_logger(__name__)


class BasePage:
    """Abstract base page — all page objects should inherit from this class."""

    # ── Default explicit-wait timeout (override in subclass if needed) ────────
    DEFAULT_WAIT = 20

    def __init__(self, driver: WebDriver) -> None:
        """
        Initialise the page with a WebDriver instance.

        Args:
            driver: Active Selenium WebDriver session.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_WAIT)

    # ─────────────────────────────────────────────────────────────────────────
    # Navigation helpers
    # ─────────────────────────────────────────────────────────────────────────
    def open(self, url: str) -> None:
        """Navigate the browser to ``url``."""
        log.info(f"Navigating to: {url}")
        self.driver.get(url)

    def get_title(self) -> str:
        """Return the current page <title> text."""
        title = self.driver.title
        log.debug(f"Page title: {title}")
        return title

    def get_current_url(self) -> str:
        """Return the current browser URL."""
        url = self.driver.current_url
        log.debug(f"Current URL: {url}")
        return url

    # ─────────────────────────────────────────────────────────────────────────
    # Element interaction helpers
    # ─────────────────────────────────────────────────────────────────────────
    def find(self, by: By, locator: str, timeout: int = DEFAULT_WAIT) -> WebElement:
        """
        Locate and return a visible web element with an explicit wait.

        Args:
            by:      Selenium ``By`` strategy.
            locator: Selector string.
            timeout: Max seconds to wait (default 20).

        Returns:
            Located :class:`WebElement`.
        """
        return wait_for_element(self.driver, by, locator, timeout, "visible")

    def find_clickable(self, by: By, locator: str, timeout: int = DEFAULT_WAIT) -> WebElement:
        """Wait for and return a *clickable* web element."""
        return wait_for_element(self.driver, by, locator, timeout, "clickable")

    def click(self, by: By, locator: str, timeout: int = DEFAULT_WAIT) -> None:
        """
        Find an element by locator and click it (with JS fallback).

        Args:
            by:      Selenium ``By`` strategy.
            locator: Selector string.
            timeout: Max seconds to wait before clicking.
        """
        log.info(f"Clicking element: ({by}, '{locator}')")
        element = self.find_clickable(by, locator, timeout)
        safe_click(self.driver, element)

    def type_text(self, by: By, locator: str, text: str, clear_first: bool = True) -> None:
        """
        Type ``text`` into an input field.

        Args:
            by:          Selenium ``By`` strategy.
            locator:     Selector string.
            text:        Text to type.
            clear_first: If ``True`` (default) clear existing value first.
        """
        log.info(f"Typing '{text}' into ({by}, '{locator}')")
        element = self.find(by, locator)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, by: By, locator: str, timeout: int = DEFAULT_WAIT) -> str:
        """
        Return the visible text of an element.

        Args:
            by:      Selenium ``By`` strategy.
            locator: Selector string.
            timeout: Max seconds to wait.

        Returns:
            Stripped text content of the element.
        """
        element = self.find(by, locator, timeout)
        text = element.text.strip()
        log.debug(f"Element text '{text}' from ({by}, '{locator}')")
        return text

    def is_element_visible(self, by: By, locator: str, timeout: int = 5) -> bool:
        """
        Check whether an element is visible without raising an exception.

        Uses a short timeout (default 5s) to avoid slowing tests down.

        Returns:
            ``True`` if element became visible within ``timeout``, else ``False``.
        """
        try:
            wait_for_element(self.driver, by, locator, timeout, "visible")
            log.debug(f"Element VISIBLE: ({by}, '{locator}')")
            return True
        except (TimeoutException, NoSuchElementException):
            log.debug(f"Element NOT visible: ({by}, '{locator}')")
            return False

    def is_element_present(self, by: By, locator: str, timeout: int = 5) -> bool:
        """Check whether an element is present in the DOM (may be hidden)."""
        try:
            wait_for_element(self.driver, by, locator, timeout, "present")
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def scroll_to(self, by: By, locator: str) -> WebElement:
        """Scroll the viewport to bring an element into view and return it."""
        element = self.find(by, locator)
        scroll_to_element(self.driver, element)
        return element
