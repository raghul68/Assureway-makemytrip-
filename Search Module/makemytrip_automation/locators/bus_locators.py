"""
locators/bus_locators.py
Element locators for the MakeMyTrip Bus search section.
"""

from selenium.webdriver.common.by import By


class BusLocators:
    # ── From / To city fields ──────────────────────────────────────────
    FROM_FIELD      = (By.XPATH, "//input[contains(@placeholder,'From') or contains(@id,'from')]"
                                 "[not(contains(@id,'flight'))]")
    FROM_FIELD_CSS  = (By.CSS_SELECTOR, "div.Bus-search input[placeholder*='From'],"
                                        "input[id*='busFrom'], input[id*='bus-from']")

    TO_FIELD        = (By.XPATH, "//input[contains(@placeholder,'To') or contains(@id,'to')]"
                                 "[not(contains(@id,'flight'))][2]")
    TO_FIELD_CSS    = (By.CSS_SELECTOR, "div.Bus-search input[placeholder*='To'],"
                                        "input[id*='busTo'], input[id*='bus-to']")

    # ── Suggestion dropdown ───────────────────────────────────────────
    SUGGESTION_LIST = (By.CSS_SELECTOR, "ul[role='listbox'], ul.suggestions")
    FIRST_OPTION    = (By.XPATH, "(//ul[@role='listbox']//li)[1] | "
                                 "(//div[contains(@class,'suggestion')]//li)[1]")

    # ── Travel date ───────────────────────────────────────────────────
    DATE_FIELD      = (By.CSS_SELECTOR, "[data-cy='travelDate'], "
                                        "div.dateInput, div[class*='dateContainer']")
    DATE_FIELD_XPATH = (By.XPATH, "//label[contains(text(),'Travel Date') or contains(text(),'Date')]"
                                  "//following::div[1]")
    CALENDAR_NEXT   = (By.CSS_SELECTOR, ".DayPicker-NavButton--next, span[class*='nextMonth']")
    DATE_CELL       = (By.XPATH, "//div[@aria-label='{date}' and not(contains(@class,'disabled'))]"
                                 " | //p[@aria-label='{date}']")

    # ── Search button ─────────────────────────────────────────────────
    SEARCH_BTN      = (By.CSS_SELECTOR, "a.primaryBtn, button.primaryBtn")
    SEARCH_BTN_XPATH = (By.XPATH, "//a[contains(@class,'primaryBtn')] | "
                                  "//button[contains(text(),'Search')]")

    # ── Results ───────────────────────────────────────────────────────
    RESULTS_CONTAINER = (By.CSS_SELECTOR, ".busListing, div[class*='busListing'], "
                                          "div[class*='busResult']")
    BUS_CARD          = (By.CSS_SELECTOR, ".busItem, .busCard, div[class*='busCard'], "
                                          "div[class*='busItem']")
    NO_RESULTS_MSG    = (By.XPATH, "//div[contains(text(),'No buses') or contains(text(),'Oops')]")
