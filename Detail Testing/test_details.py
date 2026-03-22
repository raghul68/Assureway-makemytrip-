import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from details_page import MMTPage
import time

@pytest.fixture
def driver():
    """Fixture with maximum stealth flags for standard Selenium."""
    options = Options()
    # No headless! MMT detects it almost immediately.
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-notifications")
    
    # Standard anti-detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Modern User Agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    
    # Patch navigator.webdriver to undefined
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })
    
    yield driver
    driver.quit()

def test_mmt_automation_flow(driver):
    """Execution Flow: Open -> Login-Popup -> Search -> Validation."""
    page = MMTPage(driver)
    
    # 1. Open Site
    page.open_url("https://www.makemytrip.com/flights/")
    time.sleep(5)
    
    # 2. Close login popup
    page.close_popup_if_exists()
    
    # 3. Perform city search
    # Using codes BOM (Mumbai) and DEL (Delhi)
    page.perform_search("BOM", "DEL")
    
    # 4. Wait for results (Wait longer for bypass)
    print("Waiting for search results to bypass anti-bot check...")
    time.sleep(10)
    
    try:
        card = page.get_first_result()
        
        # 5. Validation
        v_name, v_price, name_t, price_t = page.validate_visibility(card)
        
        # Assertions
        assert v_name, "Airline name should be visible"
        assert v_price, "Flight price should be visible"
        
        print(f"\nSUCCESS: Observed flight '{name_t}' at price '{price_t}'")
        
    except Exception as e:
        driver.save_screenshot("final_failure_state.png")
        print(f"Error occurred: {e}")
        # Note: MMT often shows a blank page '200 OK' if it detects automation.
        pytest.fail("Failed to load results. MMT likely detected automation.")
