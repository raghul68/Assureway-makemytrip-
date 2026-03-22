"""
locators/home_locators.py
Element locators for the MakeMyTrip Home Page.
All locators use By.<strategy> tuples — (By.X, "value").
"""

from selenium.webdriver.common.by import By


class HomeLocators:
    # ── Login popup ────────────────────────────────────────────────────
    LOGIN_POPUP            = (By.CSS_SELECTOR, ".modal-backdrop, div[class*='loginModal']")
    LOGIN_CLOSE_BTN        = (By.CSS_SELECTOR, ".commonModal__close, .icon-close-popup, span.icon-close")
    CONTINUE_WITH_EMAIL    = (By.XPATH, "//a[contains(text(),'Continue with Email')]")
    CLOSE_MODAL_BTN        = (By.XPATH, "//span[contains(@class,'close') or contains(@class,'modalClose')]")

    # ── Main navigation tabs ───────────────────────────────────────────
    FLIGHTS_TAB    = (By.XPATH, "//li[@data-cy='menu_Flights'] | //span[contains(@class,'Flights')]")
    HOTELS_TAB     = (By.XPATH, "//li[@data-cy='menu_Hotels'] | //span[contains(@class,'Hotels')] | //a[contains(@href,'hotels')]")
    BUS_TAB        = (By.XPATH, "//li[@data-cy='menu_Buses'] | //span[contains(@class,'Buses')] | //a[contains(@href,'bus')]")
    
    # Text-based fallbacks
    FLIGHTS_TEXT   = (By.XPATH, "//span[text()='Flights']")
    HOTELS_TEXT    = (By.XPATH, "//span[text()='Hotels']")
    BUS_TEXT       = (By.XPATH, "//span[text()='Buses']")

    # Alternative tab selectors
    FLIGHTS_TAB_ALT = (By.CSS_SELECTOR, "li[data-cy='menu_Flights'], a[href*='flights']")
    HOTELS_TAB_ALT  = (By.CSS_SELECTOR, "li[data-cy='menu_Hotels'], a[href*='hotels']")
    BUS_TAB_ALT     = (By.CSS_SELECTOR, "li[data-cy='menu_Buses'], a[href*='bus']")

    # ── Generic ────────────────────────────────────────────────────────
    BODY = (By.TAG_NAME, "body")
