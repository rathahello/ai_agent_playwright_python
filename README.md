# SauceDemo Test Automation Suite (Playwright + Python)

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-v1.40%2B-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev/python/)
[![Pytest](https://img.shields.io/badge/Pytest-v8.0%2B-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Design Pattern](https://img.shields.io/badge/Pattern-Page%20Object%20Model-FF6F00?style=for-the-badge)](https://martinfowler.com/bliki/PageObject.html)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

A robust, enterprise-grade End-to-End (E2E) test automation framework designed for the [SauceDemo](https://www.saucedemo.com/) e-commerce web application. Built with **Python 3**, **Playwright**, and **Pytest**, following the **Page Object Model (POM)** and **AAA (Arrange-Act-Assert)** design patterns.

---

## 📑 Table of Contents

- [Overview & Highlights](#-overview--highlights)
- [Project Architecture](#-project-architecture)
- [Test Specification & Traceability Matrix](#-test-specification--traceability-matrix)
  - [1. Authentication Suite (`test_auth.py`)](#1-authentication-suite-test_authpy)
  - [2. Inventory & Product Browsing (`test_inventory.py`)](#2-inventory--product-browsing-test_inventorypy)
  - [3. Shopping Cart Suite (`test_cart.py`)](#3-shopping-cart-suite-test_cartpy)
  - [4. Checkout Flow Suite (`test_checkout.py`)](#4-checkout-flow-suite-test_checkoutpy)
  - [5. Navigation & Session Controls (`test_navigation.py`)](#5-navigation--session-controls-test_navigationpy)
- [Prerequisites & Installation](#-prerequisites--installation)
- [Running Tests](#-running-tests)
  - [Basic Execution](#basic-execution)
  - [Headed vs Headless Mode](#headed-vs-headless-mode)
  - [Execution by Marker](#execution-by-marker)
  - [Targeted Test Execution](#targeted-test-execution)
- [Test Reporting & Artifacts](#-test-reporting--artifacts)
- [Configuration Reference (`pytest.ini`)](#-configuration-reference-pytestini)
- [Design Principles & Engineering Standards](#-design-principles--engineering-standards)
- [Continuous Integration (CI/CD)](#-continuous-integration-cicd)

---

## 🚀 Overview & Highlights

- **Playwright Sync API**: Utilizes Playwright's blazing-fast browser automation engine with native auto-waiting and resilient locator strategies.
- **Page Object Model (POM)**: Enforces clear separation between UI page interactions, locators, and test verification logic for optimal maintainability.
- **Arrange-Act-Assert (AAA)**: Every test case is cleanly structured for maximum readability and team collaboration.
- **Interactive HTML Dashboard**: Self-contained test reports generated automatically with `pytest-html`.
- **Automatic Execution Evidence**: Full `.webm` video recording and `.png` page state snapshots collected on every test run.
- **Visual Debugging Support**: Pre-configured `--slowmo 500` delay enables smooth, observable execution in headed mode.
- **Strict Typing & Linting**: Complete Python type hinting across fixtures, page objects, and test functions.

---

## 🏗️ Project Architecture

```plaintext
SauceDemo_system-playwright-python/
├── pages/                       # Page Object Model (POM) layer
│   ├── __init__.py
│   ├── base_page.py             # Common base page, navigation, and utilities
│   ├── login_page.py            # Login page locators and interaction methods
│   ├── inventory_page.py        # Product catalog, sorting, and item selection
│   ├── cart_page.py             # Shopping cart item verification and actions
│   ├── checkout_page.py         # Checkout steps (Information, Overview, Complete)
│   └── navigation_page.py       # Sidebar drawer menu and session controls
│
├── tests/                       # Automated test suites
│   ├── __init__.py
│   ├── test_auth.py             # TC-AUTH-001 to TC-AUTH-005 (Login & validations)
│   ├── test_cart.py             # TC-CART-001 to TC-CART-004 (Cart operations)
│   ├── test_inventory.py        # TC-INV-001 to TC-INV-004 (Catalog, sorting, details)
│   ├── test_checkout.py         # TC-CHK-001 to TC-CHK-003 (Checkout workflows)
│   └── test_navigation.py       # TC-NAV-001 to TC-NAV-002 (Logout & reset state)
│
├── reports/                     # Output directory for test runs (git-ignored)
│   ├── report.html              # Standalone interactive HTML report
│   └── artifacts/               # Test session videos (.webm) & screenshots (.png)
│
├── conftest.py                  # Pytest fixtures and browser lifecycle setup
├── pytest.ini                   # Core test runner configuration, CLI flags & markers
├── requirements.txt             # Production and test dependencies
└── README.md                    # Project documentation
```

---

## 🧪 Test Specification & Traceability Matrix

The framework covers **17 comprehensive end-to-end test scenarios**:

### 1. Authentication Suite (`test_auth.py`)

| Test ID | Name / Description | Type | Markers | Expected Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **TC-AUTH-001** | Successful Login with Standard User | Smoke / Functional | `@pytest.mark.auth`<br>`@pytest.mark.smoke` | Navigates to `/inventory.html`, header logo displays "Swag Labs", products visible. |
| **TC-AUTH-002** | Login Attempt with Locked-Out User | Negative / Error | `@pytest.mark.auth`<br>`@pytest.mark.negative` | Displays error: `Epic sadface: Sorry, this user has been locked out.` |
| **TC-AUTH-003** | Login Attempt with Empty Username | Negative / Validation | `@pytest.mark.auth`<br>`@pytest.mark.negative` | Displays error: `Epic sadface: Username is required` |
| **TC-AUTH-004** | Login Attempt with Empty Password | Negative / Validation | `@pytest.mark.auth`<br>`@pytest.mark.negative` | Displays error: `Epic sadface: Password is required` |
| **TC-AUTH-005** | Login Attempt with Invalid Credentials | Negative / Error | `@pytest.mark.auth`<br>`@pytest.mark.negative` | Displays error: `Epic sadface: Username and password do not match any user in this service` |

### 2. Inventory & Product Browsing (`test_inventory.py`)

| Test ID | Name / Description | Type | Markers | Expected Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **TC-INV-001** | Verify Inventory Items Display | Smoke / Functional | `@pytest.mark.inventory`<br>`@pytest.mark.smoke` | Exactly 6 products displayed; each contains non-empty title, description, price, and image. |
| **TC-INV-002** | Product Sorting by Name (A-Z & Z-A) | Functional | `@pytest.mark.inventory` | Correct alphabetical sort order verified for both ascending (`az`) and descending (`za`). |
| **TC-INV-003** | Product Sorting by Price (Low-High & High-Low) | Functional | `@pytest.mark.inventory` | Correct numeric price sorting verified for ascending (`lohi`) and descending (`hilo`). |
| **TC-INV-004** | View Product Details Page | Functional | `@pytest.mark.inventory` | Navigates to product detail page (`inventory-item.html?id=...`), validates details and "Back to products". |

### 3. Shopping Cart Suite (`test_cart.py`)

| Test ID | Name / Description | Type | Markers | Expected Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **TC-CART-001** | Add Item to Cart from Inventory | Smoke / Functional | `@pytest.mark.cart`<br>`@pytest.mark.smoke` | Button label toggles to "Remove"; shopping cart badge updates to `1`. |
| **TC-CART-002** | Remove Item from Cart on Inventory Page | Functional | `@pytest.mark.cart` | Button toggles back to "Add to cart"; shopping cart badge is removed. |
| **TC-CART-003** | Cart Items Persistence Across Pages | Functional | `@pytest.mark.cart` | Added items persist accurately when navigating from inventory to cart view (`cart.html`). |
| **TC-CART-004** | Remove Item Directly from Cart Page | Functional | `@pytest.mark.cart` | Item removed from cart list; badge updates count dynamically. |

### 4. Checkout Flow Suite (`test_checkout.py`)

| Test ID | Name / Description | Type | Markers | Expected Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **TC-CHK-001** | End-to-End Successful Checkout | Smoke / E2E | `@pytest.mark.checkout`<br>`@pytest.mark.smoke` | Completes step-one (shipping info), step-two (tax + subtotal validation), and finish page (`THANK YOU FOR YOUR ORDER`). |
| **TC-CHK-002** | Checkout Validation (Missing Fields) | Negative / Validation | `@pytest.mark.checkout`<br>`@pytest.mark.negative` | Verifies inline error triggers for First Name, Last Name, and Postal Code. |
| **TC-CHK-003** | Cancel Checkout Flow | Functional | `@pytest.mark.checkout` | Clicking "Cancel" on Step One returns user safely to `cart.html` with cart items preserved. |

### 5. Navigation & Session Controls (`test_navigation.py`)

| Test ID | Name / Description | Type | Markers | Expected Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **TC-NAV-001** | Sidebar Logout Functionality | Smoke / Functional | `@pytest.mark.navigation`<br>`@pytest.mark.smoke` | Opens burger menu, clicks "Logout", redirects to login page with session invalidated. |
| **TC-NAV-002** | Reset Application State via Sidebar | Functional | `@pytest.mark.navigation` | Clicks "Reset App State", clears cart badge, and empties shopping cart. |

---

## 💻 Prerequisites & Installation

### Step 1: Ensure Python 3.9+ is Installed
Check your current Python version:
```bash
python --version
# Expected: Python 3.9.x or higher
```

### Step 2: Set Up Virtual Environment
Create and activate an isolated Python environment:

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Install Playwright Browsers
Install the necessary Chromium, Firefox, and WebKit binaries:
```bash
playwright install
```
*(Optional: To install only Chromium for faster setup, run `playwright install chromium`)*

---

## 🏃 Running Tests

All execution defaults (HTML reporting, videos, screenshots, slow-motion) are pre-configured in `pytest.ini`.

### Basic Execution

Run all 17 tests in headless mode:
```bash
pytest
```

### Headed vs Headless Mode

**Run with browser UI visible (headed mode with 500ms slow motion):**
```bash
pytest --headed
```

**Run in pure headless mode (overriding slow motion for maximum speed):**
```bash
pytest --slowmo 0
```

### Execution by Marker

Target specific test categories using pytest markers:

```bash
# Run critical smoke tests across all features
pytest -m smoke

# Run authentication test suite
pytest -m auth

# Run shopping cart test suite
pytest -m cart

# Run inventory and sorting suite
pytest -m inventory

# Run checkout flow suite
pytest -m checkout

# Run sidebar navigation & session suite
pytest -m navigation

# Run all negative / validation error tests
pytest -m negative
```

### Targeted Test Execution

**Run a single test module:**
```bash
pytest tests/test_auth.py
pytest tests/test_checkout.py
```

**Run a specific test case by keyword name:**
```bash
pytest -k test_tc_auth_001_successful_login
pytest -k test_tc_chk_001_successful_checkout
```

---

## 📊 Test Reporting & Artifacts

After every test execution, all reports, media, and logs are automatically organized under the `reports/` directory:

```plaintext
reports/
├── report.html                  # Interactive, self-contained HTML test report
└── artifacts/                   # Per-test visual proof
    ├── test_tc_auth_001_.../
    │   ├── video.webm           # Complete test playback video
    │   └── test-finished-1.png  # High-resolution screenshot of final state
    └── ...
```

### Viewing the HTML Report

**Windows (PowerShell):**
```powershell
Start-Process .\reports\report.html
```

**Windows (CMD):**
```cmd
start .\reports\report.html
```

**macOS:**
```bash
open reports/report.html
```

**Linux:**
```bash
xdg-open reports/report.html
```

---

## ⚙️ Configuration Reference (`pytest.ini`)

The project uses `pytest.ini` for centralized runner management:

```ini
[pytest]
pythonpath = .
testpaths = tests
addopts = 
    --slowmo 500
    --html=reports/report.html
    --self-contained-html
    --screenshot=on
    --video=on
    --output=reports/artifacts
markers =
    auth: Authentication and login test suite
    cart: Shopping cart test suite
    inventory: Inventory and product browsing test suite
    checkout: Checkout flow test suite
    navigation: Navigation and session control test suite
    smoke: Critical path smoke tests
    negative: Negative test scenarios and validation error checks
```

| Setting | Purpose |
| :--- | :--- |
| `pythonpath = .` | Ensures root directory imports (e.g. `pages.*`) resolve cleanly without package errors. |
| `testpaths = tests` | Restricts test discovery to the `tests/` directory. |
| `--slowmo 500` | Inserts a 500ms pause between actions for clear visual observation during headed runs. |
| `--html` & `--self-contained-html` | Generates a standalone single-file HTML report with embedded styles and assets. |
| `--screenshot=on` | Captures full viewport screenshots upon test completion. |
| `--video=on` | Records webm video clips of each test execution. |
| `--output` | Destination path for media artifacts. |

---

## 📐 Design Principles & Engineering Standards

1. **Page Object Model (POM)**:
   - All locators (`page.locator(...)`) and UI actions are encapsulated in `pages/`.
   - Test files in `tests/` contain pure business logic and assertions without direct selector manipulation.
2. **Web-First Assertions**:
   - Uses Playwright's `expect(locator).to_be_visible()`, `expect(page).to_have_url(...)`, etc., providing automatic retry and waiting to eliminate test flakiness.
3. **Arrange-Act-Assert (AAA)**:
   - Clear visual separation between setting up preconditions, triggering user actions, and asserting expected results.
4. **Pytest Fixtures**:
   - Page object instances are cleanly injected into test methods via `conftest.py` fixtures (`login_page`, `inventory_page`, `cart_page`, `checkout_page`, `navigation_page`).
5. **Robust Locators**:
   - Prioritizes resilient selectors such as `[data-test="..."]`, `id`, and accessible roles over brittle XPath or dynamic CSS classes.

---

## 🔄 Continuous Integration (CI/CD)

The test suite can be integrated seamlessly into GitHub Actions. Below is an example workflow configuration (`.github/workflows/e2e.yml`):

```yaml
name: SauceDemo Playwright E2E Tests

on:
  push:
    branches: [ demo-system, master, main ]
  pull_request:
    branches: [ demo-system, master, main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install Dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt

      - name: Install Playwright Browsers
        run: playwright install --with-deps chromium

      - name: Run Tests
        run: pytest --slowmo 0

      - name: Upload Test Report & Artifacts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-test-reports
          path: reports/
          retention-days: 14
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
Test application provided by [Sauce Labs](https://saucelabs.com/).
