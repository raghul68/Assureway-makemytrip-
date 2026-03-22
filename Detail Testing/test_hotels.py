import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from hotel_page import HotelPage
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

def test_mmt_hotel_search(driver):
    page = HotelPage(driver)
    
    # 1. Open Site
    page.open_url("https://www.makemytrip.com/hotels/")
    
    # 2. Close Popup
    page.close_popup_if_exists()
    
    # 3. Enter details
    page.enter_hotel_details("Manali")
    
    # 4. Search
    page.click_search()
    
    # 5. Validation
    # Wait for results page check bypass
    time.sleep(5)
    try:
        hotel_name, price = page.get_first_hotel_info()
        assert hotel_name, "Hotel name should not be empty"
        assert price, "Price should not be empty"
        print(f"\nHotel Found: {hotel_name} at {price}")
    except Exception as e:
        driver.save_screenshot("hotel_search_failed.png")
        pytest.fail(f"Hotel search failed: {e}")
