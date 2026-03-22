# MakeMyTrip Automation Framework

A scalable and robust Selenium automation framework for MakeMyTrip (MMT), built using Python, Pytest, and the Page Object Model (POM) design pattern.

## Features

- **Page Object Model (POM)**: Organized and maintainable structure with separate classes for each page.
- **Robust Overlay Handling**: Implements aggressive dismissal logic for various MMT pop-ups and modals (Login, Tooltips, Ads).
- **Transient Loading Interception**: Proactively waits for loading overlays to disappear before interacting with elements.
- **Click Retry Logic**: Automatically catches `ElementClickInterceptedException` and retries using JavaScript clicks as a fallback.
- **Undetected Chromedriver**: Integrated to bypass basic anti-bot measures and headless browser detection.
- **Configuration Driven**: Environment-specific settings (URL, browser, timeouts) are managed via `config.yaml`.
- **Comprehensive Logging**: Detailed logs for every action and error, stored in `automation.log`.
- **Automatic Reporting**: Generates self-contained HTML reports with failure screenshots and DOM snapshots.

## Framework Structure

- `pages/`: Contains Page Object classes (`BasePage`, `HomePage`, `SearchResultsPage`, `DetailsPage`).
- `tests/`: Contains Pytest test cases (`test_details.py`).
- `utils/`: Utility classes for configuration logging.
- `screenshots/`: Automatically stores screenshots and DOM snapshots for failed tests.
- `config.yaml`: Centralized configuration for the framework.
- `requirements.txt`: Python dependencies.

## Setup and Execution

### Prerequisites

- Python 3.8+
- Google Chrome browser installed.

### Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Execution

To run all tests and generate an HTML report:
```bash
python -m pytest tests/test_details.py --html=report.html --self-contained-html
```

## Note on Environment Constraints

MakeMyTrip uses advanced CDN protection (Akamai). In some automated environments, requests may be blocked with a 403 Forbidden error or land on an access-denied page. This framework is designed with best-in-class tools (`undetected-chromedriver`) and retry logic to mitigate these issues in standard user environments.
