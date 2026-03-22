from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# USE A MORE DESKTOP-LIKE UA
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
options.add_argument("--disable-http2")

try:
    print("Starting driver with disable-http2...")
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    print("Navigating to makemytrip.com...")
    driver.get("https://www.makemytrip.com/")
    print(f"Title: {driver.title}")
    time.sleep(5)
    driver.save_screenshot("debug_mmt_3.png")
    print("Screenshot saved to debug_mmt_3.png")
    driver.quit()
    print("Success!")
except Exception as e:
    print(f"Error: {e}")
