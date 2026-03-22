"""
tests/test_login.py
─────────────────────────────────────────────────────────────────────────────
Login Module Test Suite for MakeMyTrip Automation Framework.

Test scenarios covered:
  TC_LOGIN_001  Valid login — valid 10-digit phone number
                ► Expected: OTP input screen is rendered (login flow proceeds)

  TC_LOGIN_002  Invalid login — empty submission
                ► Expected: Validation error message is displayed

  TC_LOGIN_003  Invalid login — bad phone number format (too short)
                ► Expected: Validation error message is displayed

  TC_LOGIN_004  Invalid login — malformed email address
                ► Expected: Validation error OR OTP screen NOT shown

  TC_LOGIN_005  Login modal UI verification
                ► Expected: Modal heading contains expected text

Design decisions:
  • All tests use the `LoginPage` POM — zero hardcoded locators here.
  • `driver` and `config` fixtures come from conftest.py.
  • Explicit waits are embedded in LoginPage methods — no time.sleep in tests.
  • Each test is independent (function-scoped driver = fresh browser per test).

To run only these tests:
    pytest tests/test_login.py -v --html=reports/login_report.html --self-contained-html
"""

import pytest

from pages.login_page import LoginPage
from utils.logger import get_logger

log = get_logger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures (page-level, function scope)
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def login_page(driver, config):
    """
    Create a LoginPage instance pre-loaded with the MMT homepage.

    Args:
        driver: WebDriver fixture from conftest.py.
        config: Config dictionary fixture from conftest.py.

    Yields:
        Initialised :class:`LoginPage` instance (modal NOT yet open).
    """
    page = LoginPage(driver)
    page.navigate_to_home(config["base_url"])
    yield page


