# 🚀 MakeMyTrip Selenium Automation Framework

A production-grade, **Python + Pytest** Selenium test automation framework for [MakeMyTrip](https://www.makemytrip.com/) built using the **Page Object Model (POM)** design pattern.

---

## 📁 Project Structure

```
makemytrip_automation/
│
├── config.yaml              # External config: URL, browser, timeouts, credentials
├── pytest.ini               # Pytest settings, markers, logging format
├── requirements.txt         # Python dependencies
├── conftest.py              # Driver fixture + screenshot-on-failure hook
├── .gitignore
│
├── pages/                   # Page Object Model layer
│   ├── __init__.py
│   ├── base_page.py         # BasePage — shared interactions (find, click, wait)
│   └── login_page.py        # LoginPage — locators & methods for login modal
│
├── tests/                   # Test layer (never contains locators)
│   ├── __init__.py
│   └── test_login.py        # 5 Login test cases
│
├── utils/                   # Framework utilities
│   ├── __init__.py
│   ├── logger.py            # INFO/ERROR logger → console + logs/execution.log
│   └── helpers.py           # Screenshot, explicit waits, safe-click, scroll
│
├── screenshots/             # Auto-created — failure screenshots land here
├── reports/                 # Auto-created — HTML reports land here
└── logs/                    # Auto-created — execution logs land here
```

---

## 🧩 Prerequisites

| Requirement | Minimum version |
|---|---|
| Python | 3.9+ |
| Google Chrome | Latest stable |
| ChromeDriver | Auto-managed by `undetected-chromedriver` |
| Git | Latest (for version control) |

---

## ⚙️ Installation

```bash
# 1. Clone the repository (after pushing to GitHub)
git clone https://github.com/<your-username>/makemytrip-automation.git
cd makemytrip-automation/makemytrip_automation

# 2. (Recommended) Create a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS / Linux

# 3. Install all dependencies
pip install -r requirements.txt
```

---

## 🔧 Configuration

Edit **`config.yaml`** before running tests:

```yaml
base_url:  "https://www.makemytrip.com/"
browser:   "chrome"
headless:  false          # Set true for CI/CD (limited support with undetected-chrome)
explicit_wait: 20         # seconds — used by all WebDriverWait calls

credentials:
  valid_phone:   "9999999999"   # Replace with a real Indian mobile number for TC_001
  invalid_phone: "123"
  invalid_email: "invalid_email_format"
```

> ⚠️ **MakeMyTrip login uses OTP** — a real OTP is sent to `valid_phone`. TC_LOGIN_001 only verifies the UI reaches the OTP screen; it does not submit an OTP.

---

## ▶️ Running Tests

```bash
# Run all login tests with verbose output + HTML report
python -m pytest tests/test_login.py -v --html=reports/login_report.html --self-contained-html

# Run all tests
python -m pytest tests/ -v --html=reports/report.html --self-contained-html

# Run by marker
python -m pytest -m login -v

# Run a single test by name
python -m pytest tests/test_login.py::TestLogin::test_valid_login_with_phone -v
```

---

## 🧪 Test Cases (Login Module)

| ID | Test | Expected Result |
|---|---|---|
| TC_LOGIN_001 | Valid phone number | OTP input screen renders |
| TC_LOGIN_002 | Empty form submission | Validation error displayed |
| TC_LOGIN_003 | Short/invalid phone (123) | Error shown / OTP not shown |
| TC_LOGIN_004 | Malformed email | Error shown / OTP not shown |
| TC_LOGIN_005 | Modal heading UI check | Modal heading text is non-empty |

---

## 🏗️ Framework Architecture

### Page Object Model (POM)

```
BasePage (pages/base_page.py)
 └── LoginPage (pages/login_page.py)
        ├── Locators  (class-level constants)
        └── Methods   (click_login_button, enter_phone, click_continue, …)
```

- **Locators** are stored only inside page classes → tests never contain XPaths/CSS selectors.
- **`BasePage`** provides `find()`, `click()`, `type_text()`, `is_element_visible()` using explicit waits.
- **`WebDriverWait`** is used everywhere; `Thread.sleep` / `time.sleep` only in teardown.

### Screenshot on Failure

`conftest.py` registers a `pytest_runtest_makereport` hook:
- Fires after every test **call phase**
- If the test **FAILED**: captures a PNG → `screenshots/FAIL__<test_name>_<timestamp>.png`
- Attaches screenshot to the **pytest-html** report automatically

### Logging

`utils/logger.py` configures:
- **Console**: `INFO` and above
- **File**: `logs/execution_<timestamp>.log` — `DEBUG` and above (every wait, click, assertion)

---

## 🌐 Git Setup

Git is not installed yet on this machine. To push to GitHub:

```bash
# 1. Install Git
winget install Git.Git

# 2. Initialise repository (from project root)
git init
git add .
git commit -m "feat: initial MakeMyTrip login automation framework"

# 3. Create a public GitHub repo and push
git remote add origin https://github.com/<your-username>/makemytrip-automation.git
git branch -M main
git push -u origin main
```

---

## ⚠️ Known Limitations

| Issue | Reason | Mitigation |
|---|---|---|
| Bot detection | MakeMyTrip uses Cloudflare + reCAPTCHA | `undetected-chromedriver` reduces fingerprinting |
| OTP submission | Live OTP required — not automatable | TC_001 validates UI flow only (up to OTP screen) |
| Dynamic locators | MMT updates their HTML frequently | XPath locators include multiple fallback expressions |

---

## 📋 Dependencies

| Package | Purpose |
|---|---|
| `selenium` | Core browser automation |
| `undetected-chromedriver` | Anti-bot Chrome driver |
| `pytest` | Test framework |
| `pytest-html` | HTML test reports |
| `PyYAML` | Config file parsing |
| `webdriver-manager` | Auto-downloads ChromeDriver |
| `Pillow` | Image processing for screenshots |
