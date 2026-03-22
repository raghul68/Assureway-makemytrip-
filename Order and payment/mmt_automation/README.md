# MakeMyTrip Selenium Automation (Python + Pytest)

A basic, scalable Selenium automation framework for MakeMyTrip's booking flow.

## 📁 Project Structure
- `config.json`: External configuration for environment variables and test data.
- `conftest.py`: Shared pytest fixtures (driver setup, teardown) and hooks (screenshot on failure).
- `order_payment_page.py`: Page Object Model (POM) containing all locators and core actions.
- `test_order_payment.py`: Automated test scenarios (Booking and Payment page validation).
- `requirements.txt`: Python package dependencies.
- `.gitignore`: Excludes unnecessary files from the repository.

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8+
- Google Chrome browser installed

### 2. Setup
```bash
# Recommendation: use a virtual environment (optional)
# python -m venv venv
# .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Running Tests
```bash
# From the mmt_automation folder
pytest test_order_payment.py
```

## 🛠 Features
- **Page Object Model (POM)**: Separation of UI locators from test logic.
- **Config Management**: External JSON for dynamic environment management.
- **Automatic Driver Handling**: Uses `webdriver-manager` to manage Chromedriver.
- **Screenshot on Failure**: Automatically captures screenshots in the `screenshots/` folder if a test fails.
- **Explicit Waits**: Uses `WebDriverWait` for stable element interaction (no `time.sleep`).
- **Scalable**: Easy to add more pages or more test cases.

## ⚠️ Important Note
- This automation does **not** perform real payments.
- It validates the presence of price and payment options on the payment screen.
