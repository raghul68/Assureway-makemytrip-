"""
conftest.py
─────────────────────────────────────────────────────────────────────────────
Pytest configuration and shared fixtures for the MakeMyTrip automation suite.

What this file provides:
  1. `config`       fixture — loads config.yaml once per session
  2. `driver`       fixture — creates & quits the WebDriver (function scope)
  3. Screenshot-on-failure hook (`pytest_runtest_makereport`)
     Automatically captures a PNG screenshot whenever a test FAILS and
     embeds it in the pytest-html report.

Design decisions:
  • Function-scoped driver: each test gets a fresh browser session.
    This is slower but prevents state leaking between tests (critical for
    auth flows where cookies / modal state can bleed between tests).
  • undetected-chromedriver: drops ChromeDriver automation fingerprints
    that MakeMyTrip's bot-detection would otherwise flag.
"""

import os
import time
import pytest
import yaml

from utils.logger import get_logger
from utils.helpers import take_screenshot

log = get_logger("conftest")

# ── Path constants ────────────────────────────────────────────────────────────
ROOT_DIR        = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT    = os.path.dirname(ROOT_DIR) if ROOT_DIR.endswith("tests") else ROOT_DIR
CONFIG_PATH     = os.path.join(PROJECT_ROOT, "config.yaml")
SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, "screenshots")
REPORTS_DIR     = os.path.join(PROJECT_ROOT, "reports")

# ── Ensure output directories exist ──────────────────────────────────────────
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR,     exist_ok=True)


# ─────────────────────────────────────────────────────────────────────────────
# Fixture: config  (session scope — load YAML once for all tests)
# ─────────────────────────────────────────────────────────────────────────────
@pytest.fixture(scope="session")
def config() -> dict:
    """
    Load and return the project configuration from config.yaml.

    Returns:
        Dictionary with all configuration values (base_url, timeouts, etc.)
    """
    log.info(f"Loading configuration from: {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    log.info(f"Config loaded — base_url: {cfg.get('base_url')}")
    return cfg


# ─────────────────────────────────────────────────────────────────────────────
# Fixture: driver  (function scope — fresh browser per test)
# ─────────────────────────────────────────────────────────────────────────────
@pytest.fixture(scope="function")
def driver(config):
    """
    Create and yield a configured Chrome WebDriver instance.

    Uses `undetected_chromedriver` to prevent bot-detection by MakeMyTrip.
    The driver is automatically quit after every test (pass or fail).

    Yields:
        Active :class:`undetected_chromedriver.Chrome` driver instance.
    """
    import undetected_chromedriver as uc

    log.info("=" * 60)
    log.info("Setting up WebDriver for test")

    # ── Chrome options ─────────────────────────────────────────────────────
    options = uc.ChromeOptions()

    if config.get("headless", False):
        # Note: undetected-chromedriver headless mode is limited.
        # For CI/CD, prefer visible mode with a display server (Xvfb on Linux).
        options.add_argument("--headless=new")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # ── Instantiate undetected Chrome ─────────────────────────────────────
    log.info("Launching undetected Chrome browser")
    web_driver = uc.Chrome(options=options, use_subprocess=True)

    # ── Apply timeouts from config ────────────────────────────────────────
    web_driver.implicitly_wait(config.get("implicit_wait", 5))
    web_driver.set_page_load_timeout(config.get("page_load_timeout", 30))

    # Maximise window for consistent element visibility
    web_driver.maximize_window()
    log.info("WebDriver ready — browser launched")

    yield web_driver  # ← Test runs here

    # ── Teardown: always quit the browser ─────────────────────────────────
    log.info("Tearing down WebDriver — closing browser")
    try:
        web_driver.quit()
    except Exception as exc:
        log.warning(f"Error during driver.quit(): {exc}")
    log.info("=" * 60)


# ─────────────────────────────────────────────────────────────────────────────
# Hook: Screenshot on failure
# ─────────────────────────────────────────────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook that runs after each test phase (setup / call / teardown).

    When a test in the ``call`` phase FAILS:
      1. Captures a screenshot using the 'driver' fixture.
      2. Saves it to the ``screenshots/`` directory.
      3. Attaches it to the pytest-html report (if plugin is active).
    """
    outcome = yield  # Execute the test
    report  = outcome.get_result()

    # Only act on failures in the test body (not setup/teardown)
    if report.when == "call" and report.failed:
        log.error(f"Test FAILED: {item.nodeid}")

        # Retrieve the driver fixture from the test's function scope
        driver_fixture = item.funcargs.get("driver")
        if driver_fixture is None:
            log.warning("No 'driver' fixture found — cannot capture screenshot")
            return

        # Build a safe filename from the test node ID
        # e.g. "tests/test_login.py::TestLogin::test_valid_login" →
        #      "tests_test_login_py__TestLogin__test_valid_login"
        safe_name = (
            item.nodeid
            .replace("::", "__")
            .replace("/", "_")
            .replace("\\", "_")
            .replace(".py", "")
        )

        screenshot_path = take_screenshot(driver_fixture, f"FAIL__{safe_name}")
        log.error(f"Failure screenshot saved → {screenshot_path}")

        # ── Attach to pytest-html report ──────────────────────────────────
        # The pytest-html plugin looks for extras on the item via _pytest_html_*
        try:
            import pytest_html
            from pytest_html import extras as html_extras

            extra_list = getattr(report, "extras", [])
            extra_list.append(html_extras.image(screenshot_path))
            report.extras = extra_list
            log.debug("Screenshot attached to HTML report")
        except ImportError:
            log.debug("pytest-html not installed — skipping report attachment")
        except Exception as exc:
            log.warning(f"Could not attach screenshot to report: {exc}")
