"""
locators/hotel_locators.py
Element locators for the MakeMyTrip Hotels search section.
"""

from selenium.webdriver.common.by import By


class HotelLocators:
    # ── City / Destination field ───────────────────────────────────────
    CITY_FIELD       = (By.CSS_SELECTOR, "[data-cy='city'], input[placeholder*='City'],"
                                         "input[placeholder*='Destination'], input[placeholder*='hotel']")
    CITY_FIELD_XPATH = (By.XPATH, "//label[contains(text(),'City') or contains(text(),'Hotel')]"
                                  "//following::input[1]")
    CITY_SUGGESTION  = (By.CSS_SELECTOR, "ul[role='listbox'] li, li[data-id]")
    CITY_FIRST_ITEM  = (By.XPATH, "(//ul[@role='listbox']//li)[1]")

    # ── Check-in date ──────────────────────────────────────────────────
    CHECKIN_FIELD       = (By.XPATH, "//label[contains(text(),'Check-In') or contains(text(),'Check In')]"
                                     "//following::div[1] | //div[@id='checkin']")
    CHECKIN_FIELD_CSS   = (By.CSS_SELECTOR, "[data-cy='checkin'], div.checkIn")

    # ── Check-out date ─────────────────────────────────────────────────
    CHECKOUT_FIELD      = (By.XPATH, "//label[contains(text(),'Check-Out') or contains(text(),'Check Out')]"
                                     "//following::div[1] | //div[@id='checkout']")
    CHECKOUT_FIELD_CSS  = (By.CSS_SELECTOR, "[data-cy='checkout'], div.checkOut")

    # ── Common calendar ────────────────────────────────────────────────
    CALENDAR_NEXT_BTN   = (By.CSS_SELECTOR, "span.DayPicker-NavButton--next, .DayPicker-NavButton--next")
    DATE_CELL           = (By.XPATH, "//div[@aria-label='{date}' and not(contains(@class,'disabled'))] "
                                     "| //p[@aria-label='{date}']")
    DATE_CELL_CSS       = (By.CSS_SELECTOR, "[aria-label='{date}']")
    APPLY_BTN           = (By.XPATH, "//button[text()='Apply'] | //a[text()='APPLY']")

    # ── Guests / Rooms ─────────────────────────────────────────────────
    GUESTS_FIELD        = (By.CSS_SELECTOR, "[data-cy='guests'], div.guestContainer")
    ROOMS_PLUS_BTN      = (By.XPATH, "(//div[contains(@class,'addRooms') or contains(@class,'addGuest')]"
                                     "//span[contains(@class,'plus')])[1]")
    ADULTS_PLUS_BTN     = (By.XPATH, "(//div[contains(@class,'addAdult')]//span[contains(@class,'plus')])[1]")
    DONE_BTN            = (By.XPATH, "//button[contains(text(),'Done') or contains(text(),'DONE')]")

    # ── Search button ──────────────────────────────────────────────────
    SEARCH_BTN          = (By.CSS_SELECTOR, "a.primaryBtn, button.primaryBtn")
    SEARCH_BTN_XPATH    = (By.XPATH, "//a[contains(@class,'primaryBtn')] | "
                                     "//button[contains(text(),'Search')]")

    # ── Results ────────────────────────────────────────────────────────
    RESULTS_CONTAINER   = (By.CSS_SELECTOR, ".listingPage, div[class*='listing']")
    HOTEL_CARD          = (By.CSS_SELECTOR, ".mmt-hotel, .hotelCard, div[class*='hotelCard'], "
                                           "div[class*='srpHotel']")
    NO_RESULTS_MSG      = (By.XPATH, "//div[contains(text(),'No hotels') or contains(text(),'Oops')]")
