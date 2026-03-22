from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

try:
    print("Starting driver...")
    driver = webdriver.Chrome(options=options)
    print("Navigating to example.com...")
    driver.get("https://www.example.com")
    print(f"Title: {driver.title}")
    driver.quit()
    print("Success!")
except Exception as e:
    print(f"Error: {e}")
