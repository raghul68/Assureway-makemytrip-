from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class MMTPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.actions = ActionChains(driver)

    # Improved Locators
    LOGIN_CLOSE = (By.XPATH, "//span[contains(@class, 'commonModal__close')] | //div[contains(@class, 'close')] | //i[contains(@class, 'wewidget_close')]")
    FROM_CITY = (By.ID, "fromCity")
    TO_CITY = (By.ID, "toCity")
    FROM_INPUT = (By.XPATH, "//input[@placeholder='From'] | //input[@aria-autocomplete='list']")
    TO_INPUT = (By.XPATH, "//input[@placeholder='To'] | //input[@aria-autocomplete='list']")
    CITY_SUGGESTION = (By.XPATH, "//li[@role='option'] | //div[contains(@class, 'react-autosuggest')]//li")
    SEARCH_BTN = (By.XPATH, "//a[contains(@class, 'widgetSearchBtn')] | //button[text()='SEARCH']")
    VIEW_FARE_BTN = (By.XPATH, "//button[contains(translate(text(), 'VIEWPRIC', 'viewpric'), 'view prices')] | //button[contains(text(), 'View Fare')]")
    BOOK_NOW_BTN = (By.XPATH, "//button[contains(text(), 'Book Now') or contains(text(), 'BOOK NOW')]")
    ADD_ADULT_BTN = (By.XPATH, "//*[contains(text(), '+ ADD NEW ADULT')]")
    FIRST_NAME = (By.XPATH, "//input[@placeholder='First Name']")
    LAST_NAME = (By.XPATH, "//input[@placeholder='Last Name']")
    GENDER_MALE = (By.XPATH, "//label[contains(., 'MALE')]//span")
    MOBILE = (By.XPATH, "//input[@placeholder='Mobile No']")
    EMAIL = (By.XPATH, "//input[@placeholder='Email']")
    STATE_DROPDOWN = (By.XPATH, "//div[contains(@class, 'select__control')] | //div[@id='dt_state_gst_info']")
    STATE_OPTION = (By.XPATH, "//div[contains(@class, 'select__option')]")
    REVIEW_CONTINUE = (By.XPATH, "//button[contains(translate(text(), 'CONTINUE', 'continue'), 'continue')]")
    CONFIRM_BTN = (By.XPATH, "//button[contains(text(), 'CONFIRM') or contains(text(), 'Confirm')]")
    YES_SECURE_TRIP = (By.XPATH, "//*[contains(text(), 'Secure my trip')]")
    PRICE_DISPLAY = (By.XPATH, "//p[contains(@class, 'totalAmount')] | //span[contains(@class, 'totalAmount')] | //span[contains(@class, 'font20')]")
    PAYMENT_OPTIONS = (By.XPATH, "//div[contains(@id, 'PAYMENT_METHODS')] | //div[contains(@class, 'paymentTab')]")

    def close_popup(self):
        # List of potential close button locators
        closers = [
            (By.XPATH, "//span[contains(@class, 'commonModal__close')]"),
            (By.XPATH, "//span[@data-cy='closeModal']"),
            (By.XPATH, "//div[contains(@class, 'close')]"),
            (By.XPATH, "//i[contains(@class, 'wewidget_close')]")
        ]
        for locator in closers:
            try:
                elements = self.driver.find_elements(*locator)
                if elements and elements[0].is_displayed():
                    elements[0].click()
            except: pass
        
        # Click on body as fallback
        try:
            self.driver.find_element(By.TAG_NAME, "body").click()
        except: pass

    def search_flights(self, from_city, to_city):
        try:
            # Human-like mouse move
            target = self.wait.until(EC.element_to_be_clickable(self.FROM_CITY))
            self.actions.move_to_element(target).pause(0.5).click().perform()
        except: pass
        
        from_input = self.wait.until(EC.visibility_of_element_located(self.FROM_INPUT))
        from_input.send_keys(from_city)
        # Mouse move to suggestion
        suggestion = self.wait.until(EC.element_to_be_clickable(self.CITY_SUGGESTION))
        self.actions.move_to_element(suggestion).pause(0.3).click().perform()

        try:
            # Same for toCity
            target_to = self.wait.until(EC.element_to_be_clickable(self.TO_CITY))
            self.actions.move_to_element(target_to).pause(0.5).click().perform()
        except: pass
        
        to_input = self.wait.until(EC.visibility_of_element_located(self.TO_INPUT))
        to_input.send_keys(to_city)
        suggestion_to = self.wait.until(EC.element_to_be_clickable(self.CITY_SUGGESTION))
        self.actions.move_to_element(suggestion_to).pause(0.3).click().perform()

        # Final check if modal is overlaying search
        self.close_popup()

        # Click Search with JS as fallback if overlay remains
        search_btn = self.wait.until(EC.element_to_be_clickable(self.SEARCH_BTN))
        try:
            search_btn.click()
        except:
            self.driver.execute_script("arguments[0].click();", search_btn)

    def select_first_flight(self):
        # Wait for results and handle potential blocking popup
        try:
            self.close_popup()
        except: pass

        self.wait.until(EC.presence_of_element_located(self.VIEW_FARE_BTN))
        view_fares = self.driver.find_elements(*self.VIEW_FARE_BTN)
        if view_fares:
            view_fares[0].click()
        
        self.wait.until(EC.element_to_be_clickable(self.BOOK_NOW_BTN)).click()

    def fill_traveler_details(self, data):
        # Handle Tab switch
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])

        self.wait.until(EC.element_to_be_clickable(self.ADD_ADULT_BTN)).click()
        self.driver.find_element(*self.FIRST_NAME).send_keys(data['firstName'])
        self.driver.find_element(*self.LAST_NAME).send_keys(data['lastName'])
        self.driver.find_element(*self.GENDER_MALE).click()
        self.driver.find_element(*self.MOBILE).send_keys(data['mobile'])
        self.driver.find_element(*self.EMAIL).send_keys(data['email'])
        
        # State Selection
        try:
            state_container = self.wait.until(EC.element_to_be_clickable(self.STATE_DROPDOWN))
            state_container.click()
            state_options = self.wait.until(EC.presence_of_all_elements_located(self.STATE_OPTION))
            for option in state_options:
                if data['state'] in option.text:
                    option.click()
                    break
        except: pass

        self.wait.until(EC.element_to_be_clickable(self.REVIEW_CONTINUE)).click()
        
        try:
            # Handle various confirmation buttons
            self.wait.until(EC.element_to_be_clickable(self.CONFIRM_BTN)).click()
        except: pass
        
        try:
            # Skip Seat Selection if possible
            self.wait.until(EC.element_to_be_clickable(self.REVIEW_CONTINUE)).click()
        except: pass

    def get_price(self):
        return self.wait.until(EC.visibility_of_element_located(self.PRICE_DISPLAY)).text

    def are_payment_options_visible(self):
        options = self.wait.until(EC.presence_of_all_elements_located(self.PAYMENT_OPTIONS))
        return len(options) > 0
