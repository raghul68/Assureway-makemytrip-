import pytest
import os
import logging
import undetected_chromedriver as uc

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@pytest.fixture(scope="function")
def driver():
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-popup-blocking")
    
    _driver = uc.Chrome(options=options)
    _driver.implicitly_wait(10)
    
    yield _driver
    
    try:
        _driver.quit()
    except Exception as e:
        pass

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        if "driver" in item.fixturenames:
            driver_fixture = item.funcargs["driver"]
            if not os.path.exists("screenshots"):
                os.makedirs("screenshots")
            screenshot_path = os.path.join("screenshots", f"{item.name}.png")
            try:
                driver_fixture.save_screenshot(screenshot_path)
                logging.error(f"Test failed! Screenshot saved to {screenshot_path}")
            except Exception as e:
                logging.error(f"Failed to save screenshot: {e}")
