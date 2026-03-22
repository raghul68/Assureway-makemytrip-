from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BasePage:
    """
    Base Page class that contains common Selenium actions and utilities.
    Other page objects should inherit from this class.
    """
    
    def __init__(self, driver):
        self.driver = driver
        # Use explicit wait (WebDriverWait) initialized for 15 seconds
        self.wait = WebDriverWait(self.driver, 15)
        
    def open_url(self, url):
        """Navigates the browser to the specified URL."""
        self.driver.get(url)
        
    def get_title(self):
        """Returns the current page title."""
        return self.driver.title
        
    def wait_for_element_visible(self, locator):
        """Waits until an element is visible on the page."""
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            print(f"Error: Element {locator} not visible after timeout.")
            return None
            
    def force_close_modals(self):
        """Attempts to close common MakeMyTrip modals if they are visible."""
        print("Scrubbing for potential modals/popups...")
        locators = [
            (By.CSS_SELECTOR, ".commonModal__close"),
            (By.ID, "webklipper-publisher-widget-container-notification-close-div"),
            (By.CSS_SELECTOR, "[data-cy='closeModal']"),
            (By.CLASS_NAME, "close")
        ]
        for locator in locators:
            try:
                # Use a very short timeout for rapid cleanup
                wait = WebDriverWait(self.driver, 2)
                element = wait.until(EC.presence_of_element_located(locator))
                self.driver.execute_script("arguments[0].click();", element)
                print(f"Dismissed modal: {locator}")
            except:
                pass


    def click_element(self, locator):
        """Waits for an element to be clickable and performs a click. Falls back to JS click if blocked."""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except Exception:
            try:
                # Fallback to JS click if standard click is intercepted or fails
                element = self.driver.find_element(*locator)
                self.driver.execute_script("arguments[0].click();", element)
                print(f"Clicked element using JS fallback: {locator}")
            except Exception as e:
                 print(f"Error: Element {locator} still not clickable. {e}")
            
    def enter_text(self, locator, text):
        """Waits for an element to be visible, clears it, and types text."""
        element = self.wait_for_element_visible(locator)
        if element:
            element.clear()
            element.send_keys(text)
            
    def is_element_displayed(self, locator):
        """Checks if an element is currently displayed on the page."""
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except NoSuchElementException:
            return False
