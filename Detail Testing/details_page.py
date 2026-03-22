from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class MMTPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        
    # Locators
    CLOSE_POP_BUTTON = (By.CSS_SELECTOR, "span.commonModal__close")
    FROM_CITY_TRIGGER = (By.ID, "fromCity")
    FROM_CITY_INPUT = (By.XPATH, "//input[@placeholder='From']")
    TO_CITY_TRIGGER = (By.ID, "toCity")
    TO_INPUT = (By.XPATH, "//input[@placeholder='To']")
    # Updated suggestion locator based on browser exploration
    FIRST_SUGGESTION = (By.CSS_SELECTOR, ".react-autosuggest__suggestion:first-child, li[id*='react-autowhatever-1-section-0-item-0']")
    # Calendar date (selects the first available or a specific date)
    DATE_SELECT = (By.XPATH, "(//div[contains(@class, 'DayPicker-Day') and not(contains(@class, 'disabled'))])[1]")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".widgetSearchBtn")
    # Results Page
    FIRST_FLIGHT_CARD = (By.CSS_SELECTOR, ".listingCard, div[id*='listing-id']")
    AIRLINE_NAME = (By.CSS_SELECTOR, ".airlineName, p.airlineName")
    FLIGHT_PRICE = (By.CSS_SELECTOR, ".priceSection .blackText, div.priceSection")

    def open_url(self, url):
        self.driver.get(url)

    def close_popup_if_exists(self):
        try:
            # Wait for popup and close
            time.sleep(3)
            close = self.wait.until(EC.element_to_be_clickable(self.CLOSE_POP_BUTTON))
            close.click()
            print("Login popup closed.")
        except:
            print("No login popup found.")
            # click body to clear any overlay
            try: self.driver.find_element(By.TAG_NAME, "body").click()
            except: pass

    def perform_search(self, from_city, to_city):
        # 1. From City
        self.wait.until(EC.element_to_be_clickable(self.FROM_CITY_TRIGGER)).click()
        f_in = self.wait.until(EC.visibility_of_element_located(self.FROM_CITY_INPUT))
        f_in.send_keys(from_city)
        time.sleep(2)
        self.wait.until(EC.element_to_be_clickable(self.FIRST_SUGGESTION)).click()

        # 2. To City
        self.wait.until(EC.element_to_be_clickable(self.TO_CITY_TRIGGER)).click()
        t_in = self.wait.until(EC.visibility_of_element_located(self.TO_INPUT))
        t_in.send_keys(to_city)
        time.sleep(2)
        self.wait.until(EC.element_to_be_clickable(self.FIRST_SUGGESTION)).click()

        # 3. Select Date (MMT usually opens calendar after To City selection)
        try:
            self.wait.until(EC.element_to_be_clickable(self.DATE_SELECT)).click()
        except:
            print("Calendar did not appear or date already selected.")

        # 4. Click Search
        search_btn = self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON))
        # Use JS click if standard click fails
        try:
            search_btn.click()
        except:
            self.driver.execute_script("arguments[0].click();", search_btn)

    def get_first_result(self):
        # Long wait for results as they load dynamically and anti-bot checks happen
        time.sleep(5)
        card = self.wait.until(EC.visibility_of_element_located(self.FIRST_FLIGHT_CARD))
        self.driver.execute_script("arguments[0].scrollIntoView();", card)
        return card

    def validate_visibility(self, card):
        name = card.find_element(*self.AIRLINE_NAME)
        price = card.find_element(*self.FLIGHT_PRICE)
        return name.is_displayed(), price.is_displayed(), name.text, price.text
