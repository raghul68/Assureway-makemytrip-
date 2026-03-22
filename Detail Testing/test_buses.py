import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bus_page import BusPage
import time

@pytest.fixture
def driver():
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Stealth
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })
    yield driver
    driver.quit()

def test_mmt_bus_search(driver):
    page = BusPage(driver)
    
    # 1. Open Site
    page.open_url("https://www.makemytrip.com/bus-tickets/")
    
    # 2. Close Popup
    page.close_popup_if_exists()
    
    # 3. Enter details
    page.enter_bus_details("Mumbai", "Pune")
    
    # 4. Search
    page.click_search()
    
    # 5. Validation
    # Wait for results page check bypass
    time.sleep(5)
    try:
        op_name, price = page.get_first_bus_info()
        assert op_name, "Bus operator name should not be empty"
        assert price, "Price should not be empty"
        print(f"\nBus Found: {op_name} at {price}")
    except Exception as e:
        driver.save_screenshot("bus_search_failed.png")
        pytest.fail(f"Bus search failed: {e}")
