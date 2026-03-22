from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging

class DetailsPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)
        self.logger = logging.getLogger("DetailsPage")

    def open(self):
        self.driver.get("https://www.makemytrip.com/")
        self.logger.info("Opened MakeMyTrip homepage.")
        
    def close_login_popup(self):
        try:
            # First handling typical "Sign In" popups
            login_close_locator = (By.CSS_SELECTOR, "span.commonModal__close, [data-cy='closeModal']")
            btn = self.wait.until(EC.element_to_be_clickable(login_close_locator))
            btn.click()
            self.logger.info("Closed login popup.")
        except TimeoutException:
            self.logger.info("No login popup appeared within timeout.")
            # Sometimes an iframe or body overlay blocks it
            try:
                self.driver.execute_script("document.body.click();")
            except Exception:
                pass

    def perform_search(self, category):
        try:
            menu_locator = {
                "flight": (By.XPATH, "//li[contains(@class, 'menu_Flights')]"),
                "hotel": (By.XPATH, "//li[contains(@class, 'menu_Hotels')]"),
                "bus": (By.XPATH, "//li[contains(@class, 'menu_Buses')]")
            }[category]
            
            # Click Category Menu
            menu = self.wait.until(EC.element_to_be_clickable(menu_locator))
            self.driver.execute_script("arguments[0].click();", menu)
            self.logger.info(f"Clicked on {category} menu.")
            
            # Click Search
            search_btn_loc = (By.XPATH, "//a[contains(@class,'primaryBtn')] | //button[contains(@class,'primaryBtn')]")
            search_btn = self.wait.until(EC.element_to_be_clickable(search_btn_loc))
            self.driver.execute_script("arguments[0].click();", search_btn)
            self.logger.info(f"Clicked on {category} search button.")
            
        except Exception as e:
            self.logger.error(f"Error while performing {category} search: {e}")
            raise

    def switch_to_new_tab(self):
        try:
            self.wait.until(EC.number_of_windows_to_be(2))
            tabs = self.driver.window_handles
            self.driver.switch_to.window(tabs[-1])
            self.logger.info("Switched to new tab.")
        except TimeoutException:
            self.logger.info("No new tab to switch to.")

    def select_first_result(self, category):
        from selenium.common.exceptions import StaleElementReferenceException
        import time
        try:
            if category == "flight":
                booking_btn_locator = (By.XPATH, "(//button[contains(.,'VIEW PRICES') or contains(.,'View Prices') or contains(.,'BOOK NOW')])[1]")
                for _ in range(3):
                    try:
                        btn = self.wait.until(EC.element_to_be_clickable(booking_btn_locator))
                        self.driver.execute_script("arguments[0].click();", btn)
                        break
                    except StaleElementReferenceException:
                        time.sleep(1)
                
                try:
                    for _ in range(3):
                        try:
                            book_now_btn = WebDriverWait(self.driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, "(//button[contains(.,'BOOK NOW')])[1]"))
                            )
                            self.driver.execute_script("arguments[0].click();", book_now_btn)
                            break
                        except StaleElementReferenceException:
                            time.sleep(1)
                except TimeoutException:
                    pass
                
                self.logger.info("Selected first flight result.")
                
            elif category == "hotel":
                hotel_card_locator = (By.XPATH, "(//div[contains(@class,'hotelCard') or @id='hotelListingContainer'])[1]")
                for _ in range(3):
                    try:
                        card = self.wait.until(EC.element_to_be_clickable(hotel_card_locator))
                        self.driver.execute_script("arguments[0].click();", card)
                        break
                    except StaleElementReferenceException:
                        time.sleep(1)
                self.logger.info("Selected first hotel result.")
                self.switch_to_new_tab()
                
            elif category == "bus":
                bus_card_locator = (By.XPATH, "(//div[contains(@class,'busCard') or contains(@class,'bus-card') or contains(., 'Select Seats')])[1]")
                for _ in range(3):
                    try:
                        card = self.wait.until(EC.element_to_be_clickable(bus_card_locator))
                        self.driver.execute_script("arguments[0].click();", card)
                        break
                    except StaleElementReferenceException:
                        time.sleep(1)
                self.logger.info("Selected first bus result.")
                
        except Exception as e:
            self.logger.error(f"Error clicking first {category} result: {e}")
            raise

    def get_details(self, category):
        details = {}
        try:
            if category == "flight":
                airline_loc = (By.XPATH, "(//*[contains(@class,'airlineName') or contains(@class,'airways-name')])[1]")
                price_loc = (By.XPATH, "(//*[contains(@class,'price') or contains(@class,'blackFont') or contains(@class,'fare')])[1]")
                timing_loc = (By.XPATH, "(//*[contains(@class,'timeInfo') or contains(@class,'time') or contains(@class,'flightTimeInfo')])[1]")
                
                details["airline"] = self.wait.until(EC.visibility_of_element_located(airline_loc)).text
                details["price"] = self.wait.until(EC.visibility_of_element_located(price_loc)).text
                details["timing"] = self.wait.until(EC.visibility_of_element_located(timing_loc)).text
                self.logger.info(f"Retrieved flight details: {details}")

            elif category == "hotel":
                name_loc = (By.XPATH, "//*[@id='detpg_hotel_name'] | //h1")
                price_loc = (By.XPATH, "//*[@id='detpg_cart_total'] | //*[contains(@class,'price')]")
                rating_loc = (By.XPATH, "//*[contains(@class,'ratingStar') or contains(@class,'rating')]")
                
                details["name"] = self.wait.until(EC.visibility_of_element_located(name_loc)).text
                try:
                    details["price"] = self.wait.until(EC.visibility_of_element_located(price_loc)).text
                except TimeoutException:
                    details["price"] = "Price not found"
                try:
                    details["rating"] = self.wait.until(EC.visibility_of_element_located(rating_loc)).text
                except TimeoutException:
                    details["rating"] = "Rating not found"
                self.logger.info(f"Retrieved hotel details: {details}")

            elif category == "bus":
                operator_loc = (By.XPATH, "(//*[contains(@class,'busName') or contains(@class,'operator') or contains(@class,'title')])[1]")
                timing_loc = (By.XPATH, "(//*[contains(@class,'busTiming') or contains(@class,'time') or contains(@class,'duration')])[1]")
                price_loc = (By.XPATH, "(//*[contains(@class,'busPrice') or contains(@class,'price') or contains(@class,'fare')])[1]")
                
                details["operator"] = self.wait.until(EC.visibility_of_element_located(operator_loc)).text
                details["timing"] = self.wait.until(EC.visibility_of_element_located(timing_loc)).text
                details["price"] = self.wait.until(EC.visibility_of_element_located(price_loc)).text
                self.logger.info(f"Retrieved bus details: {details}")

        except Exception as e:
            self.logger.error(f"Error while getting {category} details: {e}")
            raise

        return details
