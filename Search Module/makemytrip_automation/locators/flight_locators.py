"""
locators/flight_locators.py
Element locators for the MakeMyTrip Flights search section.
"""

from selenium.webdriver.common.by import By


class FlightLocators:
    # ── Trip type ──────────────────────────────────────────────────────
    ONE_WAY_RADIO    = (By.XPATH, "//span[text()='One Way']")
    ROUND_TRIP_RADIO = (By.XPATH, "//span[text()='Round Trip']")

    # ── From / To city fields ──────────────────────────────────────────
    FROM_FIELD    = (By.XPATH, "//label[contains(@for,'fromCity') or @data-cy='fromCity']//following::div[1]"
                               "| //input[@placeholder='From' or @id='fromCity']")
    FROM_FIELD_V2 = (By.CSS_SELECTOR, "[id='fromCity'], div[class*='fromCity']")
    FROM_INPUT    = (By.XPATH, "//input[contains(@placeholder,'From') or contains(@placeholder,'Departure City')]")

    TO_FIELD      = (By.XPATH, "//label[contains(@for,'toCity') or @data-cy='toCity']//following::div[1]")
    TO_FIELD_V2   = (By.CSS_SELECTOR, "[id='toCity'], div[class*='toCity']")
    TO_INPUT      = (By.XPATH, "//input[contains(@placeholder,'To') or contains(@placeholder,'Arrival City')]")

    # ── Dropdown suggestion list ───────────────────────────────────────
    SUGGESTION_LIST  = (By.CSS_SELECTOR, "ul[role='listbox'], ul.c-suggestions-list")
    SUGGESTION_ITEM  = (By.XPATH, "//ul[contains(@class,'suggestion') or @role='listbox']//li[1]")
    AIRPORT_ITEM     = (By.XPATH, "//p[contains(@class,'city_name') or contains(@class,'cityName')]"
                                  "/ancestor::li[1]")

    # ── Departure date ─────────────────────────────────────────────────
    DEPART_DATE_FIELD = (By.XPATH, "//label[contains(@for,'departure') or contains(text(),'Departure')]"
                                   "//following::div[1] | //div[@id='departure']")
    CALENDAR_NEXT_BTN = (By.CSS_SELECTOR, "span.DayPicker-NavButton--next, button.DayPicker-NavButton--next")
    CALENDAR_PREV_BTN = (By.CSS_SELECTOR, "span.DayPicker-NavButton--prev")
    DATE_CELL         = (By.XPATH, "//div[@aria-label='{date}' and not(contains(@class,'disabled'))]"
                                   "| //p[@aria-label='{date}']")
    # Use .format(date='19 Mar 2025') when building xpath

    # ── Passengers ─────────────────────────────────────────────────────
    PASSENGER_FIELD = (By.CSS_SELECTOR, "[data-cy='paxCount'], div.paxContainer")

    # ── Search button ──────────────────────────────────────────────────
    SEARCH_BTN      = (By.CSS_SELECTOR, "a.primaryBtn[data-cy='submit'], button.primaryBtn, "
                                        "a[class*='btnClass'][class*='primary']")
    SEARCH_BTN_XPATH = (By.XPATH, "//a[contains(@class,'primaryBtn')] | "
                                  "//button[contains(text(),'Search')] | "
                                  "//a[@data-cy='submit']")

    # ── Results page indicators ────────────────────────────────────────
    RESULTS_CONTAINER = (By.CSS_SELECTOR, ".listingPage, div[class*='listingPage'], "
                                          "div[class*='flightList']")
    FLIGHT_CARD       = (By.CSS_SELECTOR, ".airItenary, div[class*='airItenary'], "
                                          "div[class*='resultsWrap']")
    NO_RESULTS_MSG    = (By.XPATH, "//div[contains(text(),'No flights found') or "
                                   "contains(text(),'Oops')]")
