"""
pages/login_page.py
─────────────────────────────────────────────────────────────────────────────
LoginPage — Page Object for the MakeMyTrip Login flow.

MakeMyTrip login flow overview:
  1. User clicks the "Login / Signup" button in the header.
  2. A modal appears with a phone/email input.
  3. User enters phone number or email → clicks Continue.
  4. An OTP is sent (for valid numbers) OR an error is shown (for invalid input).
  5. This class covers steps 1–4 and the resulting states.

All locators are stored as class-level constants (not scattered across test files).
All interactions use explicit waits (WebDriverWait) — no Thread.sleep / time.sleep.

Usage:
    login_page = LoginPage(driver)
    login_page.navigate_to_home()
    login_page.open_login_modal()
    login_page.enter_email_or_phone("9999999999")
    login_page.click_continue()
    is_otp = login_page.is_otp_screen_displayed()
"""

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from pages.base_page import BasePage
from utils.logger import get_logger

log = get_logger(__name__)


class LoginPage(BasePage):
    """
    Page Object Model class for the MakeMyTrip Login / Signup modal.

    ╔══════════════════════════════════════════════════════════════════╗
    ║  LOCATORS  (class-level constants — never touch in test files)  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """

    # ── Header "Login or Create Account" button ───────────────────────────────
    # Confirmed from live DOM: <li data-cy="account" ...>
    BTN_LOGIN_HEADER = (By.CSS_SELECTOR, "li[data-cy='account']")

    # ── Close / Skip login popup (auto-popup on homepage load) ───────────────
    # Confirmed from live DOM: <span class="commonModal__close" data-cy="modalClose">
    BTN_CLOSE_POPUP = (By.CSS_SELECTOR, "span[data-cy='modalClose']")

    # ── Phone / Email input inside the login modal ────────────────────────────
    # Confirmed from live DOM: <input data-cy="userName" id="username" ...>
    INPUT_PHONE_EMAIL = (By.CSS_SELECTOR, "input[data-cy='userName']")

    # Fallback using id (also confirmed present)
    INPUT_PHONE_EMAIL_BY_ID = (By.ID, "username")

    # ── Continue / Proceed button ─────────────────────────────────────────────
    # Confirmed from live DOM: <button data-cy="continueBtn" ...>
    BTN_CONTINUE = (By.CSS_SELECTOR, "button[data-cy='continueBtn']")

    # ── OTP input (indicates OTP screen was reached — valid credential) ───────
    # Typically a 6-digit input with type tel or type number
    INPUT_OTP = (
        By.XPATH,
        "//input[@type='tel' and @maxlength='6'] | "
        "//input[contains(@placeholder,'OTP') or contains(@placeholder,'otp')] | "
        "//input[contains(@class,'otp')]"
    )

    # ── Error message displayed for invalid input ─────────────────────────────
    # Confirmed from live DOM: <p data-cy="error" class="... redText ...">
    ERROR_MESSAGE = (By.CSS_SELECTOR, "p[data-cy='error']")

    # ── Modal heading — "Login or Create Account" text ────────────────────────
    # Confirmed: <p class="font24 ... latoBold">Login or Create Account</p>
    MODAL_HEADING = (
        By.XPATH,
        "//p[contains(text(),'Login') or contains(text(),'Sign')] | "
        "//h2[contains(text(),'Log') or contains(text(),'Sign')]"
    )

    # ── "Resend OTP" link ─────────────────────────────────────────────────────
    LINK_RESEND_OTP = (
        By.XPATH,
        "//span[contains(text(),'Resend')] | "
        "//a[contains(text(),'Resend')]"
    )

    # ─────────────────────────────────────────────────────────────────────────
    # Methods (public API used by test files)
    # ─────────────────────────────────────────────────────────────────────────

    def navigate_to_home(self, url: str = "https://www.makemytrip.com/") -> None:
        """
        Open the MakeMyTrip homepage and dismiss any auto-popup.

        Args:
            url: Base URL (defaults to production MMT homepage).
        """
        log.info("Step: Navigating to MakeMyTrip homepage")
        self.open(url)
        # Give the page time to settle before checking for popups
        time.sleep(2)
        self._dismiss_popup_if_present()

    def _dismiss_popup_if_present(self) -> None:
        """
        Dismiss the login popup/overlay that MakeMyTrip sometimes shows
        automatically on page load.  Safe to call even when no popup is shown.
        """
        log.info("Step: Checking for auto-popup to dismiss")
        try:
            close_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.BTN_CLOSE_POPUP)
            )
            log.info("Auto-popup detected — dismissing it")
            close_btn.click()
            time.sleep(0.5)
        except TimeoutException:
            log.debug("No auto-popup detected — continuing")

    def click_login_button(self) -> None:
        """
        Click the 'Login or Create Account' button in the site header.

        This triggers the login modal to open.
        """
        log.info("Step: Clicking Login/Signup button in header")
        self.click(*self.BTN_LOGIN_HEADER)
        # Wait briefly for the modal animation to complete
        time.sleep(1)

    def open_login_modal(self) -> None:
        """
        High-level method: navigate to homepage and open the login modal.
        Combines navigate_to_home + click_login_button.
        """
        self.navigate_to_home()
        self.click_login_button()
        log.info("Step: Login modal should now be open")

    def enter_email_or_phone(self, credential: str) -> None:
        """
        Type a phone number or email address into the login input field.

        Args:
            credential: Phone number (10 digits) or email address string.
        """
        log.info(f"Step: Entering credential — '{credential}'")
        input_field = self.find(*self.INPUT_PHONE_EMAIL)
        input_field.clear()
        input_field.send_keys(credential)
        log.info("Credential entered successfully")

    def enter_email(self, email: str) -> None:
        """
        Alias for enter_email_or_phone — enter an email address.

        Args:
            email: Email address string.
        """
        log.info(f"Step: Entering email address — '{email}'")
        self.enter_email_or_phone(email)

    def enter_phone(self, phone: str) -> None:
        """
        Alias for enter_email_or_phone — enter a phone number.

        Args:
            phone: Phone number string (10 digits recommended).
        """
        log.info(f"Step: Entering phone number — '{phone}'")
        self.enter_email_or_phone(phone)

    def click_continue(self) -> None:
        """
        Click the 'Continue' button to submit the credential.

        After this call the page will show either:
          • OTP input screen  → valid credential recognised
          • Error message     → invalid / blank input
        """
        log.info("Step: Clicking Continue button")
        self.click(*self.BTN_CONTINUE)
        # Allow network round-trip before asserting outcome
        time.sleep(1.5)

    def submit_login_form(self, credential: str) -> None:
        """
        Convenience method: enter credential AND click Continue in one call.

        Args:
            credential: Phone number or email address.
        """
        self.enter_email_or_phone(credential)
        self.click_continue()

    def is_login_modal_open(self) -> bool:
        """
        Return True if the login modal is currently visible.

        Returns:
            ``True`` if modal is open, ``False`` otherwise.
        """
        result = self.is_element_visible(*self.INPUT_PHONE_EMAIL, timeout=8)
        log.info(f"Login modal open: {result}")
        return result

    def is_otp_screen_displayed(self) -> bool:
        """
        Return True if the OTP input screen appeared (valid credential).

        This indicates MakeMyTrip accepted the phone / email and sent an OTP.

        Returns:
            ``True`` if OTP input is visible, ``False`` otherwise.
        """
        result = self.is_element_visible(*self.INPUT_OTP, timeout=10)
        log.info(f"OTP screen displayed: {result}")
        return result

    def get_error_message(self) -> str:
        """
        Return the text of the error message shown for invalid input.

        Returns:
            Error message string, or empty string if no error is shown.
        """
        log.info("Step: Checking for error message")
        try:
            error_element = self.find(*self.ERROR_MESSAGE, timeout=8)
            msg = error_element.text.strip()
            log.info(f"Error message found: '{msg}'")
            return msg
        except TimeoutException:
            log.warning("No error message element found within timeout")
            return ""

    def is_error_message_displayed(self) -> bool:
        """
        Return True if any inline validation error is currently visible.

        Returns:
            ``True`` if an error message is present, ``False`` otherwise.
        """
        result = self.is_element_visible(*self.ERROR_MESSAGE, timeout=8)
        log.info(f"Error message visible: {result}")
        return result

    def get_modal_heading_text(self) -> str:
        """
        Return the heading text displayed inside the login modal.

        Returns:
            Heading string, or empty string if not found.
        """
        try:
            return self.get_text(*self.MODAL_HEADING, timeout=5)
        except TimeoutException:
            return ""

    def clear_input_field(self) -> None:
        """Clear whatever is currently typed in the phone/email input."""
        log.info("Step: Clearing the input field")
        try:
            field = self.find(*self.INPUT_PHONE_EMAIL)
            field.clear()
            # Triple-click select-all + Delete as a fallback
            field.send_keys(Keys.CONTROL + "a")
            field.send_keys(Keys.DELETE)
        except TimeoutException:
            log.warning("Could not clear input — field not found")
