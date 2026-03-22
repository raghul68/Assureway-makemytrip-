from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import time

class HomePage(BasePage):
    """
    Page Object containing locators and actions for MakeMyTrip Home Page.
    """
    
    URL = "https://www.makemytrip.com/"
    
    # --- Locators ---
    CLOSE_POPUP_BTN = (By.CSS_SELECTOR, ".commonModal__close")
    
    # Search Input Fields
    FROM_CITY_LABEL = (By.CSS_SELECTOR, "label[for='fromCity']")
    FROM_CITY_INPUT = (By.CSS_SELECTOR, "input[placeholder='From']")
    FROM_CITY_SUGGESTION = (By.XPATH, "(//li[contains(@role,'option')])[1]")
    
    TO_CITY_LABEL = (By.CSS_SELECTOR, "label[for='toCity']")
    TO_CITY_INPUT = (By.CSS_SELECTOR, "input[placeholder='To']")
    TO_CITY_SUGGESTION = (By.XPATH, "(//li[contains(@role,'option')])[1]")
    
    # Date Selection
    DEPARTURE_DATE_LABEL = (By.CSS_SELECTOR, "label[for='departure']")
    NEXT_MONTH_BTN = (By.CSS_SELECTOR, ".DayPicker-NavButton--next")
    AVAILABLE_DATES = (By.CSS_SELECTOR, ".DayPicker-Day[aria-disabled='false']")
    
    SEARCH_BTN = (By.CSS_SELECTOR, ".primaryBtn")
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def load(self):
        """Loads the home page and attempts to close the initial popup if present."""
        self.open_url(self.URL)
        time.sleep(3) 
        self.force_close_modals()
        # Click outside to ensure any remaining overlays are cleared
        try:
            self.driver.find_element(By.TAG_NAME, "body").click()
        except:
            pass
            
    def enter_cities(self, from_city, to_city):
        """Clicks on city inputs, types the city names, and selects the first suggestion."""
        # --- Handle FROM City ---
        self.click_element(self.FROM_CITY_LABEL)
        self.enter_text(self.FROM_CITY_INPUT, from_city)
        time.sleep(2) # Wait for suggestions to appear
        # Select first suggestion
        self.click_element(self.FROM_CITY_SUGGESTION)
        
        # --- Handle TO City ---
        # Note: Clicking FROM city often auto-moves focus or opens the TO city selection automatically
        time.sleep(1)
        try:
            self.enter_text(self.TO_CITY_INPUT, to_city)
        except:
             # If input is not visible yet, click the label to trigger it
             self.click_element(self.TO_CITY_LABEL)
             self.enter_text(self.TO_CITY_INPUT, to_city)
             
        time.sleep(2) # Wait for suggestions to appear
        self.click_element(self.TO_CITY_SUGGESTION) # Fixed: added self.
        
    def select_departure_date(self):
        """Opens calendar and selects the first available and valid date."""
        try:
            # Check if calendar is already open (often happens after TO city selection)
            if not self.is_element_displayed(self.AVAILABLE_DATES):
                self.click_element(self.DEPARTURE_DATE_LABEL)
        except:
            self.click_element(self.DEPARTURE_DATE_LABEL)
            
        time.sleep(2) # Wait for calendar animation
        # Click the first available date that is NOT disabled or outside current month
        self.click_element(self.AVAILABLE_DATES)
        
    def click_search(self):
        """Clicks the main Search button and handles results page load."""
        print("Clicking search button...")
        self.click_element(self.SEARCH_BTN)
        time.sleep(3) # Initial redirect buffer