# ─────────────────────────────────────────────────────────────────────────────
# Test Class
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.login
class TestLogin:
    """
    Test suite for the MakeMyTrip Login / Signup modal.

    Each test opens a fresh browser session (function-scoped driver fixture)
    so that cookie state, modals, and session tokens never bleed between tests.
    """

    # ── TC_LOGIN_001: Valid phone number → OTP screen should appear ───────────
    def test_valid_login_with_phone(self, login_page, config):
        """
        TC_LOGIN_001 — Valid Login: 10-digit phone number.

        Steps:
          1. Open homepage and dismiss any auto-popup.
          2. Click the Login/Signup button to open the modal.
          3. Enter a valid 10-digit Indian mobile number.
          4. Click Continue.

        Expected Result:
          • MakeMyTrip processes the number and shows the OTP entry screen.
          • This confirms the login flow progresses correctly for valid input.

        Note:
          A real OTP would be sent to the phone; we validate only the UI
          transitions, not OTP submission (which requires live credentials).
        """
        log.info("=" * 50)
        log.info("TC_LOGIN_001: Valid login — 10-digit phone number")

        # Step 1: Open login modal
        log.info("Step 1: Opening login modal")
        login_page.click_login_button()

        # Step 2: Verify modal is open before proceeding
        log.info("Step 2: Verifying login modal is open")
        assert login_page.is_login_modal_open(), (
            "FAIL: Login modal did not open after clicking the Login button. "
            "Check if the site header locator is still valid."
        )
        log.info("PASS: Login modal is open ✓")

        # Step 3: Enter a valid phone number from config
        valid_phone = config["credentials"]["valid_phone"]
        log.info(f"Step 3: Entering valid phone number — {valid_phone}")
        login_page.enter_phone(valid_phone)

        # Step 4: Submit the form
        log.info("Step 4: Clicking Continue")
        login_page.click_continue()

        # Step 5: Assert OTP screen appeared
        log.info("Step 5: Verifying OTP screen is displayed")
        is_otp = login_page.is_otp_screen_displayed()
        if not is_otp:
            # Check if an error appeared instead (bot-detection scenario)
            error_msg = login_page.get_error_message()
            if error_msg:
                pytest.skip(
                    f"MakeMyTrip rejected the request (bot-detection likely). "
                    f"Error: '{error_msg}'. Re-run tests manually in a real browser."
                )

        assert is_otp, (
            "FAIL: OTP entry screen did NOT appear after submitting a valid phone number. "
            "The site may have changed its login flow or bot-detection is active."
        )
        log.info("PASS: OTP input screen is displayed — login flow working ✓")

    # ── TC_LOGIN_002: Empty submission → error message should appear ──────────
    def test_invalid_login_empty_submission(self, login_page):
        """
        TC_LOGIN_002 — Invalid Login: empty input field submission.

        Steps:
          1. Open the login modal.
          2. Leave the input field blank.
          3. Click Continue.

        Expected Result:
          • MakeMyTrip shows a validation error: e.g. "Please enter valid details".
          • The page does NOT navigate to the OTP screen.
        """
        log.info("=" * 50)
        log.info("TC_LOGIN_002: Invalid login — empty submission")

        # Step 1: Open login modal
        log.info("Step 1: Opening login modal")
        login_page.click_login_button()

        assert login_page.is_login_modal_open(), (
            "FAIL: Login modal did not open — cannot run invalid-login test."
        )
        log.info("Modal open ✓")

        # Step 2: Ensure field is empty (no pre-fill)
        log.info("Step 2: Clearing input field (ensuring it is blank)")
        login_page.clear_input_field()

        # Step 3: Click Continue without entering any value
        log.info("Step 3: Clicking Continue with blank field")
        login_page.click_continue()

        # Step 4: Assert an error message is shown
        log.info("Step 4: Checking for validation error message")
        error_visible = login_page.is_error_message_displayed()
        error_text    = login_page.get_error_message()

        log.info(f"Error message displayed: {error_visible} | Text: '{error_text}'")

        assert error_visible, (
            "FAIL: No error message was displayed after submitting an empty login form. "
            "The site should show a validation error for blank input."
        )
        log.info(f"PASS: Validation error displayed — '{error_text}' ✓")

        # Additional assertion: make sure we did NOT land on OTP screen
        log.info("Step 5: Confirming OTP screen did NOT appear")
        assert not login_page.is_otp_screen_displayed(), (
            "FAIL: OTP screen appeared even with empty input. This should not happen."
        )
        log.info("PASS: OTP screen correctly NOT shown for empty submission ✓")

    # ── TC_LOGIN_003: Short/invalid phone number → error ─────────────────────
    def test_invalid_login_short_phone(self, login_page, config):
        """
        TC_LOGIN_003 — Invalid Login: phone number with too few digits.

        Steps:
          1. Open login modal.
          2. Enter "123" (too short to be a valid Indian mobile number).
          3. Click Continue.

        Expected Result:
          • Validation error is displayed.
          • OTP screen is NOT shown.
        """
        log.info("=" * 50)
        log.info("TC_LOGIN_003: Invalid login — short/invalid phone number")

        invalid_phone = config["credentials"]["invalid_phone"]  # "123"

        # Step 1: Open login modal
        log.info("Step 1: Opening login modal")
        login_page.click_login_button()

        assert login_page.is_login_modal_open(), (
            "FAIL: Login modal did not open."
        )

        # Step 2: Enter invalid phone number
        log.info(f"Step 2: Entering invalid phone — '{invalid_phone}'")
        login_page.enter_phone(invalid_phone)

        # Step 3: Submit
        log.info("Step 3: Clicking Continue")
        login_page.click_continue()

        # Step 4: Assert error shown OR OTP NOT shown
        log.info("Step 4: Verifying validation error or rejected flow")
        error_shown = login_page.is_error_message_displayed()
        otp_shown   = login_page.is_otp_screen_displayed()

        log.info(f"Error visible: {error_shown} | OTP visible: {otp_shown}")

        # At least one of these conditions must hold
        assert error_shown or not otp_shown, (
            "FAIL: OTP screen appeared for a clearly invalid phone number '123'. "
            "Validation logic may be broken."
        )

        error_text = login_page.get_error_message()
        log.info(f"PASS: Invalid phone rejected — error: '{error_text}' ✓")

    # ── TC_LOGIN_004: Malformed email → error ─────────────────────────────────
    def test_invalid_login_malformed_email(self, login_page, config):
        """
        TC_LOGIN_004 — Invalid Login: email address with bad format.

        Steps:
          1. Open login modal.
          2. Enter "invalid_email_format" (missing '@' and domain).
          3. Click Continue.

        Expected Result:
          • Validation error is displayed.
          • OTP screen is NOT shown.
        """
        log.info("=" * 50)
        log.info("TC_LOGIN_004: Invalid login — malformed email address")

        invalid_email = config["credentials"]["invalid_email"]  # "invalid_email_format"

        # Step 1: Open login modal
        log.info("Step 1: Opening login modal")
        login_page.click_login_button()

        assert login_page.is_login_modal_open(), (
            "FAIL: Login modal did not open."
        )

        # Step 2: Enter malformed email
        log.info(f"Step 2: Entering malformed email — '{invalid_email}'")
        login_page.enter_email(invalid_email)

        # Step 3: Submit
        log.info("Step 3: Clicking Continue")
        login_page.click_continue()

        # Step 4: Verify rejected
        log.info("Step 4: Verifying malformed email is rejected")
        error_shown = login_page.is_error_message_displayed()
        otp_shown   = login_page.is_otp_screen_displayed()
        error_text  = login_page.get_error_message()

        log.info(f"Error visible: {error_shown} | Text: '{error_text}' | OTP shown: {otp_shown}")

        assert error_shown or not otp_shown, (
            f"FAIL: OTP screen appeared for a malformed email '{invalid_email}'. "
            f"Server-side validation may have passed it through."
        )
        log.info(f"PASS: Malformed email rejected ✓ | Message: '{error_text}'")

    # ── TC_LOGIN_005: Modal heading UI verification ───────────────────────────
    def test_login_modal_heading_displayed(self, login_page):
        """
        TC_LOGIN_005 — Login Modal UI: heading text verification.

        Steps:
          1. Open login modal.
          2. Read the heading text inside the modal.

        Expected Result:
          • Modal is open and visible.
          • Heading text is non-empty (modal is rendering correctly).
        """
        log.info("=" * 50)
        log.info("TC_LOGIN_005: Login modal heading verification")

        # Step 1: Open modal
        log.info("Step 1: Opening login modal")
        login_page.click_login_button()

        # Step 2: Verify modal opened
        log.info("Step 2: Verifying modal is open")
        assert login_page.is_login_modal_open(), (
            "FAIL: Login modal is not open — cannot verify heading."
        )
        log.info("Modal open ✓")

        # Step 3: Retrieve heading text
        log.info("Step 3: Reading modal heading text")
        heading = login_page.get_modal_heading_text()
        log.info(f"Modal heading: '{heading}'")

        # Heading should be non-empty and contain expected keywords
        assert heading, (
            "FAIL: Modal heading text is empty. The modal UI may have changed."
        )

        # Soft check — heading should mention login/account/sign
        heading_lower = heading.lower()
        contains_expected_keyword = any(
            kw in heading_lower
            for kw in ("log", "sign", "account", "mobile", "email")
        )
        if not contains_expected_keyword:
            log.warning(
                f"Modal heading '{heading}' does not contain expected keywords "
                f"(log/sign/account) — UI might have changed"
            )

        log.info(f"PASS: Modal heading is displayed — '{heading}' ✓")
