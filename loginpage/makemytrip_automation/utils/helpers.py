"""
utils/helpers.py
─────────────────────────────────────────────────────────────────────────────
Reusable helper utilities shared across all page objects and tests:
    - Screenshot capture
    - Explicit-wait wrapper
    - Safe JS-click (fallback for overlapping elements)
    - Scroll-to-element
"""

import os
import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)

from utils.logger import get_logger

log = get_logger(__name__)

# ── Default directory for screenshots ────────────────────────────────────────
SCREENSHOTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "screenshots"
)


def take_screenshot(driver: WebDriver, name: str = "screenshot") -> str:
    """
    Capture a PNG screenshot and save it to the screenshots directory.

    Args:
        driver: Active Selenium WebDriver instance.
        name:   Base name for the file (spaces replaced with underscores).

    Returns:
        Absolute path to the saved screenshot file.
    """
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = name.replace(" ", "_").replace("/", "_")
    filename = f"{safe_name}_{timestamp}.png"
    filepath = os.path.join(SCREENSHOTS_DIR, filename)

    try:
        driver.save_screenshot(filepath)
        log.info(f"Screenshot saved → {filepath}")
    except Exception as exc:
        log.error(f"Failed to capture screenshot: {exc}")

    return filepath


def wait_for_element(
    driver: WebDriver,
    by: By,
    locator: str,
    timeout: int = 20,
    condition: str = "visible",
) -> WebElement:
    """
    Explicit wait for a web element.

    Args:
        driver:    Active Selenium WebDriver instance.
        by:        Selenium ``By`` strategy (e.g. ``By.XPATH``).
        locator:   Selector string.
        timeout:   Maximum seconds to wait (default 20).
        condition: ``"visible"`` (default) | ``"clickable"`` | ``"present"``.

    Returns:
        The located :class:`WebElement`.

    Raises:
        TimeoutException: If the element is not found within ``timeout``.
    """
    wait = WebDriverWait(driver, timeout)
    conditions = {
        "visible":   EC.visibility_of_element_located((by, locator)),
        "clickable": EC.element_to_be_clickable((by, locator)),
        "present":   EC.presence_of_element_located((by, locator)),
    }
    ec = conditions.get(condition, conditions["visible"])
    log.debug(f"Waiting [{condition}] for ({by}, '{locator}') — timeout={timeout}s")
    return wait.until(ec)


def safe_click(driver: WebDriver, element: WebElement) -> None:
    """
    Click an element, falling back to JavaScript click on interception.

    Some MakeMyTrip overlays intercept normal clicks; this helper tries
    a normal click first, then retries with ``execute_script``.

    Args:
        driver:  Active Selenium WebDriver instance.
        element: The :class:`WebElement` to click.
    """
    try:
        element.click()
    except ElementClickInterceptedException:
        log.warning("Normal click intercepted — retrying with JS click")
        driver.execute_script("arguments[0].click();", element)


def scroll_to_element(driver: WebDriver, element: WebElement) -> None:
    """
    Scroll the page so that ``element`` is in view.

    Args:
        driver:  Active Selenium WebDriver instance.
        element: The :class:`WebElement` to scroll to.
    """
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    time.sleep(0.3)  # Brief pause so the scroll animation finishes


def wait_for_url_change(driver: WebDriver, original_url: str, timeout: int = 20) -> bool:
    """
    Wait until the browser URL changes from ``original_url``.

    Args:
        driver:       Active Selenium WebDriver instance.
        original_url: The URL before an action was triggered.
        timeout:      Maximum seconds to wait.

    Returns:
        ``True`` if the URL changed, ``False`` on timeout.
    """
    try:
        WebDriverWait(driver, timeout).until(EC.url_changes(original_url))
        log.debug(f"URL changed from {original_url} → {driver.current_url}")
        return True
    except TimeoutException:
        log.warning(f"URL did NOT change within {timeout}s (still: {driver.current_url})")
        return False
