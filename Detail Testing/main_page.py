import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.url = "https://www.makemytrip.com/"

    def open_module(self, module):
        # Hitting module URL directly is often more reliable than menu clicking
        url_map = {
            "flight": "https://www.makemytrip.com/flights/",
            "hotel": "https://www.makemytrip.com/hotels/",
            "bus": "https://www.makemytrip.com/bus-tickets/"
        }
        print(f"Opening module: {module}")
        self.driver.get(url_map[module])
        time.sleep(10) # Heavy sleep for MMT
        self.close_popups()

    def close_popups(self):
        print("Handling popups...")
        time.sleep(2)
        selectors = [
            (By.CSS_SELECTOR, "span.commonModal__close"),
            (By.XPATH, "//button[text()='APPLY']"),
            (By.XPATH, "//button[contains(text(), 'OK')]"),
            (By.CSS_SELECTOR, ".closeBtn")
        ]
        for by, val in selectors:
            try:
                elem = self.driver.find_element(by, val)
                if elem.is_displayed():
                    elem.click()
                    print(f"Closed popup: {val}")
                    time.sleep(1)
            except:
                pass
        # click body
        try: self.driver.find_element(By.TAG_NAME, "body").click()
        except: pass

    def search_flight(self, origin, destination):
        print(f"Searching flights: {origin} -> {destination}")
        self.wait.until(EC.element_to_be_clickable((By.ID, "fromCity"))).click()
        inp = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='From']")))
        inp.send_keys(origin)
        time.sleep(2)
        # Select first suggestion
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.react-autosuggest__suggestion:first-child, .react-autosuggest__suggestions-list li"))).click()

        self.wait.until(EC.element_to_be_clickable((By.ID, "toCity"))).click()
        inp = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='To']")))
        inp.send_keys(destination)
        time.sleep(2)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.react-autosuggest__suggestion:first-child, .react-autosuggest__suggestions-list li"))).click()

        # Date
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class, 'DayPicker-Day') and not(contains(@class, 'disabled'))])[1]"))).click()

        btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".widgetSearchBtn")))
        self.driver.execute_script("arguments[0].click();", btn)

    def validate_flight_price(self):
        print("Checking results...")
        time.sleep(15) # Results load takes time
        # Handle secondary popups
        self.close_popups()
        try:
            price = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".listingCard, .priceSection, .blackText")))
            return price.is_displayed()
        except:
            return False

    def search_hotel(self, city):
        print(f"Searching hotels in: {city}")
        self.wait.until(EC.element_to_be_clickable((By.ID, "city"))).click()
        inp = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Where do you want to stay?']")))
        inp.send_keys(city)
        time.sleep(2)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.react-autosuggest__suggestion:first-child, .react-autosuggest__suggestions-list li"))).click()

        # Dates
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class, 'DayPicker-Day') and not(contains(@class, 'disabled'))])[1]"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class, 'DayPicker-Day') and not(contains(@class, 'disabled'))])[1]"))).click()

        # Apply for guests if modal is there
        try: self.driver.find_element(By.XPATH, "//button[text()='APPLY']").click()
        except: pass

        btn = self.wait.until(EC.element_to_be_clickable((By.ID, "hsw_search_button")))
        self.driver.execute_script("arguments[0].click();", btn)

    def get_hotel_details(self):
        print("Validating hotel results...")
        time.sleep(15)
        name = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#hlistpg_hotel_name, .hotelName")))
        price = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#hlistpg_hotel_notif_price, .priceText")))
        return name.text, price.text

    def search_bus(self, origin, destination):
        print(f"Searching buses: {origin} -> {destination}")
        self.wait.until(EC.element_to_be_clickable((By.ID, "fromCity"))).click()
        inp = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='From']")))
        inp.send_keys(origin)
        time.sleep(2)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.react-autosuggest__suggestion:first-child, .react-autosuggest__suggestions-list li"))).click()

        inp = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='To']")))
        inp.send_keys(destination)
        time.sleep(2)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.react-autosuggest__suggestion:first-child, .react-autosuggest__suggestions-list li"))).click()

        # Date
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class, 'DayPicker-Day') and not(contains(@class, 'disabled'))])[1]"))).click()

        btn = self.wait.until(EC.element_to_be_clickable((By.ID, "search_button")))
        self.driver.execute_script("arguments[0].click();", btn)

    def get_bus_details(self):
        print("Validating bus results...")
        time.sleep(15)
        operator = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".busName")))
        price = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".actualPrice")))
        return operator.text, price.text
