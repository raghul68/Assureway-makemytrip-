"""
conftest.py
===========
Pytest session-level fixtures and hooks for the MakeMyTrip automation suite.

Responsibilities:
  - Provide a `driver` fixture that:
      - Reads browser settings from config
      - Launches the WebDriver
      - Navigates to the base URL
      - Tears down driver after each test
  - Implement a hook that automatically captures a screenshot on test failure.
  - Add suite-level metadata to the HTML report.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

import pytest

# ── Make sure the project root is on sys.path ──────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.config_reader import ConfigReader
from utils.driver_factory import get_driver
from utils.logger import get_logger

cfg = ConfigReader()
logger = get_logger("conftest")


# ============================================================================
# pytest_configure — add custom metadata to HTML report header
# ============================================================================

def pytest_configure(config):
    """Attach environment metadata to the HTML report."""
    config._metadata = getattr(config, "_metadata", {})
    config._metadata.update(
        {
            "Application": "MakeMyTrip (https://www.makemytrip.com)",
            "Browser": cfg.browser.capitalize(),
            "Base URL": cfg.base_url,
            "Environment": "Production",
            "Test Run": datetime.now().strftime("%d %b %Y %H:%M:%S"),
        }
    )


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture(scope="function")
def driver():
    """
    Function-scoped WebDriver fixture.

    - Initialises the browser before each test.
    - Opens the MakeMyTrip homepage.
    - Tears down (quits) the browser after each test regardless of outcome.
    """
    logger.info("──────────────────────────────────────────────")
    logger.info("Setting up WebDriver for test")
    web_driver = get_driver()

    logger.info("Navigating to base URL: %s", cfg.base_url)
    web_driver.get(cfg.base_url)

    yield web_driver  # hand control to the test

    logger.info("Tearing down WebDriver")
    web_driver.quit()
    logger.info("──────────────────────────────────────────────")


# ============================================================================
# Screenshot on failure hook
# ============================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture a screenshot whenever a test fails.

    The screenshot is:
      - Saved to the configured screenshots/ folder.
      - Attached to the HTML report.
      - Filename format: <test_name>_<timestamp>.png
    """
    outcome = yield  # run the test
    report = outcome.get_result()

    # Only act on 'call' phase failures (not setup/teardown)
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver is None:
            return

        # Build screenshot path
        folder = Path(cfg.screenshots_path)
        folder.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = item.name.replace("/", "_").replace(":", "_")
        screenshot_path = folder / f"{safe_name}_{timestamp}.png"

        try:
            driver.save_screenshot(str(screenshot_path))
            logger.error(
                "TEST FAILED — screenshot saved: %s", screenshot_path
            )

            # Attach screenshot to pytest-html report
            if hasattr(report, "extra"):
                import pytest_html  # noqa: F401
                from pytest_html import extras
                report.extra = getattr(report, "extra", [])
                report.extra.append(
                    extras.image(str(screenshot_path))
                )
        except Exception as exc:
            logger.warning("Failed to save screenshot: %s", exc)
