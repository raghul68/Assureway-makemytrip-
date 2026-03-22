import pytest
import undetected_chromedriver as uc
from utils.config_manager import ConfigManager
import os
import time

@pytest.fixture(scope="function")
def driver(request):
    config = ConfigManager.get_config()
    browser_name = config.get("browser", "chrome").lower()
    
    if browser_name == "chrome":
        options = uc.ChromeOptions()
        # options.add_argument("--disable-blink-features=AutomationControlled") # UC already handles this
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Adding more arguments for stability and invisibility
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        
        driver = uc.Chrome(options=options, headless=False)
    else:
        raise ValueError(f"Browser {browser_name} not supported")
        
    driver.maximize_window()
    driver.implicitly_wait(config.get("implicit_wait", 10))
    driver.get(config.get("base_url"))
    
    yield driver
    
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        if "driver" in item.fixturenames:
            driver = item.funcargs["driver"]
            if not os.path.exists("screenshots"):
                os.makedirs("screenshots")
            
            try:
                screenshot_path = os.path.join("screenshots", f"{item.name}.png")
                driver.save_screenshot(screenshot_path)
                
                dom_path = os.path.join("screenshots", f"{item.name}_dom.html")
                with open(dom_path, "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
            except Exception as e:
                print(f"Failed to save screenshot: {e}")
