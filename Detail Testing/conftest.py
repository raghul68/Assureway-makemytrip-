import pytest
from selenium import webdriver
from utils import take_screenshot

@pytest.fixture(scope="function")
def driver(request):
    """
    Setup and teardown of the Selenium WebDriver.
    This fixture runs for every test function.
    """
    # Setup Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.page_load_strategy = 'eager'
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
    options.add_argument("--disable-http2")
    # Disable images for faster page load
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    
    # Advanced evasion: Hide automation flags
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Initialize the Chrome driver
    driver = webdriver.Chrome(options=options)
    
    # Stealth: Set webdriver property to undefined
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    
    driver.set_page_load_timeout(120) 
    driver.implicitly_wait(10) 
    
    yield driver
    
    # Capture screenshot ONLY if failed (using the hook)
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        take_screenshot(driver, request.node.name)
        
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to expose test execution results to the request fixture.
    Used for checking if a test failed to trigger the screenshot capture.
    """
    outcome = yield
    rep = outcome.get_result()
    # Set a report attribute for each phase of a call ("setup", "call", "teardown")
    setattr(item, "rep_" + rep.when, rep)
