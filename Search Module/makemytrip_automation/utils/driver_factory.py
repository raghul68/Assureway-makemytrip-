"""
utils/driver_factory.py
Creates and configures Selenium WebDriver instances.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from utils.config_reader import ConfigReader
from utils.logger import get_logger

logger = get_logger(__name__)
cfg = ConfigReader()


def get_driver() -> webdriver.Remote:
    """
    Instantiate a WebDriver based on config settings.

    Supported browsers: chrome | firefox | edge

    Returns:
        Configured WebDriver instance, ready to use.

    Raises:
        ValueError: If an unsupported browser name is specified.
    """
    browser = cfg.browser
    logger.info("Initialising WebDriver — browser: %s, headless: %s", browser, cfg.headless)

    driver = _create_driver(browser)

    # Apply common settings
    driver.set_page_load_timeout(cfg.page_load_timeout)
    driver.implicitly_wait(cfg.implicit_wait)
    driver.maximize_window()

    logger.info("WebDriver initialised successfully.")
    return driver


# ─────────────────────────────────────────────────────────────────────────────
# Private helpers
# ─────────────────────────────────────────────────────────────────────────────

def _chrome_options() -> ChromeOptions:
    opts = ChromeOptions()
    if cfg.headless:
        opts.add_argument("--headless=new")

    # Anti-bot / stability flags
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument("--disable-extensions")
    opts.add_argument("--disable-popup-blocking")
    opts.add_argument("--start-maximized")
    opts.add_argument("--lang=en-US")
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/122.0.0.0 Safari/537.36")

    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    })
    return opts


def _firefox_options() -> FirefoxOptions:
    opts = FirefoxOptions()
    if cfg.headless:
        opts.add_argument("--headless")
    opts.set_preference("dom.webdriver.enabled", False)
    return opts


def _edge_options() -> EdgeOptions:
    opts = EdgeOptions()
    if cfg.headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    return opts


def _create_driver(browser: str) -> webdriver.Remote:
    """
    Create browser-specific driver.  Chrome uses undetected_chromedriver
    to bypass anti-bot detection where possible.
    """
    if browser == "chrome":
        try:
            import undetected_chromedriver as uc
            logger.info("Using undetected-chromedriver for Chrome")
            
            # uc handles options slightly differently
            opts = uc.ChromeOptions()
            if cfg.headless:
                opts.add_argument("--headless")
            
            # Most anti-bot flags are already handled by UC by default
            opts.add_argument("--window-size=" + cfg.window_size)
            opts.add_argument("--disable-popup-blocking")
            
            driver = uc.Chrome(options=opts, driver_executable_path=ChromeDriverManager().install())
            return driver
        except (ImportError, Exception) as e:
            logger.warning("Failed to load undetected-chromedriver (%s); falling back to standard Chrome.", e)
            service = ChromeService(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=_chrome_options())

    elif browser == "firefox":
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=_firefox_options())

    elif browser == "edge":
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=_edge_options())

    else:
        raise ValueError(f"Unsupported browser '{browser}'. Choose: chrome | firefox | edge")
