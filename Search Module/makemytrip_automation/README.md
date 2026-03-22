# MakeMyTrip Selenium Automation Framework (Python + Pytest)

> A scalable, modular Selenium test automation framework for **MakeMyTrip** 
> built with **Python**, **Pytest**, and the **Page Object Model (POM)** design pattern.

---

## 📋 Table of Contents

- [Framework Overview](#framework-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Reports & Screenshots](#reports--screenshots)
- [Test Scenarios](#test-scenarios)
- [Framework Architecture](#framework-architecture)

---

## Framework Overview

| Feature | Details |
|---|---|
| Language | Python 3.8+ |
| Framework | Pytest |
| Browser Automation | Selenium 4 |
| Architecture | Page Object Model (POM) |
| Reporting | pytest-html (self-contained HTML) |
| Logging | Python `logging` module (console + file) |
| Driver Management | WebDriver Manager (auto-downloads ChromeDriver) |
| Configuration | YAML external config file |
| Screenshot | Auto-capture on test failure |

---

## Prerequisites

- **Python** 3.8 or later — [Download](https://www.python.org/downloads/)
- **Google Chrome** (latest stable) — [Download](https://www.google.com/chrome/)
- **Git** — [Download](https://git-scm.com/)
- Internet connection (to access MakeMyTrip)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/makemytrip-automation.git
cd makemytrip-automation
```

### 2. Create a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Project Structure

```
makemytrip_automation/
│
├── config/
│   └── config.yaml            ← External configuration (URL, browser, test data)
│
├── locators/
│   ├── home_locators.py       ← Homepage element locators
│   ├── flight_locators.py     ← Flight search element locators
│   ├── hotel_locators.py      ← Hotel search element locators
│   └── bus_locators.py        ← Bus search element locators
│
├── pages/
│   ├── base_page.py           ← BasePage: shared Selenium utilities + explicit waits
│   ├── home_page.py           ← HomePage: popup dismiss + tab navigation
│   ├── flight_search_page.py  ← FlightSearchPage: search flow + validation
│   ├── hotel_search_page.py   ← HotelSearchPage: search flow + validation
│   └── bus_search_page.py     ← BusSearchPage: search flow + validation
│
├── tests/
│   ├── test_flight_search.py  ← 3 flight test cases
│   ├── test_hotel_search.py   ← 3 hotel test cases
│   └── test_bus_search.py     ← 3 bus test cases
│
├── utils/
│   ├── config_reader.py       ← Singleton YAML config reader
│   ├── driver_factory.py      ← WebDriver factory (Chrome/Firefox/Edge)
│   └── logger.py              ← Centralised logging setup
│
├── screenshots/               ← Auto-created; failure screenshots saved here
├── reports/                   ← Auto-created; HTML report saved here
├── logs/                      ← Auto-created; execution logs saved here
│
├── conftest.py                ← Driver fixture + screenshot-on-failure hook
├── pytest.ini                 ← Pytest settings, markers, HTML report path
├── requirements.txt           ← Python dependencies
└── README.md
```

---

## Configuration

Edit `config/config.yaml` to change the browser, base URL, or test data:

```yaml
browser:
  name: chrome          # chrome | firefox | edge
  headless: false       # true for CI/CD pipelines

application:
  base_url: "https://www.makemytrip.com"
  timeout: 30

search_data:
  flight:
    from_city: "Delhi"
    to_city: "Mumbai"
    departure_date_offset: 7   # days from today
  hotel:
    city: "Goa"
    checkin_date_offset: 7
    checkout_date_offset: 9
  bus:
    from_city: "Bangalore"
    to_city: "Chennai"
    travel_date_offset: 5
```

---

## Running Tests

### Run all tests (generates HTML report)

```bash
pytest
```

### Run a specific module

```bash
pytest tests/test_flight_search.py -v
pytest tests/test_hotel_search.py -v
pytest tests/test_bus_search.py -v
```

### Run by marker (smoke / regression / module)

```bash
pytest -m smoke          # Quick sanity tests only
pytest -m regression     # Full regression suite
pytest -m flight         # Flight tests only
pytest -m hotel          # Hotel tests only
pytest -m bus            # Bus tests only
```

### Run with a custom report name

```bash
pytest --html=reports/custom_report.html --self-contained-html
```

### Run in headless mode (no browser window)

Set `headless: true` in `config/config.yaml`, then:

```bash
pytest
```

---

## Reports & Screenshots

| Artifact | Location |
|---|---|
| HTML Test Report | `reports/test_report.html` |
| Failure Screenshots | `screenshots/<test_name>_<timestamp>.png` |
| Execution Log | `logs/test_execution.log` |
| Pytest Log | `logs/pytest.log` |

Open the HTML report in any browser:

```bash
start reports/test_report.html        # Windows
open reports/test_report.html         # macOS
xdg-open reports/test_report.html     # Linux
```

---

## Test Scenarios

### ✈️ Flight Search (`test_flight_search.py`)

| ID | Scenario | Marker |
|---|---|---|
| TC_FLIGHT_001 | Valid one-way flight search from config | `smoke` |
| TC_FLIGHT_002 | Alternate route search Bangalore → Delhi | `regression` |
| TC_FLIGHT_003 | URL contains "flights" after search | `regression` |

### 🏨 Hotel Search (`test_hotel_search.py`)

| ID | Scenario | Marker |
|---|---|---|
| TC_HOTEL_001 | Valid hotel search from config | `smoke` |
| TC_HOTEL_002 | Hotel search for Mumbai (result count > 0) | `regression` |
| TC_HOTEL_003 | URL contains "hotel" after search | `regression` |

### 🚌 Bus Search (`test_bus_search.py`)

| ID | Scenario | Marker |
|---|---|---|
| TC_BUS_001 | Valid bus search from config | `smoke` |
| TC_BUS_002 | Bus search Hyderabad → Bangalore | `regression` |
| TC_BUS_003 | URL contains "bus" after search | `regression` |

---

## Framework Architecture

```
Test File  →  Page Class  →  BasePage  →  Selenium WebDriver
              (POM layer)    (utilities)   (browser)
                ↕
           Locator Class     Config YAML    Logger
           (no hardcoding)   (all settings) (info/error)
```

### Core design principles

1. **Page Object Model** — Each screen/section is a separate class. Tests never contain locators.
2. **Explicit Waits** — `WebDriverWait` is used everywhere. `Thread.sleep()` is avoided; only minimal `time.sleep()` is used for suggestion-popup delays.
3. **Single Responsibility** — Locators, page actions, and test logic are fully separated.
4. **External Configuration** — All environment settings, URLs, and test data live in `config.yaml`.
5. **Automatic Screenshot** — `conftest.py` hooks into Pytest to save a screenshot the moment any test fails.
6. **Structured Logging** — Every step logs at INFO/DEBUG level to both console and `logs/test_execution.log`.

---

## 📝 License

MIT License — free to use and modify.
