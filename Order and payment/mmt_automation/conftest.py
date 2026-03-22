import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
import os
import datetime
import logging
import json

# Basic Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)1s - %(levelname)1s - %(message)1s')
logger = logging.getLogger(__name__)

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_path):
        with open(config_path) as f:
            return json.load(f)
    return {}

@pytest.fixture(scope="class")
def driver(request):
    config = load_config()
    chrome_options = Options()
    
    # Masking automation
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    if config.get("headless", False):
        chrome_options.add_argument("--headless=new")
    
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Standard flags
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-http2")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    
    # Use ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Apply Stealth
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    
    driver.implicitly_wait(10)
    request.cls.driver = driver
    
    logger.info("Starting browser...")
    yield driver
    
    logger.info("Closing browser...")
    driver.quit()

# Screenshot on Failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_dir = os.path.join(os.getcwd(), "screenshots")
            if not os.path.exists(screenshot_dir): os.makedirs(screenshot_dir)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            driver.save_screenshot(os.path.join(screenshot_dir, f"{item.name}_{timestamp}.png"))
            logger.error(f"Captured screenshot for failure.")
